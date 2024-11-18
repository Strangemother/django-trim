# Themes

> [!NOTE]
> Implemented! This can be found under the template themes.

A basic theme acts like the `{% extends "filename.html" %}`, but the name of the file is pre-written in the theming module:

    {% theme "detail" %}

Loading themes is automatic through the `theming.py` of any app.
The file contains a dict loadout for new themes and overrides.

```py
from trim.theming import install, name_default_redirect

SITE_THEMES = {
    # 'detail': '/foo/name.html',
    # 'egg': '/foo/name.html',
    'code': 'code.html',
    'footer': "/products/sub/footer.html",
    'header': "/products/sub/header.html",
}

# Install any overrides and new keys
SCOPE = install(SITE_THEMES)
```

_redirect_ a default template, such as "detail" to a new template in a global fashion:

_theming.py_

```py
name_default_redirect('detail', 'double', 'detail-double-header.html',)
```

This results in a site-wide redirection of `detail`

    {% theme "detail" %} # is redirected to:
    {% theme "detail" "double" %}

The default exists:

    {% theme "detail" "default" %}

## Theme type stacking.

A sub module may install its own theme, but reference backward if the target theme is not used:

Classical:

    {% extends 'appname/model/list.html' %}

Theming (current):

    {% theme "list" %}

with setup:

```py
from trim.theming import install
install({ 'list':'appname/model/list.html' })
```

---

The preposed will allow sub referencing:

    {% theme "appname.list" %}

If `appname.list` does not exist is should fallback to `list`

    {% theme "list" %}

**Why not {% theme "model.list" %}**

In this case, it's assumed the _list_ page is the rendering page:

_[root]/products/templates/products/genericproduct_list.html_

```html
{% theme "list" with title="product list" %}
```

Therefore the appname (`products`) defines the generic theme handler for the sub apps.

```html
{% theme "list" with title="product list" %} # Current

{% theme "products.genericproduct.list" %} # not recommended
{% theme "genericproduct.list" %} # not recommended

{% theme "products.list" %} # good
{% theme "products" "list" %} # alternative
```

If `products.list` is not installed, it can default back to another e.g. `list`.

```py
## Historical for example:
name_default_redirect('list', 'double', 'list-double-header.html',)


# Add our redirect No bound template
name_upward_redirect('list', 'product')
```

```
{% theme "products" "list" %}
```

1. Look for `products.list`
2. fallback to `list`
3. This is redirected to `list.double`

inheritence chain

    products/genericproduct_list.html
        themes/list-double-header.html
            themes/list.html
                themes/page.html
                    base.html

If the product page is created, the waiting pages will bind to the new theming position

    products/genericproduct_list.html
        products/list.html
            themes/list.html
                themes/page.html
                    base.html

---

Therefore a user can install a template override with:

```py
name_default_redirect('products.list', 'double', 'list-double-header.html',)
```
