# `trim.urls`

+ Named Paths
    + `paths_named`
    + `paths_dict`
+ Includes
    + `path_includes`


## Named Patterns

Named Patterns helps build a list of `paths()` for your `urlspatterns` using dictionary mappings.


### Example

The `trim.urls.paths_named` function reduces the typing required for `path()` URLs.

The function accepts keyword arguments as the _name_ of pattern, accepting a tuple for the target _class_ within `views` and the target _url_.

_urls.py_
```py
from trim import urls
from . import views

app_name = 'myapp'

urlpatterns = urls.paths_named(views,
    # {% url myapp:name 'foostring' %}%
    name=('ClassNamedView', 'my/url/<str:foo>/',),
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
    home=('HomeView', (
                        '/',
                        '<str:theme>/',
                       ),
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


#### Before

With `trim.urls.path_includes`, The URL patterns will look something like this:

```py
from django.urls import path, include
from django.views.generic import TemplateView
from .views import HomePage

urlpatterns += [
        path('account/', include('account.urls'))
        path('products/', include('products.urls'))
        path('contact/', include('contact.urls'))
    ]

# Other examples
urlpatterns = [
    path("/", HomePage.as_view(), name='home'),
    path("about/", TemplateView.as_view(template_name="about.html")),
]
```

#### After

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