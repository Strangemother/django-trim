# https://blog.ovalerio.net/archives/1512
from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def updated_params(context, **kwargs):
    """
        {% load updated_params %}
        https://example.ovalerio.net?{% updated_params page=2 something='else' %}

    """
    dict_ = context['request'].GET.copy()
    for k, v in kwargs.items():
        dict_[k] = v
    return dict_.urlencode()