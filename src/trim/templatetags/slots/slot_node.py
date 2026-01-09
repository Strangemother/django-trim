from django import template
from loguru import logger

from .base import SlotList, parse_until

log = logger.debug


def slot_into_parent(parser, slotnode, slotlist_name, parent_node_name="wrap"):
    for node_name, token_node in parser.command_stack[::-1]:
        # push this into the wrap above.
        if node_name == parent_node_name:
            log(f'Pushing "{slotnode}" into parent "{node_name}".{slotlist_name}')
            if slotlist_name == "slotdefine":
                import pdb

                pdb.set_trace()  # breakpoint 5ae4487e //

            getattr(token_node, slotlist_name).add(slotnode)


# @register.tag(name="slot.define")
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
    nodelist, splits, extra = parse_until(parser, token, ("endslot",))
    res = DefineSlotNode(nodelist, splits, **extra)
    slot_into_parent(parser, res, "slotdefine")
    return res

    # for node_name, token_node in parser.command_stack[::-1]:
    #     # push this into the wrap above.
    #     if node_name == 'wrap':
    #         log('  _dis_ "slot.define" discovered parent (wrap)', token_node)
    #         token_node.slotdefine.add(res,)

    # return res


# @register.tag(name="slot")
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
    nodelist, tokens, extra = parse_until(parser, token, ("endslot",))
    res = SlotNode(nodelist, tokens, **extra)
    slot_into_parent(parser, res, "slotinfo")
    return res


from django.template.base import VariableDoesNotExist


class DefineSlotNode(template.Node):
    """The slot definition, within the main wrap.html."""

    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist
        first_token = tokens[0] if len(tokens) > 0 else self.get_default_name()
        self.first_token = first_token
        self.token_slot_name = template.Variable(first_token)
        self.tokens = tokens
        self.extra_context = kw
        self.args = a
        log(
            f" _cre_ DefineSlotNode({self.first_token}), {self.tokens} {self.args} {self.extra_context}"
        )

    def get_default_name(self):
        return "default"

    def get_slot_names(self, context=None):
        """
        context required _variables_ are to be processed
        """
        v = self.token_slot_name
        if context:
            try:
                v = v.resolve(context) if hasattr(v, "resolve") else v
            except VariableDoesNotExist:
                # the given string is not a variable. It could be a
                # const type (e.g. default) or a bad var.
                # Quietly fail
                return self.first_token
        return v

    def apply_parent(self, wrap_node):
        """set the parent wrapper."""
        self.extra_context["parent_wrap"] = wrap_node

    def resolve_extra_context(self, context):
        values = {}
        for key, val in self.extra_context.items():
            values[key] = val.resolve(context) if hasattr(val, "resolve") else val
        return values

    def get_slots(self, token, context):
        ## Grab 'name' from the wrap slots.
        parent_slots = self.extra_context["parent_wrap"].token.slotinfo
        matches = parent_slots.get_nodes(token, context)
        return matches

    def render(self, context):
        ## The content should be the content from the rendered slot info
        #
        # template_name = self.token_template_name.resolve(context)
        # t = context.template.engine.get_template(template_name)
        log(f"   _ren_ DefineSlotNode: {self.first_token}")

        # content applied within the definition,
        # before the parent slot implements any changes.
        default_slot_content = self.nodelist.render(context)
        content = default_slot_content

        matches = self.get_slots(self.first_token, context)
        log(
            f' . _ren_ Found: {len(matches)} matches during slot search for "{self.first_token}"'
        )

        if len(matches) > 0:
            ## The parent has a given a slot matching this definition name.
            # The content from the slot should be stripped from the wrap render
            # and applied here; replacing the `default_slot_content`
            ks = tuple(x[0] for x in matches)
            log(f"Found matches {ks}")
            # content = f'Found matches {ks}'
            vv = self.nodelist.render(context)
            for name, node in matches:
                # pump out first detection
                return node.nodelist.render(context)
        else:
            log("No matches")
        # we extend the original context; allowing this unit to be overwitten
        # if required.
        sub_ctx = {
            # Given to the definition slot
            "slot": {"rendered_content": content}
        }

        values = self.resolve_extra_context(context)
        with context.push(**sub_ctx, **values):
            # Context({'source': content}, autoescape=context.autoescape)
            return self.nodelist.render(context)


class SlotNode(template.Node):
    """A {% slot %}{% endslot %} assigns the given content to an allocated
    location with the parent {% wrap %}. The wrap maintains `slot.define` areas
    with a matching name.

            {% wrap "foo.html "%}
                {% slot "target" %}
                    <p>Content</p>
                {% endslot %}
            {% endwrap %}

    Functionally this doesn't render its content - as that task is managed by
    the definition slot.
    """

    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist
        first_token = tokens[0] if len(tokens) > 0 else self.get_default_name()
        self.first_token = first_token
        self.token_slot_name = template.Variable(first_token)
        self.tokens = tokens
        self.extra_context = kw
        self.args = a
        log(f" _cre_ SlotNode, {self.tokens} {self.args} {self.extra_context}")

    def get_default_name(self):
        return "default"

    def get_slot_names(self, context=None):
        """
        context required _variables_ are to be processed
        """
        v = self.token_slot_name
        if context:
            try:
                v = v.resolve(context) if hasattr(v, "resolve") else v
            except VariableDoesNotExist:
                # the given string is not a variable. It could be a
                # const type (e.g. default) or a bad var.
                # Quietly fail
                return self.first_token
        return v

    def render(self, context):
        # template_name = self.token_template_name.resolve(context)
        # t = context.template.engine.get_template(template_name)
        names = self.get_slot_names(context)
        # self.default_render(self, context)
        log(f"   _ren_ SlotNode, {names}")
        return f'<div class="color-gray">cut slot {names}</div>'

    def default_render(self, context):
        content = self.nodelist.render(context)
        # we extend the original context; allowing this unit to e overbwitten
        # if required.
        wrap = {
            "content": content,
        }
        #  Dynamic key for the root context, static key for the 'wrap' object.
        content_key = "content"
        sub_ctx = {}  # = {'wrap':wrap, content_key:content}
        values = {key: val.resolve(context) for key, val in self.extra_context.items()}
        with context.push(**sub_ctx, **values):
            # Context({'source': content}, autoescape=context.autoescape)
            return self.nodelist.render(context)
