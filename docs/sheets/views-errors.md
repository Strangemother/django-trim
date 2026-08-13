# Views: Custom 404 Handling

`trim.views.errors` provides a reusable mixin for converting `Http404` exceptions into redirects or a rendered 404 template.

## Import

```py
from trim.views.errors import Custom404, Custom404TemplateView
```

`Custom404` is also available as `trim.views.Custom404`.

## Template View

```py
class NotFoundView(Custom404TemplateView):
    template_name = "errors/404.html"
```

`Custom404TemplateView` uses status code `404`, defaults to `trim/errors/404.html`, and adds `status_code` to the template context.

## Redirect or Render a 404

Add `Custom404` before an object-based Django view:

```py
class ProductDetailView(Custom404, views.DetailView):
    model = Product
    custom_404_redirect_url = "catalog:product-list"
```

When `get_object()` raises `Http404`, the mixin redirects to the named URL. To render an alternate template instead:

```py
class ProductDetailView(Custom404, views.DetailView):
    model = Product
    custom_404_redirect = False
    custom_404_template_name = "catalog/errors/product_missing.html"
```

Configuration:

| Attribute | Default | Purpose |
| --- | --- | --- |
| `custom_404_redirect_url` | `None` | Reversible Django URL name used for redirects. |
| `custom_404_redirect` | `None` | `True` redirects; `False` renders a template. When unset, a supplied URL enables redirect mode. |
| `custom_404_template_name` | unset | Optional template override for inline 404 rendering. |

## Methods

| Method | Example | Purpose |
| --- | --- | --- |
| `dispatch` | `return super().dispatch(request, *args, **kwargs)` | Catches `Http404` from the wrapped view and routes it to `custom_404`. |
| `custom_404` | `return self.custom_404(request, *args, **kwargs)` | Chooses redirect or template behavior. |
| `custom_404_view` | `return self.custom_404_view(request, *args, **kwargs)` | Renders `Custom404TemplateView`. |
| `get_custom_404_url` | `url = self.get_custom_404_url(request, *args, **kwargs)` | Reverses the configured URL with the current route arguments. |
| `custom_404_redirect_response` | `return self.custom_404_redirect_response(url)` | Returns a Django redirect response. |

If neither a redirect URL nor `custom_404_redirect=False` is configured, the mixin raises `Missing404RedirectUrl`. This exception is available from `trim.views.errors.custom404`.
