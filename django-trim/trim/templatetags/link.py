from django.urls import reverse
from django import template

register = template.Library()

from ..urls import absolute_reverse, absolutify


@register.inclusion_tag('trim/link.html', takes_context=True)
def abs_link(context, link, *targs, **kwargs):
    res = gen_link(link, *targs, **kwargs)
    res['url'] = absolutify(context['request'], res['url'])
    return res


@register.inclusion_tag('trim/link.html', takes_context=False)
def link(link, *targs, **kwargs):
    return gen_link(link, *targs, **kwargs)


@register.inclusion_tag('trim/link.html', takes_context=False)
def new_link(link, *targs, **kwargs):
    kwargs.setdefault('target', '_blank')
    kwargs.setdefault('rel', 'noreferrer noopener')

    return gen_link(link, *targs, **kwargs)


@register.inclusion_tag('trim/css_link.html', name='js', takes_context=False)
def script_link(link, *targs, **kwargs):
    kwargs.setdefault('type', 'text/javascript')
    return {
        'static_name': link,
        'kwargs': kwargs,
    }

@register.inclusion_tag('trim/css_link.html', name='css', takes_context=False)
def css_link(link, *targs, **kwargs):
    """

    Build a standard <link> for CSS, using a static path

        {% css 'css/main.css' %}

    All attributes of the node are available. As an example of versatility
    (not recommended):

        {% css 'images/favicon.ico' rel="shortcut icon" type="image/png" %}
    """
    kwargs.setdefault('rel', 'stylesheet')
    kwargs.setdefault('type', 'text/css')
    return {
        'static_name': link,
        'kwargs': kwargs,
    }


@register.inclusion_tag('trim/link.html', takes_context=False)
def new_url_link(link, *targs, **kwargs):
    """Provide a _real_ URL, rather than a reversable name:

        {% load link %}
        {% for pay_url in flow.cart.receipt_links %}
            {% new_url_link pay_url "Receipt" %}
        {% endfor %}

    """
    kwargs.setdefault('target', '_blank')
    kwargs.setdefault('rel', 'noreferrer noopener')
    kwargs.setdefault('url', link)
    return gen_link(link, *targs, **kwargs)


def gen_link(link, *targs, **kwargs):
    args = targs[:-1] if len(targs) > 0 else targs
    url = kwargs.get('url', None) or reverse(link, args=args)
    text = targs[-1] if len(targs) > 0 else url
    return {
        'url': url,
        'text': text,
        'kwargs': kwargs,
    }

