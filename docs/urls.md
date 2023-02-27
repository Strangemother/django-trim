# URLs

Help the readability of your `urls.py`:

## Named Patterns `trim.urls.paths_named`

Named Patterns helps build a list of `paths()` for your `urlspatterns` using dictionary mappings.


```py

from trim import urls as t_urls
from trim.models import grab_models

from . import views

app_name = 'contact'

urlpatterns = t_urls.paths_named(views,
    success=('ContactFormSuccessView', 'thanks/',),
    # reference trim generated views.
    sheet=('ContactMessageListView', 'sheet/',),
    detail=('ContactMessageDetailView', 'sheet/<str:pk>/',),
)
```

##  Class Based `trim.urls.paths_dict`

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

from trim import urls as t_urls

urlpatterns = t_urls.paths_dict(views, trim_patterns)
```

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


## Includes `trim.urls.path_includes`

Perform Full includes through single entries, each expand to the conventional include:

```py
from trim.urls import path_includes as includes

urlpatterns += includes(
        'account', # path('account/', include('accounts'))
        'products',
        'contact',
    )
```

### Just Templates `trim.urls.as_templates`

Maybe just a `TemplateView` or four:

_urls.py (extended from above)_
```py
urlpatterns += t_urls.as_templates(
    geoms=('mockup/', 'mockup/crystal-geometries.html'),
    crystal1=('mockup/1/', 'mockup/crystal-1.html'),
    home=('mockup/home/', 'mockup/home.html'),
    v1_article=('mockup/article/', 'mockup/v1-article.html'),
    advert_cell=('advert/1/', 'small_adverts.html')
)

urlpatterns += [
    t_urls.template_view('mockup/2', 'mockup/crystal-geometries.html')
]
```

