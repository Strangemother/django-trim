from django import template
from django.forms.boundfield import BoundField
from django.template import Context
from django.template.base import token_kwargs

from trim import get_model

register = template.Library()


@register.simple_tag(takes_context=True)
def stockcount_product(context, stockcount_id):
    SC = get_model("stocks.StockCount")
    if isinstance(stockcount_id, BoundField):
        stockcount_id = stockcount_id.value()

    if stockcount_id == None:
        return ""

    return SC.objects.get(id=stockcount_id).product


# @register.inclusion_tag('dummy.html')
# def wrap(template='default.html'):
#     return {'template': template}
