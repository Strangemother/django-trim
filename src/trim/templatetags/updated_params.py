# https://blog.ovalerio.net/archives/1512
from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def updated_params(context, **kwargs):
    """Update URL query parameters while preserving existing ones.
    
    Copies all GET parameters from the current request and updates them
    with the provided keyword arguments, returning a URL-encoded query string.
    This is particularly useful for pagination, filtering, and sorting links
    where you want to maintain existing query parameters.
    
    Args:
        context: Django template context (automatically provided)
        **kwargs: Query parameters to add or update
    
    Returns:
        str: URL-encoded query string ready to use in href attributes
    
    Examples:
        {% load updated_params %}
        
        {# Basic pagination - preserves existing filters #}
        <a href="?{% updated_params page=2 %}">Next Page</a>
        
        {# Update multiple parameters #}
        <a href="?{% updated_params page=3 sort='name' order='asc' %}">Page 3</a>
        
        {# Change filter while keeping pagination #}
        <a href="?{% updated_params category='electronics' %}">Electronics</a>
    
    Reference:
        Credit to O. Valerio: https://blog.ovalerio.net/archives/1512
    """
    res = context['request'].GET.copy()
    res.update(kwargs)
    return res.urlencode()