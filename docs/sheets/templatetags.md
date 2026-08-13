# Template Tags Cheat Sheet

`trim.templatetags` provides reusable Django template tags for links, forms, time values, strings, markdown, query parameters, and composable template fragments.

## Load a Library

Django loads a template-tag module by its filename:

```django
{% load link %}
{% load quickforms %}
{% load datetime %}
```

Load multiple libraries when a template uses more than one group:

```django
{% load link quickforms updated_params %}
```

The package provides tags rather than registered filters. Django's built-in filters such as `date`, `timesince`, and `urlize` remain available separately.

## Quick Reference

| Library | Tags |
| --- | --- |
| `functional` | `functional` |
| `link` | `link`, `link.info`, `link.url`, `abs_link`, `new_link`, `new_url_link`, `url_link`, `js`, `link.js`, `css`, `link.css` |
| `quickforms` | `quickform`, `quickform.form` |
| `datetime` | `timedelta`, `human_timedelta` |
| `strings` | `str_merge` |
| `updated_params` | `updated_params` |
| `markdown` | `markdown`, `markdown.file`, `markdown.file_2`, `markdown.text` |
| `wrap` / `slot` | `wrap`, `slot`, `slot.define` |

## Link Tags

Load with:

```django
{% load link %}
```

### `link`

The primary inclusion tag. It reverses a Django URL name and renders `trim/link.html`.

```django
{% link "catalog:product-detail" product.pk "View product" class="product-link" %}
```

The tag accepts a URL name, positional URL arguments, optional link text, and HTML attributes. The final positional string is treated as the display text; if no text is supplied, the resolved URL or final URL argument is used.

```django
{% link "home" "Home" class="nav-link" aria-label="Go home" %}
```

The generated context contains `url`, `text`, and `kwargs`. Override `trim/link.html` to customize its markup.

### `link.url`

Returns only the reversed URL string:

```django
<a href="{% link.url 'catalog:product-detail' product.pk %}">
    {{ product.name }}
</a>
```

### `link.info`

Returns link data for use in template logic rather than rendering the link immediately:

```django
{% link.info "catalog:product-detail" product.pk "View" class="btn" as product_link %}
<a href="{{ product_link.url }}" class="{{ product_link.kwargs.class }}">
    {{ product_link.text }}
</a>
```

The returned mapping contains `url`, `text`, and `kwargs`.

### `abs_link`

Creates a link using an absolute URL derived from the current request:

```django
{% load link %}
{% abs_link "catalog:product-detail" product.pk "View product" %}
```

This tag requires `request` in the template context and renders through `trim/link.html`. It is useful for email or externally shared links.

### New-window and literal-URL links

| Tag | Example | Behavior |
| --- | --- | --- |
| `new_link` | `{% new_link "docs" "Documentation" %}` | Reverses a named URL and defaults to `target="_blank"` and `rel="noreferrer noopener"`. |
| `url_link` | `{% url_link download_url "Download" %}` | Uses an already-resolved URL instead of reversing a URL name. |
| `new_url_link` | `{% new_url_link download_url "Download" %}` | Uses an already-resolved URL and opens it in a new window with secure defaults. |

The `new_link` defaults protect against `window.opener` access. Explicit `target` or `rel` attributes can override them.

### CSS and JavaScript tags

```django
{% link.css "css/site.css" media="screen" %}
{% link.js "js/site.js" defer=True %}
```

The aliases `css` and `js` are also registered:

```django
{% css "css/site.css" %}
{% js "js/site.js" defer=True %}
```

`css` defaults to `rel="stylesheet"` and `type="text/css"`. `js` defaults to `type="text/javascript"`. Both resolve their `static_name` through the corresponding Trim templates.

## Quickform Tags

Load with:

```django
{% load quickforms %}
```

### `quickform`

Builds a form from a URL-resolved view with a `get_form()` method:

```django
{% quickform "catalog:product-search" as search_form %}
<form method="get" action="{{ search_form.action_url }}">
    {{ search_form.as_p }}
    <button type="submit">Search</button>
</form>
```

The tag resolves the URL, instantiates the view, calls `setup()`, and returns its form. Pass URL arguments positionally:

```django
{% quickform "catalog:product-detail" product.pk as form %}
```

Use `view_args` when arguments need to be passed as a keyword:

```django
{% quickform "catalog:product-detail" view_args=product.pk as form %}
```

Additional keyword arguments become form initial values. `action_url` overrides the form action URL.

### `quickform.form`

Renders a complete form through `trim/quickform.html`:

```django
{% quickform.form "catalog:product-search" form_submit_label="Search" %}
```

Or render an existing form instance:

```django
{% quickform.form form form_submit_button=True form_submit_label="Save" %}
```

`form_submit_label` and `form_submit_button` are treated as rendering options. Other keyword arguments are passed as form/template options. Multipart forms default to `True`; override with `multipart=False` when appropriate.

## Date and Time Tags

Load with:

```django
{% load datetime %}
```

### `timedelta`

Returns the difference between a later and earlier datetime:

```django
{% timedelta order.completed order.created as duration %}
<p>{{ duration.days }} days and {{ duration.seconds }} seconds</p>
```

The special value `now` is converted to `timezone.now()`:

```django
{% timedelta now cart.created as cart_age %}
```

### `human_timedelta`

Returns a localized, readable duration:

```django
<p>Processing time: {% human_timedelta order.shipped order.created %}</p>
```

The output includes years, days, hours, and minutes, or seconds for durations shorter than one minute. Pluralization uses Django's `ngettext`.

Both tags expect the first value to be later than the second for a positive duration.

## String Tags

Load with:

```django
{% load strings %}
```

### `str_merge`

Joins positional values after converting them to strings:

```django
{% str_merge "Order #" order.pk " - " order.status as label %}
<span>{{ label }}</span>
```

It is equivalent to joining the supplied values with an empty separator.

## Query-Parameter Tags

Load with:

```django
{% load updated_params %}
```

### `updated_params`

Copies the current request's query parameters, updates the supplied values, and returns an encoded query string:

```django
<a href="?{% updated_params page=2 %}">Next page</a>
<a href="?{% updated_params sort='name' direction='asc' %}">Sort by name</a>
```

Existing filters remain in place unless explicitly replaced. The tag requires `request` in the template context.

## Functional Tag

Load with:

```django
{% load functional %}
```

### `functional`

Locates and calls a fully qualified Python object:

```django
{% functional "math.sqrt" 16 %}
{% functional "myapp.utils.format_price" product.price currency="USD" %}
```

If the object cannot be located, it returns an empty string. If the object is not callable, it returns its string representation.

**Security warning:** this can execute arbitrary accessible Python functions. Never use a user-controlled function name. Restrict names to trusted, hard-coded or explicitly whitelisted values.

## Markdown Tags

Load with:

```django
{% load markdown %}
```

The markdown tags require the Python `markdown` package. The implementation also enables the `meta` and `pymdownx.extra` extensions when it creates a Markdown instance.

### `markdown`

Converts an inline template block to HTML:

```django
{% markdown %}
# {{ product.name }}

A **formatted** product description.
{% endmarkdown %}
```

Use `with` values to make additional context available while rendering the block:

```django
{% markdown with title=product.name %}
# {{ title }}
{% endmarkdown %}
```

### `markdown.text`

Converts supplied string arguments to rendered Markdown:

```django
{% markdown.text "# Product" "" product.description %}
```

The arguments are joined with newlines. The tag renders through `trim/templatetags/markdown_file_content.html` and returns a `markdown_object` context containing the source metadata and generated HTML.

### `markdown.file`

Loads and converts Markdown from a file:

```django
{% markdown.file "/srv/docs/readme.md" %}
{% markdown.file "docs" "guides/product.md" %}
```

Relative paths use a key from `settings.TRIM_MARKDOWN_DIRS`:

```py
TRIM_MARKDOWN_DIRS = {
    "docs": BASE_DIR / "docs",
}
```

The tag returns the same `markdown_object` context with `filepath`, `exists`, `content`, `html`, and `metadata` values. Use trusted paths and configured directories only.

### `markdown.file_2`

A lower-level include-style Markdown loader:

```django
{% markdown.file_2 "docs/readme.md" %}
{% markdown.file_2 "docs/readme.md" with title="Docs" only %}
```

It accepts `with` context values and `only` to isolate the included template context. The tag is registered under the literal name `markdown.file_2`.

## Wrap and Slot Tags

The package contains two related implementations:

- `wrap.py` registers `wrap` using `slots.wrap_node.do_wrap`.
- `slot.py` registers `slot` and `slot.define` using `slots.slot_node`.
- `trim.py` and `trim_slots.py` contain older/alternate implementations that also register `wrap` and `slot` when loaded directly.

Use the current pair in normal templates:

```django
{% load wrap slot %}
```

### `wrap`

Renders a target template around captured content:

```django
{% wrap "layouts/card.html" with object=product %}
    <h2>{{ product.name }}</h2>
    <p>{{ product.summary }}</p>
{% endwrap %}
```

The target template receives:

- `wrap.content`: rendered inner content
- `wrap.template_name`: the target template name
- `content`: the same rendered inner content
- values supplied after `with`

The wrapper template can render the content with `{{ wrap.content }}`.

### `slot.define`

Declares a replaceable area inside the wrapper template:

```django
{% load slot %}
<header>
    {% slot.define "title" %}
        <h1>Default title</h1>
    {% endslot %}
</header>
```

A `default` slot handles unnamed content:

```django
{% slot.define default %}
    <p>Default body</p>
{% endslot %}
```

### `slot`

Supplies content to a named slot when invoking the wrapper:

```django
{% load wrap slot %}
{% wrap "layouts/card.html" %}
    {% slot "title" %}
        <h1>{{ product.name }}</h1>
    {% endslot %}
    {% slot %}
        <p>Replacement body</p>
    {% endslot %}
{% endwrap %}
```

`slot` without a name targets the default slot. Slot names can be literals or template variables.

## Related Documentation

- [Form fields cheat sheet](./form-fields.md)
- [Link tags](../templates/tags/link/readme.md)
- [CSS and JavaScript tags](../templates/tags/css-js-tag.md)
- [Quickform tags](../templates/tags/quickform.md)
- [Datetime tags](../templates/tags/datetime.md)
- [Functional tag](../templates/tags/functional.md)
- [Updated parameters](../templates/tags/updated_params.md)
- [Wrap tags](../templates/tags/wrap.md)
- [Slot tags](../templates/tags/wrap-slots.md)
- [Hidden form fields](../widgets/hidden.md)
