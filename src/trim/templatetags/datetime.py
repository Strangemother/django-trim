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



@register.simple_tag(takes_context=False, name='timedelta')
def timedelta_tag(late_time, early_time, *targs, **kwargs):
    """Calculate the time difference between two datetime objects.
    
    Returns a Python timedelta object representing the duration between
    two datetime values. This is useful for time-based calculations and
    comparisons in templates.
    
    Args:
        late_time: Later datetime object (end time)
        early_time: Earlier datetime object (start time)
        *targs: Additional positional arguments (unused)
        **kwargs: Additional keyword arguments (unused)
    
    Returns:
        timedelta: Time difference between late_time and early_time
    
    Examples:
        {% load datetime %}
        
        {# Basic usage #}
        {% timedelta order.completed order.created %}
        {# Output: datetime.timedelta object (e.g., 2 days, 3:45:12) #}
        
        {# Use in comparisons #}
        {% timedelta cart.updated cart.created as duration %}
        {% if duration.days > 7 %}
            <p>Cart is over a week old!</p>
        {% endif %}
        
        {# Access timedelta properties #}
        {% timedelta event.end event.start as duration %}
        <p>Duration: {{ duration.days }} days, {{ duration.seconds }} seconds</p>
    """
    td = (late_time - early_time)
    return td

@register.simple_tag(takes_context=False, name='human_timedelta')
def str_timedelta_tag(late_time, early_time, *targs, **kwargs):
    """Calculate time difference and format it in human-readable text.
    
    Returns a localized, human-friendly string representation of the time
    difference between two datetime objects. Automatically handles years,
    days, hours, minutes, and seconds with proper pluralization.
    
    Args:
        late_time: Later datetime object (end time)
        early_time: Earlier datetime object (start time)
        *targs: Additional positional arguments (unused)
        **kwargs: Additional keyword arguments (unused)
    
    Returns:
        str: Human-readable time difference (e.g., "2 days 3 hours 45 minutes")
    
    Examples:
        {% load datetime %}
        
        {# Basic usage #}
        {% human_timedelta order.completed order.created %}
        {# Output: "2 days 3 hours 15 minutes" #}
        
        {# Show how long ago something was updated #}
        <p>Last updated: {% human_timedelta now cart.updated %} ago</p>
        {# Output: "Last updated: 3 hours 22 minutes ago" #}
        
        {# Display order processing time #}
        <div class="order-info">
            <span>Processing time: {% human_timedelta order.shipped order.created %}</span>
        </div>
        {# Output: "Processing time: 1 day 6 hours 30 minutes" #}
        
        {# Compare with Django's timesince filter #}
        <p>Django's timesince: {{ cart.created|timesince:cart.updated }}</p>
        <p>Trim's human_timedelta: {% human_timedelta cart.updated cart.created %}</p>
    """
    td = (late_time - early_time)
    return localize_timedelta(td)


def localize_timedelta(delta):
    """Convert a timedelta object to a human-readable localized string.
    
    Breaks down a timedelta into years, days, hours, and minutes (or seconds
    if less than a minute), formatting each component with proper pluralization
    using Django's ngettext for internationalization support.
    
    Args:
        delta (timedelta): Time duration to format
    
    Returns:
        str: Formatted string with space-separated time components
             (e.g., "1 year 2 days 3 hours 15 minutes")
    
    Note:
        - Years are approximated as 365 days (does not account for leap years)
        - Shows minutes if duration >= 1 minute, otherwise shows seconds
        - All components use proper singular/plural forms via ngettext
        - Automatically localizes based on Django's language settings
    
    Examples:
        >>> from datetime import timedelta
        >>> localize_timedelta(timedelta(days=400, seconds=7320))
        '1 year 35 days 2 hours 2 minutes'
        
        >>> localize_timedelta(timedelta(seconds=45))
        '45 seconds'
        
        >>> localize_timedelta(timedelta(days=1, hours=2, minutes=30))
        '1 day 2 hours 30 minutes'
    """
    ret = []
    num_years = int(delta.days / 365)
    if num_years > 0:
        delta -= timedelta(days=num_years * 365)
        ret.append(ngettext('%d year', '%d years', num_years) % num_years)

    if delta.days > 0:
        ret.append(ngettext('%d day', '%d days', delta.days) % delta.days)

    num_hours = int(delta.seconds / 3600)
    if num_hours > 0:
        delta -= timedelta(hours=num_hours)
        ret.append(ngettext('%d hour', '%d hours', num_hours) % num_hours)

    seconds= delta.seconds
    num_minutes = int(seconds / 60)
    if num_minutes > 0:
        ret.append(ngettext('%d minute', '%d minutes', num_minutes) % num_minutes)
    else:
        ret.append(ngettext('%d second', '%d seconds', seconds) % seconds)
    return ' '.join(ret)
