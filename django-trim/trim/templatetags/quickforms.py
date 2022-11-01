from django import template
from django.urls import resolve, reverse


register = template.Library()


@register.simple_tag(takes_context=True, name='quickform')
def quickform(context, view_name, **kwargs):
    """
        {% if request.session.pick_form.name %}
            {% with pf=request.session.pick_form %}
                {{ request.session.pick_form.url }}
                {% quickform pf.name view_args=pf.name_args %}
            {% endwith %}
        {% endif %}
    """
    args = kwargs.get('view_args', ())
    rev = reverse(view_name, args=args)
    vv = resolve(rev)
    form = vv.func.view_class(request=context.get('request')).get_form()
    form.action_url = rev
    form.initial = kwargs.get('initial', None) or kwargs

    return form
