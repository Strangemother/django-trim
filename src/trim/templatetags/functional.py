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
    """ Call a function by its name with positional and keyword arguments.
    This tag allows you to call a function dynamically by its name,
    passing any positional and keyword arguments to it.
    It uses `pydoc.locate` to find the function in the current Python environment.

    If the function cannot be found or is not callable, it returns an empty string.


    Usage:
        
        {% load functional %}   
        {% functional 'module.function_name' arg1 arg2 kwarg1=value1 %}

    Args:
        name (str): The fully qualified name of the function to call.
        *targs: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
    
    Returns:
        The result of the function call, or an empty string if the function
        could not be located or is not callable.
    
    Important 

    Use this tag with caution, as it executes arbitrary code.
    and can lead to security issues if the function name is not controlled.

    """
    # Note: This is a simple tag, not a filter, so it does not take
    # the context or return a string to be rendered in the template.
    # It directly returns the result of the callable.
    _callable = locate(name)
    if not _callable:
        return ''
    
    if not callable(_callable):
        return str(_callable)
    
    return _callable(*args, **kwargs)
    