from django.template import Context
from django import template
from django.template.base import token_kwargs
from . import quickforms

from loguru import logger

log = logger.debug

def inject_node(parser):
    T=parser.tokens[0].__class__
    tr = "{{ slotplot }}"
    parser.prepend_token( T(parser.tokens[0].token_type, tr))


register = template.Library()


def parse_until(parser, token, ends, delete_first=True):
    """`parser` is the iterative unit processing the nodes
    The `token` represents the current block, such as '<block token "wrap">'
    `ends` are a list of end-tokens to stop the parser

    """
    nodelist = parser.parse(ends)
    if delete_first:
        parser.delete_first_token()
    # inject_node(parser)
    splits = token.split_contents()[1:]
    extra = {}
    for i, word in enumerate(splits):
        if word == 'with':
            extra = token_kwargs(splits[i+1:], parser)
    return nodelist, splits, extra


@register.tag(name="wrap")
def do_wrap(parser, token):
    """ Wrap the contents given to the nodem with another template given through
    the tag token:

        {% wrap "stocks/wrap_form.html" with button_text="Next"  action="/fo/bar" %}
            <ul>
            {% for row in form %}
                <li>{{ row }}</li>
            {% endfor %}
            </ul>
        {% endwrap %}

    The template "wrap_forms.html" should refer to the `wrap.content` and any
    other variables from the `with` or parent contexts.

        <form method="post"
          enctype="multipart/form-data"
          {% if action %}action="{{action}}"{% endif %}>

            {{ wrap.content }}
            <input class='btn'
                type="submit"
                value="{% firstof button_text 'Confirm' %}">
            {% csrf_token %}
        </form>
    """
    log('   _def_ do wrap')
    token.slotinfo = SlotList()
    token.slotdefine = SlotList()
    nodelist, splits, extra = parse_until(parser, token, ('endwrap',))
    return WrappedContentNode(nodelist, splits, **extra)


class SlotList(object):
    def __init__(self, *a, **kw):
        log('  _def_ new SlotList', id(self))
        self.units =()

    def add(self, unit):
        # log(' -- SlotList.add', unit)
        self.units += (unit,)

    def get_nodes(self, first_token, context=None, default_value=None):
        """Return the target node given the name, this
        could be None, "default" or _named_
        """
        res = ()
        for unit in self.units:
            names = unit.get_slot_names(context)
            if first_token in names:
                log('Found match!')
                res += ((first_token, unit,),)

        return res # default_value # content = slotlist.

    def __repr__(self):
        return f'<{self.__class__.__name__} {len(self.units)} slots>'


class WrappedContentNode(template.Node):
    def __init__(self, nodelist, tokens, *a, **kw):
        log('  _cre_ __init__ wrap')
        self.nodelist = nodelist
        self.tokens = tokens
        self.token_template_name = template.Variable(tokens[0])
        self.extra_context = kw

    def render(self, context):
        slots = self.token.slotinfo
        log(f'    _ren_ Wrap node rendering template with: {slots}')
        ## The name supplied to the wrap object. {% wrap "name.html" %}
        ### Note (bug(: This doesn't work with relative paths.
        template_name = self.token_template_name.resolve(context)

        ## The imported child to import into the view wrap.
        wrap_templ = context.template.engine.get_template(template_name)

        # wrap_templ.compile_nodelist()
        nodes = wrap_templ.nodelist
        ## discover slots.
        for node in nodes:
            if isinstance(node, DefineSlotNode):
                log(' ! Found definition slot')
                log(f"{type(node)} {node}")
                node.apply_parent(self)

        # import pdb; pdb.set_trace()  # breakpoint 4d2da5d4 //
        ## The data given to the wrap -
        content = self.nodelist.render(context)


        # we extend the original context; allowing this unit to be overwitten
        # if required.
        wrap = {
                'content': content,
                'template_name': template_name
            }
        #  Dynamic key for the root context, static key for the 'wrap' object.
        content_key = 'content'
        sub_ctx = {'wrap':wrap, content_key:content}
        # values = {key: val.resolve(context) for key, val in self.extra_context.items()}
        values = {}
        for key, val in self.extra_context.items():
            values[key] = val.resolve(context) if hasattr(val, 'resolve') else val
            # values = {key: val.resolve(context) }
        with context.push(**sub_ctx, **values):
            # Context({'source': content}, autoescape=context.autoescape)
            return wrap_templ.render(context)


@register.tag(name="slot.define")
def do_define_slot(parser, token):
    """A definition slot to apply within the wrap target

            {% slot.define "name" %}content will be replaced{% endslot %}

        The wrap targets this slot

            {% wrap 'foo.html' %}
                {% slot "name" %}
                    Content to replace the slot.
                {% endslot %}
            {% endwrap %}
    """
    nodelist, splits, extra = parse_until(parser, token, ('endslot',))
    res = DefineSlotNode(nodelist, splits, **extra)
    for node_name, token_node in parser.command_stack[::-1]:
        # push this into the wrap above.
        if node_name == 'wrap':
            log('  _dis_ "slot.define" discovered parent (wrap)', token_node)
            token_node.slotdefine.add(res,)

    return res


@register.tag(name="slot")
def do_slot(parser, token):
    """A `{% slot %} {% endslot %}`  token to capture a placeholder replacement
    for a wrap. The HTML within is applied to the target slot.

    Parse the content and return a SlotNode. This new node is applied to the
    first discovered `{% wrap %}` parent.

    return the new SlotNode
    ---

    The appliance captures the nodes within within the block, then
    iterates backward through the parser node stack until the first
    `wrap` node.
    This new SlotNode instance is pushed into the wrap token `slotinfo`
    list, later inspected when the Wrap is rendered.

    Note: the slotinfo is within the _token_ `token_node` and not the _Node_,
    as the target _wrap_ node may not exist yet (being a currently unrendered
    token).
    """
    nodelist, tokens, extra = parse_until(parser, token, ('endslot',))
    res = SlotNode(nodelist, tokens, **extra)

    for node_name, token_node in parser.command_stack[::-1]:
        # push this into the wrap above.
        if node_name == 'wrap':
            log('  _dis_ "slot" discovered parent (wrap)', token_node)
            token_node.slotinfo.add(res,)

    return res


class DefineSlotNode(template.Node):
    """The slot definition, within the main wrap.html."""

    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist
        first_token = tokens[0] if len(tokens) > 0 else 'no-name'
        self.token_slot_name = template.Variable(first_token)
        self.tokens = tokens
        self.extra_context = kw
        self.args = a
        log(f' _cre_ DefineSlotNode, {self.tokens} {self.args} {self.extra_context}')

    def apply_parent(self, wrap_node):
        """set the parent wrapper.
        """
        self.extra_context['parent_wrap'] = wrap_node

    def resolve_extra_context(self, context):
        values = {}
        for key, val in self.extra_context.items():
            values[key] = val.resolve(context) if hasattr(val, 'resolve') else val
        return values

    def render(self, context):
        # template_name = self.token_template_name.resolve(context)
        # t = context.template.engine.get_template(template_name)
        log(f'   _ren_ DefineSlotNode, {self.tokens}')
        ## The content should be the content from the rendered slot info
        first_token = self.tokens[0]

        # content applied within the definition,
        # before the parent slot implements any changes.
        default_slot_content = self.nodelist.render(context)

        ## Grab 'name' from the wrap slots.
        parent_slots = self.extra_context['parent_wrap'].token.slotinfo
        matches = parent_slots.get_nodes(first_token, context)

        if len(matches) > 0:
            ## The parent has a given a slot matching this definition name.
            #The content from the slot should be stripped from the wrap render
            #and applied here; replacing the `default_slot_content`
            log('Found matches')
            ks = tuple(x[0] for x in matches)
            content = f'Found matches {ks}'
            vv = self.nodelist.render(context)
            for name, node in matches:
                # pump out first detection
                return node.nodelist.render(context)
        else:
            content = default_slot_content
        # we extend the original context; allowing this unit to be overwitten
        # if required.
        sub_ctx = {
                # Given to the definition slot
                'slot': {
                    'rendered_content': content
                }
            }

        values = self.resolve_extra_context(context)
        with context.push(**sub_ctx, **values):
            # Context({'source': content}, autoescape=context.autoescape)
            return self.nodelist.render(context)


class SlotNode(template.Node):
    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist
        first_token = tokens[0] if len(tokens) > 0 else self.get_default_name()
        self.token_slot_name = template.Variable(first_token)
        self.tokens = tokens
        self.extra_context = kw
        self.args = a
        log(f' _cre_ SlotNode, {self.tokens} {self.args} {self.extra_context}')

    def get_default_name(self):
        return '"default"'

    def get_slot_names(self, context=None):
        """
        context required _variables_ are to be processed
        """
        v = self.token_slot_name
        if context:
            v = v.resolve(context) if hasattr(v, 'resolve') else v
        return v

    def render(self, context):
        # template_name = self.token_template_name.resolve(context)
        # t = context.template.engine.get_template(template_name)
        names = self.get_slot_names(context)
        # self.default_render(self, context)
        log(f'   _ren_ SlotNode, {names}')
        return f'<div class="color-gray">cut slot {names}</div>'

    def default_render(self, context):
        content = self.nodelist.render(context)
        # we extend the original context; allowing this unit to e overbwitten
        # if required.
        wrap = {
                'content': content,
            }
        #  Dynamic key for the root context, static key for the 'wrap' object.
        content_key = 'content'
        sub_ctx = {}# = {'wrap':wrap, content_key:content}
        values = {key: val.resolve(context) for key, val in self.extra_context.items()}
        with context.push(**sub_ctx, **values):
            # Context({'source': content}, autoescape=context.autoescape)
            return self.nodelist.render(context)



# @register.simple_tag(takes_context=True)
# def info_form(context, product_id):
#     return forms.ProductQuestionForm(initial={
#             'product_id':product_id,
#         })
#
# @register.inclusion_tag('dummy.html')
# def wrap(template='default.html'):
#     return {'template': template}
