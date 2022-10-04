from django.template import Context
from django import template
from django.template.base import token_kwargs

def inject_node(parser):
    T=parser.tokens[0].__class__
    tr = "{{ slotplot }}"
    parser.prepend_token( T(parser.tokens[0].token_type, tr))

register = template.Library()

def parse_until(parser, token, ends):
    nodelist = parser.parse(ends)
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
    nodelist, splits, extra = parse_until(parser, token, ('endwrap',))
    return WrappedContentNode(nodelist, splits, **extra)


class WrappedContentNode(template.Node):
    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist
        self.token_template_name = template.Variable(tokens[0])
        self.extra_context = kw

    def render(self, context):
        print('rendering wrap')
        template_name = self.token_template_name.resolve(context)
        t = context.template.engine.get_template(template_name)
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
        values = {key: val.resolve(context) for key, val in self.extra_context.items()}
        with context.push(**sub_ctx, **values):
            # Context({'source': content}, autoescape=context.autoescape)
            return t.render(context)


@register.tag(name="slot")
def do_slot(parser, token):
    nodelist, splits, extra = parse_until(parser, token, ('endslot',))
    return SlotNode(nodelist, splits, **extra)


class SlotNode(template.Node):
    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist
        # self.token_template_name = template.Variable(tokens[0])
        self.extra_context = kw

    def render(self, context):
        # template_name = self.token_template_name.resolve(context)
        # t = context.template.engine.get_template(template_name)
        print('rendering slot')
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
