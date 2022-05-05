# Django Short Shorts

Django Short Shorts helps boilerplate work for very fast prototyping and dev jumpstarts. With `short horts` minimal boilerplate code parts, build conventional urls, views, models without the hassle.

> Use Short Shorts for boilerplate, PoC, or just pure laziness, to quickly write common django components.


## Setup


Download:

    pip install django-short-shorts


### Install:

Apply the app `short` to your `INSTALLED_APPS` within your `settings.py`:

    INSTALLED_APPS = [
        # ...
        'short',
        # ...
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]


You're ready to go.

#### Optional Integration

Later-on you may need to apply an entry to your `context_processors`.

Within the your settings `TEMPLATES` entity, add `short.context.appname` to the `OPTIONS.context_processors`:

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # ...
                    "short.context.appname",
                ],
            },
        },
    ]


And that's it.


## Quick Guide


### Models

Build model fields with less text:

```py
from django.db import models
from short import shorts

class Product(models.Model):

    name = shorts.chars()
    unique_id = shorts.chars(default=rand_str)
    description = shorts.text()
    urls = shorts.m2m(Hyperlink)
    damaged = shorts.false_bool()
    created = shorts.dt_created()
    updated = shorts.dt_updated()
    count = shorts.integer(1)
    associated = shorts.m2m('self')
    location = shorts.m2m(Location)
    image = shorts.image()
```

Easy integrate `__str__` and `__repr__` with the `_short_string` trick:

**Before** (default):

```py
>>> p = models.Product.objects.first()
<Product: Product object (3)>
>>> print(p)
Product object (3)
```

**add shorts** upgrade:

```py
class Product(models.Model):
    # ... all previous fields
    _short_string = '"{self.name}" x{self.count}'

    def get_short_string(self):
        s = '"{self.name}"' if self.count == 1 else self._short_string
        return s.format(self=self)
```

**After:**

```py
>>> p = models.Product.objects.first()
<Product(3) '"example name" x4'>
>>> print(p)
"example name" x4
```

### Views

Generate many views for a model using localised discovery:

+ CreateView
+ ListView
+ UpdateView
+ DeleteView
+ DetailView


_views.py_
```py
# from django.shortcuts import render
from short import views as shorts
shorts.crud_classes()

# from . import models
# from short.models import grab_models

# shorts.crud_classes(__name__, models.Product)
# shorts.crud_classes(__name__, grab_models(models))
# shorts.guess_classes(models=grab_models(models))
```

Or with less magic, Generate views for a single or many target models:

```py
# from django.shortcuts import render
from short import views as shorts
from short.models import grab_models
from . import models

# Generate class views for the Product model in this module ("product.views")
shorts.crud_classes(__name__, models.Product)

# Generate views for all models from the import:
shorts.crud_classes(__name__, grab_models(models))
```

Generate the same for 'history' classes:

+ ArchiveIndexView
+ DateDetailView
+ DayArchiveView
+ MonthArchiveView
+ TodayArchiveView
+ WeekArchiveView
+ YearArchiveView

For a single set of class based views for a single model:

_views.py_
```py
# from django.shortcuts import render
from short import views as shorts

# Build many views for the single model
shorts.history(models.Product)

# Specify the target module (this one "products.views") and the views `date_field`
shorts.history(models.Product, __name__, date_field='created')
```

This also works on many models and can be used in conjunction with `crud` functions:

_views.py_
```py
from short import views as shorts

shorts.crud_classes()
shorts.history_classes()
```

This will produce 12 class views per discovered model.


### URLS

Views must be connect with URLs. A minimal example to link the new _crud_ and
_history_ views we just created:

_urls.py_
```py
from django.urls import path

from short import grab_models, urls as shorts, names
from . import views, models

app_name = 'products'

urlpatterns = shorts.paths_default(views, grab_models(models),
    views=names.crud() + names.history(),
)
```

The `short.urls.path_default` function generated many urls for the given views by iterating the found models.

Change the default url patterns using the `shorts.urls.path_less` alternative:

```py
from . import models
from short.models import grab_models

urlpatterns = shorts.paths_less(views, grab_models(models),
    ignore_missing_views=True,
    list='',
    create='new/',
    update='change/<str:pk>/',
    delete='delete/<str:pk>/',
    detail='<str:pk>/',
)
```

Perhaps a more-literal dictionary form is preferred:

```py

short_patterns = {
    'ProductListView': '',
    'ProductCreateView': ('create', 'new/'),
    'ProductUpdateView': ('update', 'change/<str:pk>/'),
    'ProductDeleteView': 'delete/<str:pk>/',
    'ProductDetailView': '<str:pk>/',
}

urlpatterns = shorts.paths_dict(views, short_patterns)

```

Within the master `urls.py`, you can use `short.urls.path_includes`, of which performs the
same as `include` with extras. The `error_handlers` generates error urls such as `404`:

_shoppinglist/urls.py_
```py
from django.contrib import admin
from django.urls import path, include

from short.urls import path_includes, error_handlers

app_name = 'shoppinglist'

urlpatterns = [
    path('admin/', admin.site.urls),
] + path_includes('products')


error_handlers(__name__)
```

### Admin

Automatically generate admin pages for a range of models:

_admin.py_
```py
from short import admin as shorts
from . import models

shorts.register_models(models)
```

## Why build this

A lot of my work with django is hammering fast PoC or dev work - to hack out a new idea, research a small example. I spend a lot of time writing _yet another_ model TextField, or Boilerplating five more ArchiveViews for a throw-away app. Copy/pasting is fine but yields errors.

Django Short Shorts provides a set of methods to _write boilerplate fields, models, views, etc.._ - without forsaking clean code.

For example

    class Product(models.Model):
        name = models.TextField(max_length=255, blank=True, null=True)

Replaced with

    class Product(models.Model):
        name = shorts.text()
