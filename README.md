# Django Trim

> Django Trim shortcuts all the boilerplate for some of those daily django parts. Reduce the amount of written text and trim your code for easier reading, faster prototyping, and less typing.

Django Trim reduces the amount of text, imports and general congantive overload of microtasks when plugging together a django app in it's initial stages.

+ Less typed text, same functionality
+ clear, predicable functional naming
+ Leverage conventions for faster prototyping
+ 100% compatible with existing django components.

## Setup

Download:

```bash
pip install django-trim
```

### Install:

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

#### Optional Integration

Later-on you may need to apply an entry to your `context_processors`.

Within the your settings `TEMPLATES` entity, add `trim.context.appname` to the `OPTIONS.context_processors`:

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # ...
                    "trim.context.appname",
                ],
            },
        },
    ]

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

functionally named model fields:

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

_otherapp/models.py_

```py
from trim.models import AutoModelMixin

class FooMonkeyMixin(AutoModelMixin):

    def wave(self, word):
        print(f"Hi - I'm a {self} waving {word}")

    class Meta:
        # The target app 'baskets' and its model 'Cart'
        model_name = 'otherapp.Person'
```

```py
>>> from otherapp.models import Person
>>> Person().wave('hello')
"Hi I'm <Person: Person object (None)> waving hello"
```

### Forms

Trim your form definitions with `trim.forms.fields`. They're exactly the same fields as the original , but with less text!

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

Excellently easy URLS defined as reable dicts:

```py
from trim import urls

trim_patterns = dict(
    NoteIndexView=('index', ''),
    EntryJsonList=('entity-list-json', 'entry/list/json/',),
    EntryDetailView=('entry-detail-json', '<str:pk>/json/', ),
)

# No change to the loadout.
urlpatterns = urls.paths_dict(views, trim_patterns)
# Perform Full includes through single entries, each expand to the conventional include:
urlpatterns += urls.path_includes(
        'account', # path('account/', include('accounts'))
        'products',
        'contact',
    )
```

And so much more! All designed to trim your code for readability and us lazy fingers.

## Why.

I write a lot of django code for fun and business, and I'm constantly implementing the core basics, or applying a _"place holder"_ component until I need a fancy replacement.

I've become constantly bored with writing _yet another quick list view_ and a few years ago I considered the idea of a "django boilerplate". To help me boilerplate my work _as I'm developing_, but implement clear, short, standard methodology until I upgrade to a finished view.

Futhermore the boilerplate tool could infer urls, admin, models etc - plugging the gaps until I implement a long-term replacement.

This app serves as _many tiny shortcuts_ all trimmed. As such 99% of the functionality is passive, reading the runtime and producing classes, paths, upon django wakeup and injecting into the module.

---

I aim for the _Trim_ philosophy "convenient and thoughtless" - where a function or method should be quick to type, until I'm ready to replace them with the django builtins.



## License

This project is licensed under the terms of the MIT License.

The MIT License offers you the freedom to use, modify, and distribute this code. While it’s not a formal requirement, taking a moment to acknowledge the original contributors reflects a deep-seated respect that is fundamental to the open-source community.

## Contributing

We sincerely welcome contributions! There is no barrier for entry and all input is valid input. If you find a bug or have a feature request, please open an issue. If you'd like to contribute code, please fork the repository and submit a pull request.

---

Open-source is as much about collaboration and mutual respect as it is about code. As a project committed to this ethos, we promise to always recognize and credit contributions with gratitude and respect.

We value the thoughtfulness and care put into each contribution, not to reduce them to mere numbers or to brush them off with a cavalier _"...that’s what open source is..."_. A project thrives on its community’s spirit and collective efforts.

