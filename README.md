<div align="center">

![Upload Python Package](./docs/logo/django-trim-logo-flat-300.png)

# Django Trim

Effortlessly trim the boilerplate in your Django projects.

[![Upload Python Package](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/django-trim?label=django-trim)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-trim)

---

</div>

> This convenient little library streamlines your models, views, forms, and more, - supporting core functionality for a smoother, more enjoyable day of coding.


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


## Some Features

Django trim is a facade to the common features of Django providing a layer of sugar for all those daily components. Some quick examples to quickly trim your code:

| Thing | Bits |
| --- | --- |
| Models    | [Auto Model Mixin](./docs/models/auto_model_mixin.md) \| [Fields](./docs/models/fields.md) \| [Live String](./docs/models/live.md) |
| Views     | [Authed Views](./docs/views/authed-views.md) \| [List View](./docs/views/listviews.md) \| [JSON Views](./docs/views/serialized.md) |
| Forms     | [quickforms](./docs/forms/quickforms.md) \| [`{% quickform %}` tag](./docs/template/tags/quickform.md) |
| URLs      | [named urls](./docs/urls.md)  |
| Admin     | [`register_models`](./docs/admin.md)  |
| Templates | [`{% link %}` tag](./docs/templates/tags/link.md) \| [`{% wrap %}` tag](./docs/templates/tags/wrap.md) \| [`{% slot %}` Tag](./docs/templates/tags/wrap-slots.md) |
| _Execute_ | [`read_one`](./docs/execute.md)

`django-trim` shortcuts a wealth of fun django parts. All are designed to trim your code without effort. Some of our favourite features:

### Models

Use `trim.models.fields` for easy to grab model fields:


```py
from trim.models import fields


class HenBasket(models.Model):
    """A Stock change example """

    # ForeignKey to another model.
    chicken = fields.fk(Chicken)
    user = fields.user_fk()
    # Standard Fields
    full = fields.bool_false()
    other = fields.text()
    eggs = fields.int(6)
    # A datetime pair; created, updated.
    created, updated = fields.dt_cu_pair()
```

All `trim.models.fields` shadow the standard Django field. They are designed to be completely interchangable.


### Views

Simplify your class-based-view Generation with a single-point imports and trimmed extras:

```py
from trim import views # All views available
from . import models

class MyModelListView(views.ListView, views.Permissioned):
    model = models.MyModel
    permission_required = 'stocks.view_stockingmethod'


class AddressDetailView(views.UserOwnedMixin, views.DetailView):
    user_field = 'creator'
    user_allow_staff = True

    model = models.Address
    ...
```

### Forms

Instantly install prepared forms into a view, utilising the form built-into the class-based `FormView`:

```jinja
{% load quickforms %}

<form>
{% quickform "app:formview-name" %} <!-- synonymous to {{ form.as_ul }} -->
</form>

{% quickform.form "app:formview-name" %} <!-- Ready to go POST form -->
```


### URLs

Looking for instantly readable URLs, connected to your class based views?

```py
from trim import urls
from . import views

app_name = 'website'

trim_patterns = dict(
    MyModelListView='',
    AddressDetailView='<str:pk>/',
    ...
    CreateView=('create', 'new/'),             # Use named urls: website:create
    UpdateView=('update', 'change/<str:pk>/'), # Paths are Paths!
    DeleteView='delete/<str:pk>/',             # _JUST_ a URL? Cool
)

urlpatterns = trims.paths_dict(views, trim_patterns)
```


### Admin

Instantly and automatically generate admin views for all your models

```py
from django.contrib import admin
from trim import admin as t_admin

from . import models

t_admin.register_models(models)
```

### Template Tags

#### Wrap Tag

Generate `wrap` templates to import into your view:

```jinja2
{% load wrap slot %}

{% wrap "wraps/target.html" %}
    {% slot %}
        <p>Replace the default content with alternative HTML,
        no slot names needed.</p>
    {% endslot %}
{% endwrap %}
```

#### Link Tag

Generate a hyperlink to a view with `{% link viewname arguments label %}`

```jinja2
{% load link %}
{% link "appname:viewname" %}
```

--

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

