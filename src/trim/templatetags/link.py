from django import template
from django.urls import reverse

register = template.Library()

from ..urls import absolute_reverse, absolutify


@register.simple_tag(takes_context=False, name="link.info")
def link_info(view_name, *targs, **kwargs):
    """Return complete link information dictionary for a Django view.

    This template tag returns a ShadowDict containing 'url', 'text', and
    'kwargs' for the specified view name. Use this when you need access to
    all link properties in your template logic.

    Args:
        view_name: Django URL pattern name to reverse
        *targs: Positional arguments - URL args followed by optional link text
        **kwargs: Additional HTML attributes for the link element

    Returns:
        ShadowDict: Dictionary with 'url', 'text', and 'kwargs' keys

    Example:
        {% load link %}
        {% link.info 'home' %}
        {% link.info 'article-detail' article.pk 'Read More' class='btn' %}
    """
    return link(view_name, *targs, **kwargs)


@register.simple_tag(takes_context=False, name="link.url")
def link_url(view_name, *targs, **kwargs):
    """Return only the URL string for a Django view.

    This template tag extracts just the 'url' value from the link dictionary,
    providing a shortcut when you only need the reversed URL path without
    additional link attributes.

    Args:
        view_name: Django URL pattern name to reverse
        *targs: Positional arguments passed to Django's reverse()
        **kwargs: Additional URL parameters (not used in URL generation)

    Returns:
        str: The reversed URL path

    Example:
        {% load link %}
        <a href="{% link.url 'home' %}">Home</a>
        <a href="{% link.url 'article-detail' article.pk %}">Article</a>
    """
    return link(view_name, *targs, **kwargs)["url"]


@register.inclusion_tag("trim/link.html", takes_context=True)
def abs_link(context, link, *targs, **kwargs):
    """Generate an absolute URL link with full domain.

    Converts a relative Django URL into an absolute URL including the protocol
    and domain from the current request context. Useful for emails, external
    references, or social media sharing links.

    Args:
        context: Django template context (automatically provided)
        link: Django URL pattern name to reverse
        *targs: Positional arguments - URL args followed by optional link text
        **kwargs: Additional HTML attributes for the link element

    Returns:
        dict: Link dictionary with absolute 'url', 'text', and 'kwargs'

    Example:
        {% load link %}
        {% abs_link 'article-detail' article.pk 'Read Article' %}
        {# Generates: https://example.com/articles/123/ #}
    """
    res = gen_link(link, *targs, **kwargs)
    res["url"] = absolutify(context["request"], res["url"])
    return res


@register.inclusion_tag("trim/link.html", takes_context=False)
def link(link, *targs, **kwargs):
    """Generate an HTML link element from a Django view name or existing link dict.

    This is the primary link template tag, supporting two modes:
    1. Create a new link from a view name (passes to gen_link)
    2. Update an existing ShadowDict link with new text or attributes

    The generated link is rendered using the 'trim/link.html' template.

    Args:
        link: Django URL pattern name (str) or existing ShadowDict to update
        *targs: Positional arguments - URL args followed by optional link text
        **kwargs: Additional HTML attributes (class, id, data-*, etc.)

    Returns:
        dict: Link dictionary with 'url', 'text', and 'kwargs' for template

    Examples:
        {% load link %}
        {# Basic link #}
        {% link 'home' 'Go Home' %}

        {# Link with URL arguments #}
        {% link 'article-detail' article.pk 'Read More' %}

        {# Link with HTML attributes #}
        {% link 'profile' user.id 'Profile' class='btn btn-primary' %}

        {# Update existing link #}
        {% link existing_link 'New Text' class='updated' %}
    """
    if isinstance(link, ShadowDict):
        if len(targs) > 0:
            link["text"] = targs[0]
        link["kwargs"].update(kwargs)
        return link
    return gen_link(link, *targs, **kwargs)


@register.inclusion_tag("trim/link.html", takes_context=False)
def new_link(link, *targs, **kwargs):
    """Generate a link that opens in a new tab with security attributes.

    Creates an HTML link with target='_blank' and rel='noreferrer noopener'
    by default. This is useful for external links or links you want to open
    in a new browser tab while maintaining security best practices.

    The 'noreferrer noopener' attributes prevent the new page from accessing
    the window.opener property and protect against tabnabbing attacks.

    Args:
        link: Django URL pattern name to reverse
        *targs: Positional arguments - URL args followed by optional link text
        **kwargs: Additional HTML attributes (can override target and rel)

    Returns:
        dict: Link dictionary with 'url', 'text', and 'kwargs' including
              target='_blank' and rel='noreferrer noopener'

    Examples:
        {% load link %}
        {# External link in new tab #}
        {% new_link 'external-resource' 'View Resource' %}

        {# Link with URL arguments #}
        {% new_link 'pdf-download' doc.id 'Download PDF' %}

        {# Override default attributes #}
        {% new_link 'popup' rel='noopener' class='external' %}
    """
    kwargs.setdefault("target", "_blank")
    kwargs.setdefault("rel", "noreferrer noopener")

    return gen_link(link, *targs, **kwargs)


@register.inclusion_tag("trim/js_link.html", name="js", takes_context=False)
def script_link(link, *targs, **kwargs):
    """Build a standard `<script>` for JS, usig the static path.

        {% link.js "examples/js/my-js-file.js"  %}

    Creating a standard script tag:

        <script type="text/javascript"  src="/static/examples/js/my-js-file.js></script>

    Apply args and kwargs as required:

        {% link.js "examples/js/petite-vue.iife.js" "defer" "init" %}
        # <script src="examples/js/petite-vue.iife.js" defer init></script>

    """
    kwargs.setdefault("type", "text/javascript")
    return {
        "static_name": link,
        "kwargs": kwargs,
        "args": targs,
    }


register.inclusion_tag("trim/js_link.html", name="link.js", takes_context=False)(
    script_link
)


@register.inclusion_tag("trim/css_link.html", name="css", takes_context=False)
def css_link(link, *targs, **kwargs):
    """

    Build a standard <link> for CSS, using a static path

        {% css 'css/main.css' %}

    All attributes of the node are available. As an example of versatility
    (not recommended):

        {% css 'images/favicon.ico' rel="shortcut icon" type="image/png" %}
    """
    kwargs.setdefault("rel", "stylesheet")
    kwargs.setdefault("type", "text/css")
    return {
        "static_name": link,
        "kwargs": kwargs,
        "args": targs,
    }


register.inclusion_tag("trim/css_link.html", name="link.css", takes_context=False)(
    css_link
)


@register.inclusion_tag("trim/link.html", takes_context=False)
def new_url_link(link, *targs, **kwargs):
    """Provide a _real_ URL, rather than a reversable name:

    {% load link %}
    {% for pay_url in flow.cart.receipt_links %}
        {% new_url_link pay_url "Receipt" %}
    {% endfor %}

    """
    kwargs.setdefault("target", "_blank")
    kwargs.setdefault("rel", "noreferrer noopener")
    kwargs.setdefault("url", link)
    return gen_link(link, *targs, **kwargs)


@register.inclusion_tag("trim/link.html", takes_context=False)
def url_link(link, *targs, **kwargs):
    """Provide a _real_ URL, rather than a reversable name:

    {% load link %}
    {% for pay_url in flow.cart.receipt_links %}
        {% url_link pay_url "Receipt" %}
    {% endfor %}

    """
    # kwargs.setdefault('target', '_blank')
    # kwargs.setdefault('rel', 'noreferrer noopener')
    kwargs.setdefault("url", link)
    return gen_link(link, *targs, **kwargs)


class ShadowDict(dict):
    pass


def gen_link(link, *targs, **kwargs):
    # "...X as name %}" detection
    hotix_as_word = targs[-2:] == (
        "",
        "",
    )
    ## We cut _3_ as (1) for the _last argument (text) and 2 for 'as X'
    ## else -1 for just the _last argument_
    cutlen = -3 if hotix_as_word else -1
    # Args are exerything given except the last "text" arg (and hotfix 'as X')
    args = targs[:cutlen] if len(targs) > 0 else targs
    url = kwargs.get("url", None) or reverse(link, args=args)
    text = targs[cutlen] if len(targs) > 0 else url

    return ShadowDict(
        url=url,
        text=text,
        kwargs=kwargs,
    )
