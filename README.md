# Django Trim

[![Upload Python Package](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/django-trim?label=django-trim)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-trim)


> Effortlessly trim the boilerplate in your Django projects with `django-trim`. This convenient little library streamlines your models, views, forms, and more, - supporting core functionality for a smoother, more enjoyable day of coding.


Django Trim complements Django's robust framework, offering a suite of tools that enhance and simplify the creation of URLs, forms, views, models, templates, and more.

+ Less typed text, same functionality
+ clear, predicable functional naming
+ Leverage conventions for faster prototyping
+ 100% compatible with existing Django components.

`django-trim` respects Django's core principles, adding a layer of convenience and efficiency for developers who love Django's power but want to type lss wrds.


## Setup

Download:

```bash
pip install django-trim
```

### Install

Note this Apply the app `trim` to your `INSTALLED_APPS` within your `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'trim',
    # ...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

You're ready to go.


## Trim Examples

Django trim is a facade to the common features of Django providing a layer of sugar for all those daily components. Some quick examples to quickly trim your code:

+ Models
+ Views
+ Forms
+ URLs
+ Admin
+ Templates

`django-trim` shortcuts a wealth of fun django parts. All are designed to trim your code without effort.


### Models

At the top of the list is functional model fields. For instant and easy importing:


<table>
<thead><tr>
  <th align="left">Before</th>
  <th align="left">After</th>
</tr></thead>
<tbody><tr valign="top"><td>

```py
from django.db import models


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.TextField(max_length=100)


class Album(models.Model):
    artist = models.ForeignKey(Musician,
                            on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
```

</td><td>


```py
from django.db import models
from trim.models import fields


class Musician(models.Model):
    first_name = models.chars(50)
    last_name = models.str(50)    # alias of string or chars
    instrument = models.text(100)


class Album(models.Model):
    artist = models.fk(Musician)
    name = models.chars(100)
    release_date = models.date()
    num_stars = models.int()
```

</td></tbody></table>


All fields exist, including complex types such as the _User_ Foreign Key, or even a `DateTime` _created_ and _updated_:

```py
from django.db import models
from trim.models import fields

class StockChange(models.Model):
    user = fields.user_fk()
    stockcount = fields.fk(StockCount)
    from_count = fields.int(0)
    to_count = fields.int(1)
    created, updated = fields.dt_cu_pair()
```


### Forms

Trim your form definitions with `trim.forms.fields`. They're exactly the same fields as the original, but with less text!


```py
from django import forms
from trim.forms import fields

class ContactForm(forms.Form):
    sender = fields.email(required=False) # EmailField
    cc_myself = fields.bool_false() # A boolean field if `False` prepared
    subject = fields.chars(max_length=255, required=False) # CharField
    message = fields.text(required=True) # A ready-to-go CharField with a TextArea widget
```

### Views

Easy import (class based) views:

```py
from trim import views
from . import models

class MyModelListView(views.ListView, views.Permissioned):
    """A list view for all MyModels for users with admin mymodel "view" permission.
    """
    model = models.MyModel
    permission_required = ( 'stocks.view_mymodel')
```

### URLs

Excellently easy URLS defined as readable dictionaries:


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


You can choose `name` defined patterns using `paths_named()`, or alternatively `ClassViewName` pattern using `paths_dict()`

```py
from trim import urls

trim_patterns = dict(
    NoteIndexView=('index', ''),
    EntryJsonList=('entity-list-json', 'entry/list/json/',),
    EntryDetailView=('entry-detail-json', '<str:pk>/json/', ),
)

# No change to the loadout.
urlpatterns = urls.paths_dict(views, trim_patterns)
```

Perform Full includes through single entries, each expand to the conventional include:

<table>
<thead><tr>
  <th align="left">Before</th>
  <th align="left">After</th>
</tr></thead>
<tbody><tr valign="top"><td>

```py
from django.urls import include, path

urlpatterns = [
    path("account/", include("account.urls")),
    path("products/", include("products.urls")),
    path("contact/", include("contact.urls")),
    ...
]
```

</td><td>


```py
urlpatterns = urls.path_includes(
        'account',
        'products',
        'contact',
        ...
    )
```

</td></tbody></table>


And so much more! All designed to trim your code for readability and us lazy fingers.


---

## Philosophy

I aim for the _Trim_ philosophy "convenient and thoughtless" - where a function or method should be quick to type, until I'm ready to replace them with the django builtins.


## License

This project is licensed under the terms of the MIT License.

The MIT License offers you the freedom to use, modify, and distribute this code. While it’s not a formal requirement, taking a moment to acknowledge the original contributors reflects a deep-seated respect that is fundamental to the open-source community.

## Contributing

We sincerely welcome contributions! There is no barrier for entry and all input is valid input. If you find a bug or have a feature request, please open an issue. If you'd like to contribute code, please fork the repository and submit a pull request.

---

Open-source is as much about collaboration and mutual respect as it is about code. As a project committed to this ethos, we promise to always recognize and credit contributions with gratitude and respect.

We value the thoughtfulness and care put into each contribution, not to reduce them to mere numbers or to brush them off with a cavalier _"...that’s what open source is..."_. A project thrives on its community’s spirit and collective efforts.

