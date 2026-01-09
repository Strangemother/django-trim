from django import template
from django.urls import resolve, reverse


register = template.Library()

quickform_kwargs = (
    "form_submit_label",
    "form_submit_button",
)


@register.inclusion_tag(
    "trim/quickform.html", takes_context=True, name="quickform.form"
)
def quickform_template(context, view_name, *args, **kwargs):
    """Apply a quickform within a form template, utilising the quickform as
    the thing to render.

        {% quickform.form 'associations:grouping-search-form'
            form_submit_button=True
            form_submit_label='Search'
            id='quicksearchform'
        %}

    Provide a `Form` instance as the first object to render a page form.

        {% quickform.form myform %}

    any option not in `quickform_kwargs` is applied to the form a node parameter.
    """
    form = view_name
    if isinstance(view_name, str):
        form = quickform(context, view_name, *args, **kwargs)

    extra = {"opts": {}, "trim_form": {}, "multipart": kwargs.get("multipart", True)}

    if getattr(form, "action_url", None) is None:
        kwpop = kwargs.pop("action_url", None)
        if kwpop is not None:
            form.action_url = kwpop

    for x, v in kwargs.items():
        # x, y for x, y in kwargs.items() if x in quickform_kwargs
        k = ["opts", "trim_form"][bool(x in quickform_kwargs)]
        extra[k][x] = v

    return {
        "trim_quickform_form": form,
        **extra,
    }


@register.simple_tag(takes_context=True, name="quickform")
def quickform(context, view_name, *url_args, **kwargs):
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
    request = context.get("request")
    args = kwargs.get("view_args", ()) if len(url_args) == 0 else url_args

    rev = reverse(view_name, args=args)
    resolve_match = resolve(rev)
    action_url = kwargs.pop("action_url", rev)

    view = resolve_match.func.view_class
    initkwargs = resolve_match.func.view_initkwargs
    view.view_initkwargs = initkwargs

    instance = view(**initkwargs)
    instance.setup(request, *args, **kwargs)

    form = instance.get_form()
    # Mutate the form to apply the action URL.
    form.action_url = action_url

    initial = kwargs.get("initial", None) or kwargs
    if hasattr(form, "initial") and (len(initial) > 0):
        form.initial.update(initial)
    return form
