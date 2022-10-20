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
    td = (late_time - early_time)
    return td

@register.simple_tag(takes_context=False, name='human_timedelta')
def str_timedelta_tag(late_time, early_time, *targs, **kwargs):
    td = (late_time - early_time)
    return localize_timedelta(td)


def localize_timedelta(delta):
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
