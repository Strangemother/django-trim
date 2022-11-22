from django.urls import reverse
from django import template

register = template.Library()

from ..urls import absolute_reverse, absolutify



@register.simple_tag(takes_context=False, name='link.info')
def link_info(view_name, *targs, **kwargs):
    return link(view_name, *targs, **kwargs)


@register.inclusion_tag('trim/link.html', takes_context=True)
def abs_link(context, link, *targs, **kwargs):
    res = gen_link(link, *targs, **kwargs)
    res['url'] = absolutify(context['request'], res['url'])
    return res


@register.inclusion_tag('trim/link.html', takes_context=False)
def link(link, *targs, **kwargs):
    if isinstance(link, ShadowDict):
        if len(targs) > 0:
            link['text'] = targs[0]
        link['kwargs'].update(kwargs)
        return link
    return gen_link(link, *targs, **kwargs)


@register.inclusion_tag('trim/link.html', takes_context=False)
def new_link(link, *targs, **kwargs):
    kwargs.setdefault('target', '_blank')
    kwargs.setdefault('rel', 'noreferrer noopener')

    return gen_link(link, *targs, **kwargs)


@register.inclusion_tag('trim/js_link.html', name='js', takes_context=False)
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


class ShadowDict(dict):
    pass


def gen_link(link, *targs, **kwargs):
    # "...X as name %}" detection
    hotix_as_word = targs[-2:] == ('', '',)
    ## We cut _3_ as (1) for the _last argument (text) and 2 for 'as X'
    ## else -1 for just the _last argument_
    cutlen = -3 if hotix_as_word else -1
    # Args are exerything given except the last "text" arg (and hotfix 'as X')
    args = targs[:cutlen] if len(targs) > 0 else targs

    url = kwargs.get('url', None) or reverse(link, args=args)
    text = targs[cutlen] if len(targs) > 0 else url

    return ShadowDict(
        url=url,
        text=text,
        kwargs=kwargs,
    )

