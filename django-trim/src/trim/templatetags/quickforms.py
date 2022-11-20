from django import template
from django.urls import resolve, reverse


register = template.Library()

quickform_kwargs = ('form_submit_label', 'form_submit_button', )

@register.inclusion_tag('trim/quickform.html', takes_context=True, name='quickform.form')
def quickform_template(context, view_name, **kwargs):
    """Apply a quickform within a form template, utilising the quickform as
    the thing to render.

        {% quickform.form 'associations:grouping-search-form'
            form_submit_button=True
            form_submit_label='Search'
            id='quicksearchform'
        %}

    any option not in `quickform_kwargs` is applied to the form a node parameter.
    """
    form = quickform(context, view_name, **kwargs)
    extra = { 'opts': {}, 'trim_form': {}}

    for x,v in kwargs.items():
        # x, y for x, y in kwargs.items() if x in quickform_kwargs
        k = ['opts', 'trim_form'][bool(x in quickform_kwargs)]
        extra[k][x] = v

    return {
        'trim_quickform_form': form,
        **extra,
    }


@register.simple_tag(takes_context=True, name='quickform')
def quickform(context, view_name, **kwargs):
    """Build a form given the view_name and any `view_arguments`

        {% quickform 'associations:grouping-search-form' as grouping_search_form %}
        <form id='grouping_search_form'
            method='post'
            action='{{ grouping_search_form.action_url }}'>
            {{ grouping_search_form.as_ul }}
            {% csrf_token %}
            <button type='submit'>Submit</button>
        </form>

    """
    args = kwargs.get('view_args', ())
    rev = reverse(view_name, args=args)
    vv = resolve(rev)
    form = vv.func.view_class(request=context.get('request')).get_form()
    form.action_url = rev
    form.initial = kwargs.get('initial', None) or kwargs

    return form
