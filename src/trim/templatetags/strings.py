"""
   {% timedelta cart.updated cart.created format="" %}
   {{ cart.created|timesince:cart.updated }}
   {% human_timedelta cart.updated cart.created format="" %}
"""
from django import template
from datetime import timedelta
from django.urls import reverse
from django.utils.translation import ngettext

register = template.Library()



@register.simple_tag(takes_context=False)
def str_merge(*targs, **kwargs):
    return ''.join(map(str, targs))
