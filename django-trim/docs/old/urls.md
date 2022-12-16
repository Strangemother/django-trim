# URL's and Paths

Django Short Shorts provides a range of url `path` setup functions for setting up your `urls.py` with less typing.

## Quick start

My personal favourite is the quickest:

```py
from short import urls as shorts
from . import views

urlpatterns = shorts.paths(
    profile=('profile/', views.ProfileView,),
    home=('', views.ProfileView,),
)
```

Functionally identical to this:

```py
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('', views.ProfileView.as_view(), name='home'),
```

Go you just have some template files?

```py
urlpatterns += shorts.as_templates(
    geoms=('mockup/', 'mockup/crystal-geometries.html'),
    crystal1=('mockup/1/', 'mockup/crystal-1.html'),
    crystal1=('mockup/home/', 'mockup/home.html'),
)
```

Functionally identical to:

```py
urlpatterns = [
    path('mockup/', views.TemplateView.as_view(name=..), name='geoms'),
    #...
]
```

## Integration Methods

Firstly lets look at a few `path` urls using the standard method:

```py
from django.urls import path

from . import views

urlpatterns += [
    path('', views.NoteIndexView.as_view(), name='index'),
    path('<str:pk>/json/', views.EntryDetailView.as_view(), name='entry-detail-json'),
    path('entry/list/json/', views.EntryJsonList.as_view(), name='entry-list-json'),
]
```

Let's use the `short.urls.paths_dict` function to build the same thing with less typing:

```py
short_patterns = {
    'NoteIndexView': ('index', ''),
    'EntryJsonList': ('entity-list-json', 'entry/list/json/',),
    'EntryDetailView':('entry-detail-json', '<str:pk>/json/', ),
}

urlpatterns += shorts.paths_dict(views, short_patterns)
```

Personally I think a `dict` definition looks nice:

```py
short_patterns = dict(
    NoteIndexView=('index', ''),
    EntryJsonList=('entity-list-json', 'entry/list/json/',),
    EntryDetailView=('entry-detail-json', '<str:pk>/json/', ),
)

urlpatterns += shorts.paths_dict(views, short_patterns)
```

Anything iterable is usable such as a tuple of tuples in place of a dict:

```py
short_patterns = (
    ('NoteIndexView', ('index', '')),
    ('EntryJsonList', ('entity-list-json', 'entry/list/json/',)),
    ('EntryDetailView', ('entry-detail-json', '<str:pk>/json/', )),
)

urlpatterns += shorts.paths_dict(views, short_patterns)
```

However that's a lot of brackets, consider the `short.urls.paths_tuple` to provide flat tuples as your setup.

```py
short_patterns = (
    ('NoteIndexView', 'index', '' ),
    ('EntryJsonList', 'entity-list-json', 'entry/list/json/' ),
    ('EntryDetailView', 'entry-detail-json', '<str:pk>/json/' ),
)

urlpatterns += shorts.paths_tuple(views, short_patterns)
```

---

In all cases the _short.shorts_ library implements a standard `django.urls.path` list,
