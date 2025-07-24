# https://blog.ovalerio.net/archives/1512
from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def updated_params(context, **kwargs):
    """
        {% load updated_params %}
        https://example.ovalerio.net?{% updated_params page=2 something='else' %}

    """
    res = context['request'].GET.copy()
    res.update(kwargs)
    return res.urlencode()