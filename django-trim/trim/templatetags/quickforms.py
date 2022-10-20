from django import template
from django.urls import resolve, reverse


register = template.Library()


@register.simple_tag(takes_context=True, name='quickform')
def quickform(context, view_name, **kwargs):
    rev = reverse(view_name)
    vv = resolve(rev)
    form = vv.func.view_class(request=context.get('request')).get_form()
    form.action_url = rev
    form.initial = kwargs.get('initial', None) or kwargs

    return form
