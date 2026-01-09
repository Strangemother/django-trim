"""
{% timedelta cart.updated cart.created format="" %}
{{ cart.created|timesince:cart.updated }}
{% human_timedelta cart.updated cart.created format="" %}
"""

from django import template
from pydoc import locate

register = template.Library()


@register.simple_tag(takes_context=False)
def functional(name, *args, **kwargs):
    """Dynamically call any Python function by its fully qualified name.

    This powerful template tag allows you to execute any accessible Python
    function directly from your templates by providing its module path and name.
    Uses `pydoc.locate` to find and execute the function with provided arguments.

    Args:
        name (str): Fully qualified function name (e.g., 'os.path.join', 'math.sqrt')
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Result of the function call, or empty string if function not found,
        or string representation if the located object is not callable

    Examples:
        {% load functional %}

        {# Call math functions #}
        {% functional 'math.sqrt' 16 %}
        {# Returns: 4.0 #}

        {# Call string methods #}
        {% functional 'str.upper' 'hello world' %}
        {# Returns: 'HELLO WORLD' #}

        {# Call custom module functions #}
        {% functional 'myapp.utils.format_price' product.price currency='USD' %}

        {# Call datetime functions #}
        {% functional 'datetime.datetime.now' %}

        {# Access module constants #}
        {% functional 'math.pi' %}
        {# Returns: 3.141592653589793 #}

    Security Warning:
        Use this tag with extreme caution in production environments.
        It can execute arbitrary code and poses security risks if the
        function name comes from untrusted sources. Only use with
        controlled, whitelisted function names in production.

    Note:
        If the located object is not callable (e.g., a constant or variable),
        it will be converted to a string and returned.
    """
    # Note: This is a simple tag, not a filter, so it does not take
    # the context or return a string to be rendered in the template.
    # It directly returns the result of the callable.
    _callable = locate(name)
    if not _callable:
        return ""

    if not callable(_callable):
        return str(_callable)

    return _callable(*args, **kwargs)
