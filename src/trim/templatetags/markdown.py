from django import template
from django.urls import resolve, reverse
from django.conf import settings

from .shared_tools import parse_until

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
        self.token_template_name = template.Variable(tokens[0])
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
            plain_markdown_text = textwrap.dedent(django_markdown_text)
            return md.convert(plain_markdown_text)



@register.inclusion_tag('trim/templatetags/markdown_file_content.html', takes_context=True,
                        name='markdown.file')
def src_code_content_template(context, part_a=None, part_b=None, *args, **kwargs):
    """Load and process a markdown file.
    """
    base_dir = settings.POLYPOINT_DOCS_DIR
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


def get_file_contents(path, parent=None):
    parent = parent or settings.POLYPOINT_DEMO_DIR
    target = parent / path
    print('target', target)
    exists = target.exists()
    content = None
    if exists:
        content = target.read_text()
    return {
        'filepath': target,
        'exists': exists,
        'content': content,
    }