from django import template
from django.urls import resolve, reverse
from django.conf import settings

from .shared_tools import parse_until, parse_tag

import textwrap

try:
    import markdown as markdown_orig
except ImportError:
    markdown_orig = None


register = template.Library()



@register.tag(name="markdown")
def do_slot(parser, token):
    nodelist, splits, extra = parse_until(parser, token, ('endmarkdown',))
    return MarkdownContentNode(nodelist, splits, **extra)


class MarkdownContentNode(template.Node):

    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist

        self.token_template_name = None
        if len(tokens) > 0:
            self.token_template_name =  template.Variable(tokens[0])
        self.extra_context = kw

    def render(self, context):
        print('rendering markdown')

        wrap = {}
        md = get_markdown_object()

        # Make a resolved dict of values given through the init.
        values = {key: val.resolve(context) for key, val in self.extra_context.items()}
        with context.push(**wrap, **values):
            # Context({'source': content}, autoescape=context.autoescape)
            ## This is markdown plain - convert to rendered markdown
            django_markdown_text = self.nodelist.render(context)
            django_markdown_text = '\n'.join([m.lstrip() for m in django_markdown_text.split('\n')])

            if django_markdown_text[0] == '\n':
                django_markdown_text = django_markdown_text[1:]

            plain_markdown_text = textwrap.dedent(django_markdown_text)
            return md.convert(plain_markdown_text)


from django.template.loader_tags import (
        TemplateSyntaxError,
        construct_relative_path,
        Node,
        token_kwargs,
    )


@register.tag("markdown.file_2")
def do_markdown_file(parser, token):
    """
    Load a template and render it with the current context. You can pass
    additional context using keyword arguments.

    _This is a direct clone of the include node with an alterntive Node parser._

    Example::

        {% markdown.file "foo" "some/include.md" %}
        {% markdown.file "foo" "some/include.md" with bar="BAZZ!" baz="BING!" %}

    Use the ``only`` argument to exclude the current context when rendering
    the included template::

        {% markdown.file "foo" "some/include.md" only %}
        {% markdown.file "foo" "some/include.md" with bar="1" only %}
    """
    # bits = token.split_contents()
    # if len(bits) < 2:
    #     raise TemplateSyntaxError(
    #         "%r tag takes at least one argument: the name of the template to "
    #         "be included." % bits[0]
    #     )

    # options = {}
    # remaining_bits = bits[2:]
    # while remaining_bits:
    #     option = remaining_bits.pop(0)
    #     if option in options:
    #         raise TemplateSyntaxError(
    #             "The %r option was specified more than once." % option
    #         )
    #     if option == "with":
    #         value = token_kwargs(remaining_bits, parser, support_legacy=False)
    #         if not value:
    #             raise TemplateSyntaxError(
    #                 '"with" in %r tag needs at least one keyword argument.' % bits[0]
    #             )
    #     elif option == "only":
    #         value = True
    #     else:
    #         raise TemplateSyntaxError(
    #             "Unknown argument for %r tag: %r." % (bits[0], option)
    #         )
    #     options[option] = value

    # namemap = options.get("with", {})


    bits, namemap, options = parse_tag(parser, token)

    # bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    isolated_context = options.get("only", False)

    c_bits = tuple(parser.compile_filter(value) for value in bits)
    return IncludeNode(
        c_bits,
        extra_context=namemap,
        isolated_context=isolated_context,
    )


class IncludeNode(Node):
    context_key = "__include_context"

    def __init__(self, template_bits, *args, extra_context=None,
                 isolated_context=False, **kwargs):
        self.template_bits = template_bits
        self.extra_context = extra_context or {}
        self.isolated_context = isolated_context
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: template_bits={self.template_bits!r}>"

    def render(self, context):
        """
        Render the specified template and context. Cache the template object
        in render_context to avoid reparsing and loading when used in a for
        loop.
        """

        # convert the vars into resolved strings
        resolved_bits = (x.resolve(context) for x in self.template_bits)

        ## In the original version, this _template_ (resolved str) is a
        # path to a template. However here we have content to resolve.
        # (like a block...)

        #engine.from_string(...)

        # template = self.template.resolve(context)
        # Does this quack like a Template?
        if not callable(getattr(template, "render", None)):
            # If not, try the cache and select_template().
            template_name = template or ()
            if isinstance(template_name, str):
                template_name = (
                    construct_relative_path(
                        self.origin.template_name,
                        template_name,
                    ),
                )
            else:
                template_name = tuple(template_name)
            cache = context.render_context.dicts[0].setdefault(self, {})
            template = cache.get(template_name)
            if template is None:
                template = context.template.engine.select_template(template_name)
                cache[template_name] = template
        # Use the base.Template of a backends.django.Template.
        elif hasattr(template, "template"):
            template = template.template

        values = {
            name: var.resolve(context) for name, var in self.extra_context.items()
        }

        # info = get_file_contents(bits[1], bits[0])

        if self.isolated_context:
            return template.render(context.new(values))
        with context.push(**values):
            return template.render(context)


@register.inclusion_tag('trim/templatetags/markdown_file_content.html', takes_context=True,
                        name='markdown.file')
def src_code_content_template(context, part_a=None, part_b=None, *args, **kwargs):
    """Load and process a markdown file.

    The target file may be an _absolute_ path or _relative_ within a
    TRIM_MARKDOWN_DIRS entry.

    absolute:

        {% markdown.file '/abs/path/to/readme.md' %}

    relative takes two parts:

        {% markdown.file "docs" 'points/readme.md' %}

    The `base_dir` `"docs"` is populated give the settings config:

            # a pack of locations we can use for {% markdown.file filepath %}
            TRIM_MARKDOWN_DIRS = {
                'point_src': POLYPOINT_SRC_DIR,
                'point_src_rel': POLYPOINT_THEATRE_SRC_RELATIVE_PATH,
                'site_demos': POLYPOINT_DEMO_DIR,
                'docs': POLYPOINT_DOCS_DIR,
            }

    The `TRIM_MARKDOWN_DIRS` entry (such as "docs") should be an absolute path,
    allowing the file target `[base_dir] / [relative_path]`.

    """
    base_dir = None
    filename = part_a

    if part_b is not None:
        base_dir = settings.TRIM_MARKDOWN_DIRS.get(part_a)
        # dir, filename.
        filename = part_b


    info = get_file_contents(filename, base_dir)
    if info['exists']:
        content = info['content']
        md = get_markdown_object()
        info['html'] = md.convert(content)
        info['metadata'] = md.Meta
    else:
        print('Does not exist', info)

    return {
        'markdown_object': info,
    }


@register.inclusion_tag('trim/templatetags/markdown_file_content.html', takes_context=True,
                        name='markdown.text')
def src_code_content_text(context, *args, **kwargs):
    """Load and process markdown from a var or string.

        {% markdown.text 'This _content_ is rendered through **Markdown**' %}
    """

    content = "\n".join(args)

    info = {
        'filepath': None,
        'exists': True,
        'content': content,
    }


    md = get_markdown_object()
    info['html'] = md.convert(content)
    info['metadata'] = md.Meta

    return {
        'markdown_object': info,
    }


def get_markdown_object():
    # context['view']

    # meta into the context.
    # HTML is the raw
    # https://python-markdown.github.io/extensions/
    extensions=[
        'meta',
        # 'extra',
        "pymdownx.extra",

    ]

    if markdown_orig is None:
        raise MissingImportError('markdown module is not installed.')

    md = markdown_orig.Markdown(extensions=extensions)
    return md


from pathlib import Path


def get_file_contents(path, parent=None, safe=True):
    if parent is None and safe is True:
        target = Path('.') / path
        exists = target.exists()
        return {
            'filepath': target,
            'exists': exists,
            'error': 'no parent defined',
        }
    target = Path(parent) / path
    print('target', target)
    exists = target.exists()
    content = None
    if exists and target.is_file():
        content = target.read_text()
    else:
        exists = False
    return {
        'filepath': target,
        'exists': exists,
        'content': content,
    }