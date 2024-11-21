
## Template View

An instant view for your template:

```py
from trim import urls

urlpatterns += [
    urls.template_view('mockup/', 'mockup/crystal-geometries.html'),
]
```

Or mutiple in a larger definition:

```py
from trim import urls

urlpatterns += urls.as_templates(
    geoms=('mockup/one/', 'mockup/crystal-geometries.html'),
    meta_materials=('mockup/two', 'mockup/meta-state-materials.html'),
)
```


## favicon_path

Implement your favicon as a static redirect

```py
# (primary) urls.py
from trim.urls import favicon_path

urlpatterns = [
    ...
    favicon_path('favicon.ico'),
]
```


## absolute_reverse

Given a `request` and a view `name`, perform a reverse of the name and return an absolute url

```py
from trim.urls import absolute_reverse

absolute_reverse(request, "app:viewname")
# http://example.com/foo/bar
```


## absolutify

Given a request, and a partial path, return a complete or _absolute_ path, for the current host:

```py
from trim.urls import absolutify

absolutify(request, '/foo/bar/')
# http://example.com/foo/bar
```

## path_includes

Perform a standard django `include(...)`, using the name of the app to infer the url:


```py
from trim.urls import path_includes_pair as includes

urlpatterns = [
    path("django-admin/", admin.site.urls),
] + includes(
        'file',     # app, applied url file/...
    )
```

Another example:

```py
from django.contrib import admin
from django.urls import path, include

from trim.urls import path_includes, error_handlers

app_name = 'shoppinglist'

urlpatterns = [
    path('admin/', admin.site.urls),
] + path_includes('products')

error_handlers(__name__)
```


## path_includes_pair

 Similar to the `path_includes` function; given many names, convert to a django
 include and return paths. With `path_includes_pair`, a single item may be a list or tuple, allowing `('module', 'url/')` expansion.

```py
from trim.urls import path_includes_pair as includes

urlpatterns = [
    path("django-admin/", admin.site.urls), # default method
] + includes(
        'file',                         # single string entry
        ('trim.account', 'account/',),  # Tuple entry
    )

```


## path_include

Similar to a standard Django include, the `path_include` helps install apps with a `url` module within.

Install an app with the URL alone:

```py
from trim.urls import path_include

path_include('products/',)
```

We can extend this to a url string, a _urls_ module to import, and a name. In all cases if a parameter is missing, its infered from the sibling values:

```py
from trim.urls import path_include

path_include('products/',)
path_include('mythings/', 'products.urls', ) # name=mythings
path_include('mythings/', 'products.urls', 'items') # name=items
path_include('products/', 'products.urls', 'products')
```

## paths_tuple

Setup URLS using a tuple of tuples, with each given tuple prepared and passed to the paths_dict:

```py
from trim import urls

trim_patterns = (
    ('NoteIndexView', 'index', '' ),
    ('EntryJsonList', 'entity-list-json', 'entry/list/json/' ),
    ('EntryDetailView', 'entry-detail-json', '<str:pk>/json/' ),
)

urlpatterns = urls.paths_tuple(views, trim_patterns)
```

Of which is the same as:

```py
from trim import urls

trim_patterns = dict(
    NoteIndexView=('index', ''),
    EntryJsonList=('entity-list-json', 'entry/list/json/',),
    EntryDetailView=('entry-detail-json', '<str:pk>/json/', ),
)

urlpatterns = urls.paths_dict(views, trim_patterns)
```

## Other Functions

+ path_include
+ paths_named
+ paths_tuple
+ paths_dict
+ template_view
+ as_templates
+ error_handlers