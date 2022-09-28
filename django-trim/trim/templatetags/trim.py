from django.template import Context
from django import template
from django.template.base import token_kwargs


register = template.Library()


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
    nodelist = parser.parse(('endwrap',))
    parser.delete_first_token()
    splits = token.split_contents()[1:]
    for i, word in enumerate(splits):
        if word == 'with':
            extra = token_kwargs(splits[i+1:], parser)
    return WrappedContentNode(nodelist, splits, **extra)


class WrappedContentNode(template.Node):
    def __init__(self, nodelist, tokens, *a, **kw):
        self.nodelist = nodelist
        self.token_template_name = template.Variable(tokens[0])
        self.extra_context = kw

    def render(self, context):
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


# @register.simple_tag(takes_context=True)
# def info_form(context, product_id):
#     return forms.ProductQuestionForm(initial={
#             'product_id':product_id,
#         })
#
# @register.inclusion_tag('dummy.html')
# def wrap(template='default.html'):
#     return {'template': template}
