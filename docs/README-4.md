<div markdown=1 align="center">

![django trim logo](./docs/logo/django-trim-logo-flat-300.png)

# Django Trim

Effortlessly trim the boilerplate in your Django projects.


[![Upload Python Package](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/django-trim?label=django-trim)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-trim)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-trim)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)


</div>


> Trim the boilerplate from your Django projects with shortcuts for models, views, forms, URLs, template tags, and more.



## Docs Quick Links

> [!TIP]
> Head to the [docs/ for a list of components](./docs/)!

- Models: [Functional Fields](./docs/models/fields.md) · [Auto Model Mixin](./docs/models/auto_model_mixin.md) · [Live Model Access](./docs/models/live.md)
- Views: [List Views](./docs/views/list-views.md) · [Authenticated Views](./docs/views/authed-views.md) · [JSON/Serialized](./docs/views/serialized.md) · [File Upload/Download](./docs/views/files-up-down.md)
- Forms: [Quickforms](./docs/forms/quickforms.md) · [Quickform Tag](./docs/templates/tags/quickform.md)
- URLs: [Overview](./docs/urls/readme.md) · [Helpers](./docs/urls/functions.md)
- Templates: [Link](./docs/templates/tags/link/readme.md) · [Wrap/Slot](./docs/templates/tags/wrap.md) · [Strings](./docs/templates/tags/strings.md) · [Updated Params](./docs/templates/tags/updated-params.md) · [CSS/JS](./docs/templates/tags/css-js-tag.md)
- Admin: [Register Models](./docs/admin.md)
- Execute: [read_one](./docs/execute.md)

Django trim is a facade to the common features of Django, providing a layer of sugar for all those daily tasks.

> [!TIP]
> Head to the [docs/ for a list of components](./docs/)!

## Install &amp; Setup

Install from [PyPI](https://pypi.org/project/django-trim/) and install it to your Django project:

```bash
pip install django-trim
```

In your `settings.py`, include `trim` in `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'trim',
    # ...
]
```

## 30 Second Demo


```python
# models.py
from django.db import models
from trim.models import fields

class HenBasket(models.Model):
    chicken = fields.fk('Chicken')
    full = fields.bool_false()
    eggs = fields.int(6)
```

```python
# views.py
from trim import views
from .models import HenBasket

class HenBasketListView(views.ListView):
    model = HenBasket
```

```python
# urls.py
from trim.urls import paths_named
from . import views

urlpatterns = paths_named(
    views,
    list=(
        'HenBasketListView',
        ('', 'baskets/'),
    ),
)
```


## Contents

[Models](#models) | [Views](#views)    | [Forms](#forms) | [URLs](#urls) | [Admin](#admin) | [Template Tags](#template-tags) | [Other Features](#other-features)


## Highlights and Features

`django-trim` respects Django's core principles, adding a layer of convenience for developers who love Django's power but want to type lss wrds.

+ Less typed text, same functionality
+ Zero lock‑in. Swap any helper for the Django builtin at any time.
+ 100% compatible with Django components.


Head to the [docs/ for a list of components](./docs/)


## Models


[Models](./docs/models/) | [Auto Model Mixin](./docs/models/auto_model_mixin.md) \| [Functional Fields](./docs/models/fields.md) \| [Live String](./docs/models/live.md)

<details> <summary>Key Features</summary>

`trim.models` gives you concise, functional shortcuts for defining Django models.

+ Skip repetitive field declarations and use helpers like `fields.fk('ModelName')`, `fields.bool_false()`, and `fields.int(6)` for clarity and speed.
+ Auto-mixins let you add behaviors without touching your original model code.
+ Instantly access any installed model via `trim.live.app.ModelName`—no imports needed.

Whether you want rapid prototyping or maintainable code, `trim.models` keeps your models clean, explicit, and fully compatible with Django’s built-ins.

</details>


## Views

[Views](./docs/views/)     | [Authed Views](./docs/views/authed-views.md) \| [List View](./docs/views/list-views.md) \| [JSON Views](./docs/views/serialized.md)

<details> <summary>Key Features</summary>

`trim.views` provides a set of functional views and decorators to simplify your view logic.

+ Simplified view creation with `views.get`, `views.post`, and more.
+ Built-in support for authentication and permissions.
+ Easy JSON serialization with `views.serialized`.
+ Decorators for common tasks like `@views.auth_required` and `@views.permission_required`.

</details>

## Forms


[Forms](./docs/forms/)     | [quickforms](./docs/forms/quickforms.md) \| [`{% quickform %}` tag](./docs/templates/tags/quickform.md)

<details> <summary>Key Features</summary>

`trim.forms` provides a set of functional forms and form fields to streamline form handling.

+ Functional form fields like `forms.chars()`, `forms.email()`, and more.
+ Use the `{% quickform %}` template tag for quick form rendering in templates.

</details>

## URLs

[URLs](./docs/urls/) | [named urls](./docs/urls)

## Admin

[`register_models`](./docs/admin.md) | [`register`](./docs/admin.md#register)

## Templates

[Templates](./docs/templates/)

### TemplateTags

[`{% quickform %}` tag](./docs/templates/tags/quickform.md) | [`{% link %}` tag](./docs/templates/tags/link/readme.md) |
[`{% wrap %}` tag](./docs/templates/tags/wrap.md) and [`{% slot %}` Tag](./docs/templates/tags/wrap-slots.md)

<details> <summary>Key Features</summary>

`trim.templates` provides a set of template tags to enhance your Django templates.

</details>


## Other Features

_Execute_ | [`read_one`](./docs/execute.md)

---

## Philosophy

I aim for the _Trim_ philosophy "convenient and thoughtless". Convenient, explicit shortcuts you can replace with Django builtins anytime.


## Contributing

Issues and PRs are welcome. See the tracker on GitHub.


## License

MIT — see [LICENSE](./LICENSE).
