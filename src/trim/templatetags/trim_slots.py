from collections import defaultdict

from django import template
from django.template import Context
from django.template.base import token_kwargs

from . import quickforms
from .shared_tools import parse_until

slot_space = defaultdict(dict)


def inject_node(parser):
    T = parser.tokens[0].__class__
    tr = "{{ slotplot }}"
    parser.prepend_token(T(parser.tokens[0].token_type, tr))


register = template.Library()


@register.tag(name="wrap")
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
    nodelist, splits, extra = parse_until(parser, token, ("endwrap",))
    return WrappedContentNode(nodelist, splits, **extra)


class WrappedContentNode(template.Node):
    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist
        self.token_template_name = template.Variable(tokens[0])
        self.extra_context = kw

    def render(self, context):
        print(" rendering wrap", self)
        template_name = self.token_template_name.resolve(context)
        print("   Template name:", template_name)
        t = context.template.engine.get_template(template_name)
        ## The users given content.
        sub_ctx = {
            "wrap_key": id(self),
            "wrap_render_mode": "fragment",
        }
        with context.push(**sub_ctx):
            content = self.nodelist.render(context)

        # we extend the original context; allowing this unit to be overwitten
        # if required.
        wrap = {"content": content, "template_name": template_name}
        #  Dynamic key for the root context, static key for the 'wrap' object.
        content_key = "content"
        sub_ctx = {
            "wrap": wrap,
            content_key: content,
            # 'wrapper': context.setdefault('wrapper'),
            "wrap_render_mode": "render",
            "wrap_key": id(self),
        }

        values = {key: val.resolve(context) for key, val in self.extra_context.items()}
        with context.push(**sub_ctx, **values):
            print("    Rendering Wrapper content")
            # Context({'source': content}, autoescape=context.autoescape)
            return t.render(context)


@register.tag(name="slot")
def do_slot(parser, token):
    nodelist, splits, extra = parse_until(parser, token, ("endslot",))
    return SlotNode(nodelist, splits, **extra)


class SlotNode(template.Node):
    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist
        self.slot_name = template.Variable(tokens[0]) if len(tokens) > 0 else "noname"
        self.extra_context = kw

    def render(self, context):
        # template_name = self.token_template_name.resolve(context)
        # t = context.template.engine.get_template(template_name)
        wrm = context.get("wrap_render_mode", None)
        # wrapper = context.get('wrapper', None)
        kl = context.get("wrap_key")
        print(" rendering slot in mode:", wrm, kl)
        return getattr(self, f"render_mode_{wrm}")(context)

    def render_mode_render(self, context):
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
        kl = context.get("wrap_key")
        with context.push(**sub_ctx, **values):
            #     # Context({'source': content}, autoescape=context.autoescape)
            #     return self.nodelist.render(context)
            nodelist_render = slot_space.get(kl, None)
            if nodelist_render:
                slotname = self.slot_name  # .resolve(context)
                return nodelist_render[slotname](context)
            else:
                # Apply slot default.
                return f"'no data for {kl}'"

    def render_mode_fragment(self, context):
        """In fragment mode the content is parsed from the wrap target. Capture
        the slots for later render by a wrapper.
        """
        content = self.nodelist.render(context)
        sub_ctx = {}

        kl = context.get("wrap_key")
        # In this case we don't render,instead capture under the wrapr name

        values = {key: val.resolve(context) for key, val in self.extra_context.items()}
        with context.push(**sub_ctx, **values):
            res = self.nodelist.render
            slot_space[context["wrap_key"]][self.slot_name or "no_slot_name"] = res
            # slot_space[context['wrap_key']]['default'] = content

        # slot_space[context['wrap_key']] = res
        return str(context["wrap_key"])


# @register.simple_tag(takes_context=True)
# def info_form(context, product_id):
#     return forms.ProductQuestionForm(initial={
#             'product_id':product_id,
#         })
#
# @register.inclusion_tag('dummy.html')
# def wrap(template='default.html'):
#     return {'template': template}
