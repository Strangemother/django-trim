from django import template
from django.template.base import token_kwargs
from loguru import logger

from .base import SlotList, parse_until
from .slot_node import DefineSlotNode, SlotNode

log = logger.debug
warn = logger.warning


def do_wrap(parser, token):
    """Wrap the contents given to the nodem with another template given through
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
    log("   _def_ do wrap")

    slotinfo = SlotList()
    slotdefine = SlotList()

    token.slotinfo = slotinfo
    token.slotdefine = slotdefine

    nodelist, splits, extra = parse_until(parser, token, ("endwrap",))

    res = WrappedContentNode(nodelist, splits, **extra)
    # res.slotinfo = slotinfo
    # res.slotdefine = slotdefine

    return res


class WrappedContentNode(template.Node):
    slotinfo = None
    slotdefine = None

    def __init__(self, nodelist, tokens, *a, **kw):
        log("  _cre_ __init__ wrap")
        self.nodelist = nodelist
        self.tokens = tokens
        self.token_template_name = template.Variable(tokens[0])
        self.extra_context = kw

    def announce_wrapper(self, wrap_templ):
        # wrap_templ.compile_nodelist()
        nodes = wrap_templ.nodelist
        res = ()
        # Iterate through the {% slots.define %} within the wrap template
        # Each node is given _this_ parent instance, allowing the DefineSlotNode
        # to read this _parent_wrap_ when generating its content.
        for node in nodes:
            if isinstance(node, DefineSlotNode):
                log(f" ! Found {type(node).__name__} slot {node.token_slot_name}")
                node.apply_parent(self)
                res += (node,)

        return res

    def render(self, context):
        slots = self.token.slotinfo

        log(f"\n\n\n    _ren_ Wrap node rendering template with: {slots}")
        ## The name supplied to the wrap object. {% wrap "name.html" %}
        ### Note (bug(: This doesn't work with relative paths.
        template_name = self.token_template_name.resolve(context)

        ## The target {% wrap name %} template - containing slots and the _result_.
        wrap_templ = context.template.engine.get_template(template_name)
        define_slots = self.announce_wrapper(wrap_templ)

        if len(define_slots) == 0:
            log(" - rendering standard...")
            # No slot.define, generic render can proceed.
            return self.standard_render(context, wrap_templ)
        log(f"Rendering with wrap slots: {define_slots}")
        return self.slot_render(
            context, wrap_templ, define_slots, template_name=template_name
        )

    def slot_render(self, context, wrap_templ, define_slots, **extras):
        # slotdefine = self.token.slotdefine

        ## We set any recently discovered (through the announce), slot.define
        # within the template. This is done within the render, as the wrap
        # template has only just instansiated, and the DefineSlotNodes hadn't
        # a chance in the past to declare themselves to the wrap.
        self.token.slotdefine.set(define_slots)

        self.populate_lost_content_slot(context, self.nodelist)
        return self.standard_render(context, wrap_templ)

    def filter_not(self, nodes, types):
        # Discover any nodes within this wrap - of which is not a slot type.
        # Strip these, as they should be pushed into the default, lost
        # area.
        # If there are no slots defined, the content is rendered as standard
        lost_nodes = ()
        for item in nodes:
            if isinstance(item, types):
                continue
            # found lost node.
            lost_nodes += (item,)
        return lost_nodes

    def populate_lost_content_slot(self, context, nodes):
        ## slots named "lost" in the define list.

        slotdefine = self.token.slotdefine
        slot_types = (
            DefineSlotNode,
            SlotNode,
        )
        lost_nodes = self.filter_not(nodes, slot_types)

        log(f"Found {len(lost_nodes)} lost nodes (without a wrap slot)")

        slotinfo = self.token.slotinfo

        target_slotname = "lost"
        if len(slotinfo) == 0:
            ## If the input slotcount is 0, everything into default.
            # If the output slots is 1, then it can only be that one slot.
            #
            # however, as _no-slots_ in, should perhaps  _not_ go to
            # slot "other-content" by accident.
            #
            # So _default_ (if exists) for unslotted content,
            # then _lost_ if no _default_,
            # fail if no _lost_ or _default_
            # (the slot.define are named or no define slots exist.)
            target_slotname = "default"

        target_slotdefs = slotdefine.get_nodes(target_slotname, context)

        log(f"Found {len(target_slotdefs)} slot.define for: {target_slotname}")

        ## if the target was missing, then the default or lost is not available.
        # As such if we tested 'default', finally test lost. Else quit.
        if len(target_slotdefs) == 0 and target_slotname == "default":
            log(f"No target '{target_slotname}', using _lost_.")
            target_slotname = "lost"
            target_slotdefs = slotdefine.get_nodes(target_slotname, context)

        if len(target_slotdefs) == 0:
            # No lost slot. Change the definition to another;
            warn(f"No define slots for _lost_ or _default_ - this is truly lost data.")
            return

        return
        # BUG: The lost slots are stacked into this for every request.
        # Likely due to this _add_ during the render phase.
        # And the SlotList is _sticky_ to the token, not this (fresh) Node.

        # The lost_nodes is a tuple, we need a NodeList type for the
        # newly generated info slot; lost
        NL = type(nodes)
        # Iterate all `slot.define lost` - Generally only one would exist.
        for name, unit in target_slotdefs:
            # push the lost content into the slotinfo, using the same name
            # as the _unit_, therefore the _lost_ or _default_ `slot.define`
            # render exactly like a named slot.
            simulated_lost_slot = SlotNode(NL(lost_nodes), unit.tokens)
            ## Once applied, the next render sequence captures this
            #'slotinfo' stack similar to a named slot.

            # BUG: The lost slots are stacked into this for every request.
            # Likely due to this _add_ during the render phase.
            # And the SlotList is _sticky_ to the token, not this (fresh) Node.
            slotinfo.add(simulated_lost_slot)

    def standard_render(self, context, wrap_templ, **extras):
        """Render the wrapper template, using the finalised self.nodelist

        At this point for a slotted template, the slot information
        has been shuffled into the correct nodes, or the node within the nodelist
        (such as a SlotNode) has been populated with the correct assets.

        """
        ## Render this {% wrap %}
        content = self.nodelist.render(context)

        sub_ctx = {
            "wrap": {
                "content": content,
                **extras,
            },
            "content": content,
        }

        values = {}
        for key, val in self.extra_context.items():
            values[key] = val.resolve(context) if hasattr(val, "resolve") else val

        with context.push(**sub_ctx, **values):
            return wrap_templ.render(context)
