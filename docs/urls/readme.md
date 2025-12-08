# `trim.urls`

Simplify Django URL configuration with helper functions that reduce boilerplate and improve readability.

> [!TIP]
> For comprehensive documentation of all URL functions, see [URL Functions Reference](./functions.md).

## Quick Reference

| Tool | Description |
| ---  |  --- |
| [paths_named](./functions.md#paths_named) | Apply patterns using the _view name_ as the keyword |
| [paths_dict](./functions.md#paths_dict) |  A pattern using the _class name_ as the keyword |
| [paths_tuple](./functions.md#paths_tuple) | Build patterns from tuple definitions |
| [path_includes](./functions.md#path_includes) | Create many _include_ patterns, using the _appname_ |
| [path_includes_pair](./functions.md#path_includes_pair) | Perform _includes_ with a tuple of _appname_, and _url_ |
| [path_include](./functions.md#path_include) | Single app include with smart inference |
| [template_view](./functions.md#template_view) | Create a single template-only view |
| [as_templates](./functions.md#as_templates) | Create multiple template-only views |
| [absolute_reverse](./functions.md#absolute_reverse) | a `reverse(name)` with the request host prefix |
| [absolutify](./functions.md#absolutify) | convert any url-like string to a fully resolved url  |
| [favicon_path](./functions.md#favicon_path) | create a general favicon url |
| [error_handlers](./functions.md#error_handlers) | Set up custom error page handlers |



## Named Patterns

Named Patterns helps build a list of `paths()` for your `urlspatterns` using dictionary mappings.

The function accepts keyword arguments as the _name_ of pattern, and a tuple for the target _class_ within `views` and the target _url_.

_urls.py_
```py
from trim import urls
from . import views

app_name = 'myapp'

urlpatterns = urls.paths_named(views,
    # {% url myapp:name 'foostring' %}
    name=('ClassNamedView', 'my/url/<str:foo>/',),
    # {% url myapp:stock_list 'Go to stock list' %}
    stock_list=('StockListView', 'stocks/',),
    # {% url myapp:stock_detail object.slug 'view item' %}
    stock_detail=('StockDetailView', 'stocks/<str:slug>',),
    ...
)
```

<table>
<thead><tr>
  <th align="left">Before</th>
  <th align="left">After</th>
</tr></thead>
<tbody><tr valign="top"><td>

Using django's standard pattern for `urls.py`, it may look something like this:

```py
from django.urls import path
from .views import AboutView, ContactView, HomeView

app_name = 'website'

urlpatterns = [
    path("about/", AboutView.as_view(), name='about'),
    path("contact/", ContactView.as_view(), name='contact'),
    path("/", HomeView.as_view(), name='home'),
    path("<str:theme>/", HomeView.as_view(), name='home'),
]
```

</td><td>

The `urls.paths_named` accepts the `views` module, and all patterns as keyword arguments.

```py
from trim import urls
from . import views

app_name = 'website'

urlpatterns = urls.paths_named(views,
    about=('AboutView', 'sheet/<str:pk>/',),
    contact=('ContactView', 'contact/',),
    home=('HomeView', ('/', '<str:theme>/'),),
)
```

</td></tbody></table>


The tuple value contains: `("ClassName", "url")`. The `"url"` may be a tuple, for many urls to one view. As per the example for the _home_ view:

```py
    home=('HomeView',
        # Many URLS - same view.
        ('/', '<str:theme>/', ),
    ), ...
```

##  Class Based `trim.urls.paths_dict`

As an alternative to the _named_ paths, we can use the class name as the key.

Define the target class as the key, with a value of the name and url tuple:

    ClassName: url
    ClassName2: (name, url)
    ClassName3: (name, (url, url, ...))


Use the `urls.paths_dict` function to load a complete dict:

```py
trim_patterns = {
    'ProductListView': '',
    'ProductCreateView': ('create', 'new/'),
    'ProductUpdateView': ('update', 'change/<str:pk>/'),
    'ProductDeleteView': 'delete/<str:pk>/',
    'ProductDetailView': '<str:pk>/',
}

from trim import urls

urlpatterns = urls.paths_dict(views, trim_patterns)
```


### `view_prefix`

The same dictionary pattern can be used for two view-stacks.
In this case we build two sets of the same url pattern, but with the `view_prefix`

```py
trim_patterns = dict(
    ListView='',                              # ProductListView, PeopleListview
    CreateView=('create', 'new/'),            # ProductCreateView, PeopleCreateview
    UpdateView=('update', 'change/<str:pk>/'),# ...
    DeleteView='delete/<str:pk>/',
    DetailView='<str:pk>/',
)

urlpatterns = trims.paths_dict(views, trim_patterns, view_prefix='Product')
urlpatterns = trims.paths_dict(views, trim_patterns, view_prefix='People')
```

## Templates Only

> `trim.urls.as_templates()` for many views, `trim.urls.template_view()` for a single view.

If you only need to present a template, without needing any functionality you can use the `as_templates` function.

It's similar to the `trim.urls.paths_named` function and automatically generates a `TemplateView` for each given keyword argument:

_urls.py_
```py
from trim import urls

urlpatterns = urls.as_templates(
    geoms_mockup=('mockup/', 'mockup/crystal-geometries.html'),
    crystal_mockup=('mockup/1/', 'mockup/crystal-1.html'),
    home=('mockup/home/', 'mockup/home.html'),
    v1_article=('mockup/article/', 'mockup/v1-article.html'),
    advert_cell=('advert/1/', 'small_adverts.html')
)
```

Alternatively you can produce a single `TemplateView` using the `trim.urls.template_view` function:

```py
... # continued from above.

urlpatterns += [
    urls.template_view('mockup/2', 'mockup/crystal-geometries.html')
]
```

## Includes

> `trim.urls.path_includes`

In general cases, the name of a django app can be the sub pattern url for our app. We can reduce an `include` to one entry:

```py
from trim.urls import path_includes as includes

urlpatterns = includes(
        'account',  # path('account/', include('account'))
        ...
    )
```

### Usage

As an example setup, the _myapp_ django site has three internal apps, each residing within a sub-url.

    MyApp:
        myapp: /
        account: /account/
        products: /products/
        contact: /contact/

The URL for the _contact_ app would be:

    https://127.0.0.1:8000/contact/



<table>
<thead><tr>
  <th align="left">Before</th>
  <th align="left">After</th>
</tr></thead>
<tbody><tr valign="top"><td>


With `trim.urls.path_includes`, The URL patterns will look something like this:

```py
from django.urls import path, include
from django.views.generic import TemplateView
from .views import HomePage

urlpatterns += [
        path('account/', include('account.urls')),
        path('products/', include('products.urls')),
        path('contact/', include('contact.urls')),
    ]

# Other examples
urlpatterns = [
    path("/", HomePage.as_view(), name='home'),
    path("about/", TemplateView.as_view(template_name="about.html")),
]
```

</td><td>

We can trim this down, by performing full `include` through single entries - each entry will become the conventional `path` include:

```py
from trim.urls import path_includes as includes
from trim import urls
from .views import HomePage

urlpatterns += includes(
        'account', # path('account/', include('accounts'))
        'products',
        'contact',
    )

# other examples
urlpatterns = urls.paths_dict(views, home=('/', Homepage))
urlpatterns += [urls.template_view('about/', 'about.html')]
```

This example is purposefully verbose to show we can still concatenate `paths_dict`, `lists` and `includes` without issue.

</td></tbody></table>

### path_includes_pair

Similar to the `path_includes` function; given many names, convert to a django include and return paths. With `path_includes_pair`, a single item may be a list or tuple, allowing ('module', 'url/') expansion.

```py
from trim.urls import path_includes_pair as includes

urlpatterns = [
    path("django-admin/", admin.site.urls),
] + includes(
        'file', # file/
        ('home', "",) # /
        ('trim.account', 'myprofile/',),
    )
```


### absolute_reverse

Reverse a name and return the _absolute_ URL from the request header, returning the host used by the request.

```py
from trim.urls import absolute_reverse

name = 'account:home'
args = (user.slug, )
absolute_reverse(request, name, *args)
# https://userhostdomain.com/profiles/terry-99
```


### absolutify

Given any string (preferably a URL path fragment), return the absolute URL using the host within the given request.

```py
path = '/foo/bar/'
absolutify(request, path)
# https://userhostdomain.com/foo/bar/
```

### favicon_path

Implement your favicon as a static redirect

```
favicon_path(ingress_path='favicon.ico', static_path='images/{ingress_path}')
```

It returns a `RedirectView` with a URL to the applied static files address.

```py
# (primary) urls.py
from trim.urls import favicon_path

urlpatterns = [
    # /static/images/favicon.ico
    favicon_path('favicon.ico'),
    ...
]
```
