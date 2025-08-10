<div markdown=1 align="center">

![django trim logo](./docs/logo/django-trim-logo-flat-300.png)

# Django Trim

Effortlessly trim the boilerplate in your Django projects.

[![Upload Python Package](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/django-trim?label=django-trim)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-trim)

---

</div>


> Trim the boilerplate from your Django projects with shortcuts for models, views, forms, URLs, template tags, and more.


Django trim is a facade to the common features of Django, providing a layer of sugar for all those daily tasks.

> [!TIP]
> Head to the [docs/ for a list of components](./docs/)!

## Setup

Install Django Trim from [PyPI](https://pypi.org/project/django-trim/) and add it to your Django project:

```bash
pip install django-trim
```

### Install

In your `settings.py`, include `trim` in `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'trim',
    # ...
]
```

That’s it!

## Contents

[Models](#models) | [Views](#views)    | [Forms](#forms) | [URLs](#urls) | [Admin](#admin) | [Template Tags](#template-tags) | [Other Features](#other-features)



## Highlights and Features

`django-trim` respects Django's core principles, adding a layer of convenience for developers who love Django's power but want to type lss wrds.

+ Less typed text, same functionality
+ clear, predicable functional naming
+ Leverage conventions for faster prototyping
+ 100% compatible with existing Django components.

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

I aim for the _Trim_ philosophy "convenient and thoughtless" - where a function or method should be quick to type, until I'm ready to replace them with the django builtins.


## License

This project is licensed under the terms of the MIT License.

The MIT License offers you the freedom to use, modify, and distribute this code. While it’s not a formal requirement, taking a moment to acknowledge the original contributors reflects a deep-seated respect that is fundamental to the open-source community.

## Contributing

We sincerely welcome contributions! There is no barrier for entry and all input is valid input. If you find a bug or have a feature request, please open an issue. If you'd like to contribute code, please fork the repository and submit a pull request.

---

Open-source is as much about collaboration and mutual respect as it is about code. As a project committed to this ethos, we promise to always recognize and credit contributions with gratitude and respect.

We value the thoughtfulness and care put into each contribution, not to reduce them to mere numbers or to brush them off with a cavalier _"...that’s what open source is..."_. A project thrives on its community’s spirit and collective efforts.

