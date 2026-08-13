# URL Helpers Cheat Sheet

`trim.urls` provides concise helpers for building Django `urlpatterns`, including view-to-path generation, app includes, template-only routes, absolute URL utilities, and error handler registration.

## Import

```py
from trim import urls
```

Or import individual helpers:

```py
from trim.urls import paths_named, path_include, absolute_reverse
```

A normal URL configuration can combine Trim helpers with Django's `path()` and `include()`:

```py
from django.contrib import admin
from trim import urls
from . import views

app_name = "catalog"

urlpatterns = [path("admin/", admin.site.urls)]
urlpatterns += urls.paths_named(
    views,
    list=("ProductListView", ""),
    detail=("ProductDetailView", "<int:pk>/"),
)
```

## View Pattern Builders

### `paths_named`

Uses keyword names as URL names and maps each value to a view class and URL pattern:

```py
urlpatterns = urls.paths_named(
    views,
    home=("HomeView", ""),
    detail=("ProductDetailView", "products/<int:pk>/"),
)
```

A string value uses Trim's conventional class-name mapping:

```py
urlpatterns = urls.paths_named(
    views,
    view_prefix="Product",
    list="",
    detail="<int:pk>/",
)
```

The generated classes are `ProductListView` and `ProductDetailView`; the URL names are `list` and `detail` unless a prefix is supplied.

| Argument | Default | Purpose |
| --- | --- | --- |
| `views` | required | Module containing the view classes. |
| `view_prefix` | `None` | Prefix prepended to each inferred class name. |
| `ignore_missing_views` | `False` | Skip missing view classes instead of raising `AttributeError`. |
| `url_pattern_prefix` | `None` | Prefix prepended to every URL pattern. |
| `url_name_prefix` | `None` | Prefix prepended to every URL name. |
| `**patterns` | `{}` | URL-name to `(view class, URL)` definitions. |

A view can receive multiple URL patterns by using a tuple of paths:

```py
urlpatterns = urls.paths_named(
    views,
    home=("HomeView", ("", "<str:theme>/")),
)
```

### `paths_dict`

Uses view class names as keys:

```py
patterns = {
    "ProductListView": ("list", ""),
    "ProductDetailView": ("detail", "<int:pk>/"),
    "ProductDeleteView": "delete/<int:pk>/",
}
urlpatterns = urls.paths_dict(views, patterns)
```

A compact string infers the URL name from the view's base class or class name. Reuse a definition for prefixed view stacks:

```py
base = {
    "ListView": ("list", ""),
    "DetailView": ("detail", "<int:pk>/"),
}
urlpatterns = urls.paths_dict(views, base, view_prefix="Product")
urlpatterns += urls.paths_dict(views, base, view_prefix="Customer")
```

Important arguments are `patterns`, `view_prefix`, `ignore_missing_views`, `url_pattern_prefix`, `url_name_prefix`, and `safe_prefix`. Extra keyword arguments are merged into the pattern definitions.

### `paths_tuple`

Accepts `(class_name, url_name, URL)` tuples and delegates to `paths_dict`:

```py
patterns = (
    ("HomeView", "home", ""),
    ("ProductDetailView", "product-detail", "products/<int:pk>/"),
)
urlpatterns = urls.paths_tuple(views, patterns)
```

### `paths`

Builds URL patterns from `(name, (URL, view, ...))` pairs. It converts class-based views to `as_view()` callables and leaves functions callable:

```py
urlpatterns = urls.paths(
    (
        ("home", ("", views.HomeView)),
        ("health", ("health/", health_check)),
    )
)
```

Extra mapping dictionaries are passed to a class-based view's `as_view()`:

```py
urlpatterns = urls.paths(
    (("product-list", ("products/", views.ProductListView, {"paginate_by": 25})),)
)
```

### Model CRUD Shortcuts

`paths_default` and `paths_less` generate conventional model URL stacks using `paths_named`.

```py
urlpatterns = urls.paths_default(
    views,
    [Product, Category],
    views=("list", "create", "update", "delete", "detail"),
)
```

`paths_less` accepts the patterns directly:

```py
urlpatterns = urls.paths_less(
    views,
    [Product],
    list="",
    create="new/",
    update="change/<int:pk>/",
    delete="delete/<int:pk>/",
    detail="<int:pk>/",
)
```

Each model receives a URL prefix based on its lower-case class name and URL-name prefix, such as `product/` and `product-list`.

## Template Routes

### `template_view`

Creates one `TemplateView` route without defining a view class:

```py
urlpatterns = [
    urls.template_view("about/", "pages/about.html", name="about"),
]
```

Signature:

```py
urls.template_view(url_string, html_path, name="template_view")
```

### `as_templates`

Creates several template-only routes. Each keyword becomes the URL name and each value is `(URL, template path)`:

```py
urlpatterns += urls.as_templates(
    about=("about/", "pages/about.html"),
    privacy=("privacy/", "pages/privacy.html"),
)
```

## App Includes

### `path_include`

Creates one smart `include()` route. The module and namespace are inferred when omitted:

```py
urlpatterns = [
    urls.path_include("products/"),
    urls.path_include("store/", "catalog.products.urls", "products"),
]
```

The arguments are `url_name`, `url_module=None`, and `path_name=None`. A missing trailing slash is added to the URL prefix.

### `path_includes`

Includes multiple apps using each app name as both the URL prefix and module base:

```py
urlpatterns += urls.path_includes("products", "orders", "accounts")
```

This creates `products/ -> products.urls`, `orders/ -> orders.urls`, and `accounts/ -> accounts.urls`.

### `path_includes_pair`

Supports custom module and URL pairs:

```py
urlpatterns += urls.path_includes_pair(
    "products",
    ("catalog.orders", "orders/"),
    ("trim.account", "account/"),
)
```

A string expands to `(name, f"{name}/")`; a tuple expands to `(module, URL prefix)`.

`include` is an alias for `path_includes`:

```py
urlpatterns += urls.include("products", "orders")
```

## Static and File Routes

### `favicon_path`

Creates a redirect route from a public favicon path to a static file:

```py
urlpatterns = [
    urls.favicon_path(),
    urls.favicon_path("apple-touch-icon.png", "icons/apple-touch-icon.png"),
]
```

The defaults are `ingress_path="favicon.ico"` and `static_path="images/{ingress_path}"`.

### `static_redirect_path`

The lower-level helper used by `favicon_path`:

```py
urlpatterns = [
    urls.static_redirect_path("robots.txt", "robots.txt"),
]
```

It returns a Django `path()` containing a `RedirectView` to the static-files storage URL.

## Absolute URLs

### `absolute_reverse`

Reverses a named URL and prefixes it with the current request scheme and host:

```py
from trim.urls import absolute_reverse

url = absolute_reverse(request, "catalog:product-detail", product.pk)
```

### `absolutify`

Converts a relative path into an absolute URL using the request:

```py
from trim.urls import absolutify

url = absolutify(request, product.get_absolute_url())
```

These helpers use `request.scheme` and `request.get_host()`. Apply the same host validation and proxy configuration required by your deployment before using request-derived absolute URLs in security-sensitive contexts.

## Error Handlers

### `error_handlers`

Registers handler path strings on a target URL module:

```py
# project/urls.py
from trim.urls import error_handlers

urlpatterns = [...]
error_handlers(__name__)
```

Customize selected handlers:

```py
error_handlers(
    __name__,
    setup={
        404: "catalog.views.custom_404",
        500: "catalog.views.custom_500",
    },
)
```

The default handler names are `handler400`, `handler403`, `handler404`, and `handler500`, pointing to the corresponding `trim.views.errors` paths. `template_dir` is accepted by the current function signature for compatibility, but the current implementation does not otherwise use it.

## Small Helpers and Placeholders

| Helper | Example | Purpose |
| --- | --- | --- |
| `clean_str` | `prefix = urls.clean_str(None)` | Converts `None` or `False` to `""`; otherwise returns the value unchanged. |
| `path_urls` | `result = urls.path_urls(views, relations)` | Placeholder; currently returns `None`. |
| `index` | `result = urls.index("home")` | Placeholder; currently returns `None`. |

Do not use `path_urls` or `index` as route builders until their implementations are completed.

## Related Documentation

- [URL functions reference](../urls/functions.md)
- [URL overview](../urls/readme.md)
- [Views cheat sheets](./views-overview.md)
- [Django URL dispatcher documentation](https://docs.djangoproject.com/en/stable/topics/http/urls/)

## Quick Reference

```py
from trim import urls

urlpatterns = []
urlpatterns += urls.paths_named(views, home=("HomeView", ""))
urlpatterns += urls.paths_dict(views, {"ProductListView": ("products", "products/")})
urlpatterns += urls.paths_tuple(views, (("AboutView", "about", "about/"),))
urlpatterns += urls.as_templates(privacy=("privacy/", "pages/privacy.html"))
urlpatterns += urls.path_includes("products", "orders")
urlpatterns += [urls.favicon_path()]
error_handlers = urls.error_handlers(__name__)
```
