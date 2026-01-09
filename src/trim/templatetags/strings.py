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
    """Join many separate strings into a single string

    {% str_merge "foo" var ".baz" as my_str %}
    {{ my_str }}
    """
    return "".join(map(str, targs))
