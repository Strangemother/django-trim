from django import template
from django.urls import resolve, reverse
from django.template.loader_tags import (
        do_extends,
        construct_relative_path,
        BLOCK_CONTEXT_KEY,
        BlockNode,
        Node, Template, BlockContext, TextNode
        )

from django.template.base import TemplateSyntaxError

from ..context import theming

register = template.Library()


@register.simple_tag(takes_context=True)
def theme_string(context):
    pass

from django.template.base import token_kwargs

@register.tag('theme')
def do_theme_extends(parser, token):
    # replace the token with the string tokeniser.
    bits = token.split_contents()
    extra = {}
    # bits[1] = construct_relative_path(parser.origin.template_name, bits[1])

    # Track the position of thr 'with' statement, to parse all string
    # bits before the position.
    with_position = None

    parts = ()
    for i, word in enumerate(bits):
        if word == 'with':
            with_position = i
            extra = token_kwargs(bits[i+1:], parser)
            break
        if i == 0:
            continue
        # push bit into text ignoring 0
        parts += (word,)

    # Parse vars before i
    parent_name = parser.compile_filter(bits[1])
    # path = theming[parent_name.var]

    # if path is None:
    #     raise TemplateSyntaxError("'%s' Unknown theme name" % parent_name)

    template_vars = tuple(parser.compile_filter(x) for x in parts)
    # token.contents = ' '.join((bits[0], f'"{path}"',))

    # bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    # parent_name = parser.compile_filter(bits[1])

    nodelist = parser.parse()
    if nodelist.get_nodes_by_type(ThemeExtendsNode):
        raise TemplateSyntaxError("'%s' cannot appear more than once in the same template" % bits[0])

    return ThemeExtendsNode(nodelist, template_vars, extra_context=extra, origin=parser.origin)


class ThemeExtendsNode(Node):
    must_be_first = True
    context_key = 'extends_context'

    def __init__(self, nodelist, template_vars, template_dirs=None, extra_context=None, **kw):
        self.nodelist = nodelist
        self.parent_name = None
        self.template_vars = template_vars
        self.template_dirs = template_dirs
        self.blocks = {n.name: n for n in nodelist.get_nodes_by_type(BlockNode)}
        self.extra_context = extra_context or {}
        self.kwargs = kw or {}

    def get_parent_token(self):
        if self.parent_name:
            return self.parent_name.token
        return tuple(x.token for x in self.template_vars)

    def __repr__(self):
        return '<%s: extends %s>' % (self.__class__.__name__, self.get_parent_token())

    def find_template(self, template_name, context):
        """
        This is a wrapper around engine.find_template(). A history is kept in
        the render_context attribute between successive extends calls and
        passed as the skip argument. This enables extends to work recursively
        without extending the same template twice.
        """
        history = context.render_context.setdefault(
            self.context_key, [self.origin],
        )
        template, origin = context.template.engine.find_template(
            template_name, skip=history,
        )
        history.append(origin)
        return template

    def resolve_parent(self, context):
        if self.parent_name:
            return self.parent_name.resolve(context)
        return self.resolve_theme_parent(context)

    def resolve_theme_parent(self, context):
        """Resolve the synonym of the `parent_name` for the _theming_
        multi string"""
        # resolve_buts,
        res = ()
        for template_var in self.template_vars:
            rtv = template_var.resolve(context)
            res += (rtv,)

        # Provide the parts into the theming,
        position_bit = theming.resolve_theme_parent(res, self.origin, context)
        path = construct_relative_path(self.origin.template_name, position_bit)
        return path
        # path = theming[parent_name.var]

    def get_parent(self, context):
        parent = self.resolve_parent(context)
        if not parent:
            error_msg = "Invalid template name in 'extends' tag: %r." % parent
            if self.parent_name.filters or\
                    isinstance(self.parent_name.var, Variable):
                error_msg += " Got this from the '%s' variable." %\
                    self.parent_name.token
            raise TemplateSyntaxError(error_msg)
        if isinstance(parent, Template):
            # parent is a django.template.Template
            return parent
        if isinstance(getattr(parent, 'template', None), Template):
            # parent is a django.template.backends.django.Template
            return parent.template
        return self.find_template(parent, context)

    def render(self, context):
        compiled_parent = self.get_parent(context)

        if BLOCK_CONTEXT_KEY not in context.render_context:
            context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()
        block_context = context.render_context[BLOCK_CONTEXT_KEY]

        # Add the block nodes from this node to the block context
        block_context.add_blocks(self.blocks)

        # If this block's parent doesn't have an extends node it is the root,
        # and its block nodes also need to be added to the block context.
        for node in compiled_parent.nodelist:
            # The ThemeExtendsNode has to be the first non-text node.
            if not isinstance(node, TextNode):
                if not isinstance(node, ThemeExtendsNode):
                    blocks = {n.name: n for n in
                              compiled_parent.nodelist.get_nodes_by_type(BlockNode)}
                    block_context.add_blocks(blocks)
                break

        extra = self.extra_context


        # Call Template._render explicitly so the parser context stays
        # the same.
        with context.render_context.push_state(compiled_parent, isolated_context=False):
            extra = {key: val.resolve(context) for key, val in extra.items()}
            print('Extra', extra)
            context.push(extra)
            return compiled_parent._render(context)


@register.filter(name='attr')
def get_attr(value, arg):
    """Return the _attribute_ of the given object, such as a model field from a
    model instance.

        {{ object|attr:field }}

    Example:

        {% load theming %}

        {% with field="field_name" %}
        The value of {{ field }} for model "{{ object }}" == {{ object|attr:field }}
        {% endwith %}

    """
    return getattr(value,arg)
