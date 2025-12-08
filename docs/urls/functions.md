
# URL Helper Functions

Utility functions for simplifying common URL patterns and operations in Django. These helpers reduce boilerplate and make URL configuration more expressive.

## Table of Contents

+ [paths_named](#paths_named) - Pattern generation using view names as keywords
+ [paths_dict](#paths_dict) - Pattern generation using class names as keys
+ [paths_tuple](#paths_tuple) - Pattern generation from tuple definitions
+ [template_view](#template_view) - Instant template-only views
+ [as_templates](#as_templates) - Multiple template views at once
+ [path_include](#path_include) - Smart app URL includes
+ [path_includes](#path_includes) - Multiple app includes
+ [path_includes_pair](#path_includes_pair) - Paired module/URL includes
+ [favicon_path](#favicon_path) - Static favicon redirect
+ [absolute_reverse](#absolute_reverse) - Full URL from view name
+ [absolutify](#absolutify) - Convert relative to absolute URLs
+ [error_handlers](#error_handlers) - Custom error page setup

---

## paths_named

Generate URL patterns using the **view name** as the keyword. Most flexible for custom naming.

### Basic Usage

```py
from trim import urls
from . import views

app_name = 'myapp'

urlpatterns = urls.paths_named(views,
    # {% url 'myapp:home' %}
    home=('HomeView', ''),
    # {% url 'myapp:about' %}
    about=('AboutView', 'about/'),
    # {% url 'myapp:contact' %}
    contact=('ContactView', 'contact/'),
)
```

### Function Signature

```py
paths_named(views, view_prefix=None, ignore_missing_views=False, 
            url_pattern_prefix=None, url_name_prefix=None, **patterns)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `views` | `module` | Required | Views module containing view classes |
| `view_prefix` | `str` | `None` | Prefix to prepend to view class names |
| `ignore_missing_views` | `bool` | `False` | Skip missing views instead of raising errors |
| `url_pattern_prefix` | `str` | `None` | Prefix for all URL patterns |
| `url_name_prefix` | `str` | `None` | Prefix for all URL names |
| `**patterns` | `dict` | `{}` | Pattern definitions |

### Multiple URLs per View

Assign multiple URL patterns to a single view by using a tuple of URLs:

```py
urlpatterns = urls.paths_named(views,
    home=('HomeView', ('/', '<str:theme>/')),  # Two URLs, one view
    product=('ProductDetailView', 'product/<int:pk>/'),
)
```

### With Prefixes

Use prefixes to organize URL patterns systematically:

```py
urlpatterns = urls.paths_named(views,
    view_prefix='Product',  # Looks for ProductListView, ProductDetailView
    url_pattern_prefix='products/',  # All URLs start with 'products/'
    url_name_prefix='product-',  # Names: 'product-list', 'product-detail'
    
    list=('ListView', ''),
    detail=('DetailView', '<int:pk>/'),
    create=('CreateView', 'new/'),
)
```

Generates:
- `products/` → `ProductListView` (name: `product-list`)
- `products/<int:pk>/` → `ProductDetailView` (name: `product-detail`)
- `products/new/` → `ProductCreateView` (name: `product-create`)

### Shorthand Pattern Syntax

If you only provide a URL string (not a tuple), `paths_named` automatically infers the view class name:

```py
urlpatterns = urls.paths_named(views,
    view_prefix='Product',
    
    list='',  # Automatically uses ProductListView
    detail='<int:pk>/',  # Automatically uses ProductDetailView
)
```

---

## paths_dict

Generate URL patterns using **class names** as dictionary keys. Ideal for explicit class-to-pattern mapping.

### Basic Usage

```py
from trim import urls
from . import views

trim_patterns = {
    'ProductListView': ('list', ''),
    'ProductDetailView': ('detail', '<int:pk>/'),
    'ProductCreateView': ('create', 'new/'),
}

urlpatterns = urls.paths_dict(views, trim_patterns)
```

### Function Signature

```py
paths_dict(views, patterns=None, view_prefix=None, ignore_missing_views=False,
           url_pattern_prefix=None, url_name_prefix=None, safe_prefix=False)
```

### Compact Syntax

Omit the name to use a sensible default:

```py
trim_patterns = {
    'ProductListView': '',  # name inferred as 'productlistview'
    'ProductCreateView': ('create', 'new/'),
    'ProductDeleteView': 'delete/<int:pk>/',
}

urlpatterns = urls.paths_dict(views, trim_patterns)
```

### Using view_prefix

Reuse the same pattern definition for multiple model views:

```py
base_patterns = {
    'ListView': ('list', ''),
    'DetailView': ('detail', '<int:pk>/'),
    'CreateView': ('create', 'new/'),
    'UpdateView': ('update', '<int:pk>/edit/'),
}

urlpatterns = (
    urls.paths_dict(views, base_patterns, view_prefix='Product') +
    urls.paths_dict(views, base_patterns, view_prefix='Customer')
)
```

Generates:
- `ProductListView`, `ProductDetailView`, etc.
- `CustomerListView`, `CustomerDetailView`, etc.

---

## paths_tuple

Generate patterns from a tuple of tuples. More compact for sequential definitions.

### Basic Usage

```py
from trim import urls
from . import views

trim_patterns = (
    ('HomeView', 'home', ''),
    ('AboutView', 'about', 'about/'),
    ('ContactView', 'contact', 'contact/'),
    ('ProductDetailView', 'product-detail', 'products/<int:pk>/'),
)

urlpatterns = urls.paths_tuple(views, trim_patterns)
```

### Tuple Format

Each tuple is: `(ClassName, name, url)`

```py
trim_patterns = (
    ('NoteIndexView', 'index', ''),
    ('EntryJsonList', 'entry-list-json', 'entry/list/json/'),
    ('EntryDetailView', 'entry-detail', '<str:pk>/json/'),
)

urlpatterns = urls.paths_tuple(views, trim_patterns)
```

### Equivalent to paths_dict

`paths_tuple` converts tuples to a dictionary and calls `paths_dict`:

```py
# These are equivalent:
urlpatterns = urls.paths_tuple(views, (
    ('HomeView', 'home', ''),
))

urlpatterns = urls.paths_dict(views, {
    'HomeView': ('home', ''),
})
```

---

## template_view

Create a single template-only view without a custom view class.

### Basic Usage

```py
from trim import urls

urlpatterns = [
    urls.template_view('about/', 'pages/about.html'),
    urls.template_view('privacy/', 'pages/privacy.html', name='privacy'),
]
```

### Function Signature

```py
template_view(url_string, html_path, name='template_view')
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url_string` | `str` | Required | URL pattern |
| `html_path` | `str` | Required | Path to template file |
| `name` | `str` | `'template_view'` | URL name for reversing |

### Example

```py
urlpatterns += [
    urls.template_view('mockup/', 'mockup/crystal-geometries.html', name='mockup-geoms'),
]
```

Equivalent to:
```py
from django.views.generic import TemplateView

urlpatterns += [
    path('mockup/', TemplateView.as_view(template_name='mockup/crystal-geometries.html'), 
         name='mockup-geoms'),
]
```

---

## as_templates

Create multiple template-only views at once using keyword arguments.

### Basic Usage

```py
from trim import urls

urlpatterns += urls.as_templates(
    about=('about/', 'pages/about.html'),
    contact=('contact/', 'pages/contact.html'),
    privacy=('privacy/', 'legal/privacy.html'),
)
```

### Function Signature

```py
as_templates(**props)
```

Each keyword becomes the URL name, and its value is a tuple of `(url, template_path)`.

### Example: Mockup Pages

```py
urlpatterns += urls.as_templates(
    geoms_mockup=('mockup/geometries/', 'mockup/crystal-geometries.html'),
    materials_mockup=('mockup/materials/', 'mockup/meta-state-materials.html'),
    dashboard_mockup=('mockup/dashboard/', 'mockup/admin-dashboard.html'),
)
```

Access via:
```django
{% url 'geoms_mockup' %}
{% url 'materials_mockup' %}
```

---

## path_include

Smart Django `include()` with automatic inference. Simplifies app URL inclusion.

### Basic Usage

```py
from trim.urls import path_include

# Minimal: infers module and name from URL
urlpatterns = [
    path_include('products/'),  # Includes products.urls, name='products'
]
```

### Function Signature

```py
path_include(url_name, url_module=None, path_name=None)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url_name` | `str` | Required | URL prefix (e.g., `'products/'`) |
| `url_module` | `str` | `None` | Module path (e.g., `'products.urls'`) |
| `path_name` | `str` | `None` | URL name for namespace |

### Inference Examples

```py
# All these work:
path_include('products/')
# → include('products.urls'), name='products'

path_include('store/', 'products.urls')
# → include('products.urls'), name='store'

path_include('store/', 'products.urls', 'shop')
# → include('products.urls'), name='shop'

path_include('products/', 'myapp.products.urls', 'products')
# → include('myapp.products.urls'), name='products'
```

### Full Example

```py
from django.contrib import admin
from trim.urls import path_include, error_handlers

app_name = 'shoppinglist'

urlpatterns = [
    path('admin/', admin.site.urls),
    path_include('products/'),
    path_include('cart/'),
    path_include('checkout/'),
]

error_handlers(__name__)
```

---

## path_includes

Include multiple apps at once. Each app name becomes `{app}/` URL pattern.

### Basic Usage

```py
from trim.urls import path_includes

urlpatterns = [
    path("admin/", admin.site.urls),
] + path_includes('products', 'cart', 'checkout')
```

### Function Signature

```py
path_includes(*names)
```

Generates:
- `products/` → includes `products.urls`
- `cart/` → includes `cart.urls`
- `checkout/` → includes `checkout.urls`

### Example

```py
from django.contrib import admin
from trim.urls import path_includes, error_handlers

app_name = 'store'

urlpatterns = [
    path('admin/', admin.site.urls),
] + path_includes(
    'products',
    'categories',
    'orders',
    'customers',
)

error_handlers(__name__)
```

---

## path_includes_pair

Include apps with custom URL prefixes. Allows `(module, url)` tuple pairing.

### Basic Usage

```py
from trim.urls import path_includes_pair

urlpatterns = [
    path("admin/", admin.site.urls),
] + path_includes_pair(
    'products',  # products/ → products.urls
    ('cart', 'shopping-cart/'),  # shopping-cart/ → cart.urls
    ('trim.account', 'account/'),  # account/ → trim.account.urls
)
```

### Function Signature

```py
path_includes_pair(*items)
```

Each item can be:
- A string: `'app'` → `app/` includes `app.urls`
- A tuple: `('module', 'url/')` → `url/` includes `module.urls`

### Example

```py
from trim.urls import path_includes_pair as includes

urlpatterns = [
    path("django-admin/", admin.site.urls),
] + includes(
    'file',  # file/ → file.urls
    'uploads',  # uploads/ → uploads.urls
    ('trim.account', 'accounts/'),  # accounts/ → trim.account.urls
    ('myapp.blog', 'blog/'),  # blog/ → myapp.blog.urls
)
```

---

## favicon_path

Create a static file redirect for your favicon.

### Basic Usage

```py
from trim.urls import favicon_path

urlpatterns = [
    # ...
    favicon_path('favicon.ico'),
]
```

### Function Signature

```py
favicon_path(ingress_path='favicon.ico', static_path='images/{ingress_path}')
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ingress_path` | `str` | `'favicon.ico'` | URL path to intercept |
| `static_path` | `str` | `'images/{ingress_path}'` | Static file path |

### Custom Static Path

```py
urlpatterns = [
    favicon_path('favicon.ico', 'icons/favicon.ico'),
    favicon_path('apple-touch-icon.png', 'icons/apple-touch-icon.png'),
]
```

Under the hood, creates a `RedirectView` to `staticfiles_storage.url()`.

---

## absolute_reverse

Reverse a URL name and return the **full absolute URL** (including scheme and domain).

### Basic Usage

```py
from trim.urls import absolute_reverse

def my_view(request):
    full_url = absolute_reverse(request, 'myapp:product-detail', product.pk)
    # Returns: 'https://example.com/products/42/'
    return JsonResponse({'url': full_url})
```

### Function Signature

```py
absolute_reverse(request, name, *args)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | `HttpRequest` | Django request object |
| `name` | `str` | URL name to reverse |
| `*args` | `any` | Arguments for URL pattern |

### Example: Email Links

```py
from trim.urls import absolute_reverse

def send_reset_email(request, user):
    reset_url = absolute_reverse(request, 'account:password-reset', user.token)
    # reset_url = 'https://example.com/account/reset/abc123/'
    
    send_mail(
        'Password Reset',
        f'Click here: {reset_url}',
        'noreply@example.com',
        [user.email],
    )
```

---

## absolutify

Convert a relative path to an absolute URL using the request context.

### Basic Usage

```py
from trim.urls import absolutify

def my_view(request):
    full_url = absolutify(request, '/products/42/')
    # Returns: 'https://example.com/products/42/'
    return JsonResponse({'url': full_url})
```

### Function Signature

```py
absolutify(request, path)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | `HttpRequest` | Django request object |
| `path` | `str` | Relative or absolute path |

### Example: API Responses

```py
from trim.urls import absolutify

class ProductListJsonView(JsonListView):
    model = Product
    
    def serialize_result(self, result):
        return [
            {
                'id': product.id,
                'name': product.name,
                'url': absolutify(self.request, product.get_absolute_url()),
            }
            for product in result
        ]
```

---

## error_handlers

Set up custom error page handlers for 400, 403, 404, and 500 errors.

### Basic Usage

```py
from trim.urls import error_handlers

app_name = 'myapp'

urlpatterns = [
    # ... your patterns
]

error_handlers(__name__)  # Sets up default error handlers
```

### Function Signature

```py
error_handlers(name, setup=None, template_dir=None)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | Required | Module name (use `__name__`) |
| `setup` | `dict` | `None` | Custom handler paths |
| `template_dir` | `str` | `'trim/errors/'` | Template directory |

### Default Handlers

```py
{
    400: 'trim.views.errors.handler400',
    403: 'trim.views.errors.handler403',
    404: 'trim.views.errors.handler404',
    500: 'trim.views.errors.handler500',
}
```

### Custom Handlers

```py
error_handlers(__name__, {
    404: 'myapp.views.custom_404',
    500: 'myapp.views.custom_500',
})
```

### Custom Template Directory

```py
error_handlers(__name__, template_dir='myapp/errors/')
```

---

## Quick Reference

```py
from trim import urls
from . import views

# Pattern generation
urlpatterns = urls.paths_named(views,
    home=('HomeView', ''),
    about=('AboutView', 'about/'),
)

urlpatterns = urls.paths_dict(views, {
    'ProductListView': ('list', ''),
})

urlpatterns = urls.paths_tuple(views, (
    ('HomeView', 'home', ''),
))

# Template views
urlpatterns += urls.as_templates(
    about=('about/', 'pages/about.html'),
)

# Includes
urlpatterns = [
    path_include('products/'),
] + path_includes('cart', 'orders')

# Utilities
favicon_path('favicon.ico')
full_url = absolute_reverse(request, 'myapp:view-name')
full_url = absolutify(request, '/path/')
error_handlers(__name__)
```