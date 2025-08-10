<div align="center">

<img src="./docs/logo/django-trim-logo-flat-300.png" alt="django-trim logo" width="240" />

# Django Trim

Trim Django boilerplate with concise, compatible helpers for models, views, forms, URLs, admin, and templates.

[![Upload Python Package](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/django-trim?label=django-trim)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-trim)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-trim)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

</div>

> A thin, explicit layer over Django that reduces boilerplate without lock‑in. Use the shortcuts, or swap back to built‑ins anytime.


## Docs Quick Links

- Models: [Functional Fields](./docs/models/fields.md) · [Auto Model Mixin](./docs/models/auto_model_mixin.md) · [Live Model Access](./docs/models/live.md)
- Views: [List Views](./docs/views/list-views.md) · [Authenticated Views](./docs/views/authed-views.md) · [JSON/Serialized](./docs/views/serialized.md) · [File Upload/Download](./docs/views/files-up-down.md)
- Forms: [Quickforms](./docs/forms/quickforms.md) · [Quickform Tag](./docs/templates/tags/quickform.md)
- URLs: [Overview](./docs/urls/readme.md) · [Helpers](./docs/urls/functions.md)
- Templates: [Link](./docs/templates/tags/link/readme.md) · [Wrap/Slot](./docs/templates/tags/wrap.md) · [Strings](./docs/templates/tags/strings.md) · [Updated Params](./docs/templates/tags/updated-params.md) · [CSS/JS](./docs/templates/tags/css-js-tag.md)
- Admin: [Register Models](./docs/admin.md)
- Execute: [read_one](./docs/execute.md)


## Quick Start

1) Install

```bash
pip install django-trim
```

2) Add to your Django settings

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'trim',
]
```

3) Use in 30 seconds

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

> [!TIP]
> Explore the docs for more helpers and patterns: `docs/`.


## Highlights

- Fewer keystrokes, same Django. Functional helpers map 1:1 to Django features (lss wrds 😉).
- Zero lock‑in. Swap any helper for the Django builtin at any time.
- Convention‑friendly. Sensible defaults for rapid prototyping.
- Works with your stack. 100% compatible with Django components.


## Feature Areas

### Models
- Use concise helpers like `fields.fk('ModelName')`, `fields.bool_false()`, `fields.int(6)`.
- Add behavior without touching original models via Auto Model Mixin.
- Access any installed model via `trim.live.app.ModelName`.
- Docs: [Fields](./docs/models/fields.md) · [Auto Model Mixin](./docs/models/auto_model_mixin.md) · [Live](./docs/models/live.md)

### Views
- Simplified class-based views and decorators.
- Built-in auth/permission mixins and easy JSON serialization.
- Docs: [List](./docs/views/list-views.md) · [Auth](./docs/views/authed-views.md) · [JSON](./docs/views/serialized.md) · [Files](./docs/views/files-up-down.md)

### Forms
- Functional form helpers and the `{% quickform %}` tag for zero-config rendering.
- Docs: [Quickforms](./docs/forms/quickforms.md) · [Quickform Tag](./docs/templates/tags/quickform.md)

### URLs
- Generate URL patterns from view classes.
- Docs: [Overview](./docs/urls/readme.md) · [Helpers](./docs/urls/functions.md)

### Templates
- Advanced composition with `{% link %}`, `{% wrap %}`, and `{% slot %}`.
- Docs: [Link](./docs/templates/tags/link/readme.md) · [Wrap](./docs/templates/tags/wrap.md) · [Wrap/Slot](./docs/templates/tags/wrap-slots.md) · [Strings](./docs/templates/tags/strings.md) · [Updated Params](./docs/templates/tags/updated-params.md) · [CSS/JS](./docs/templates/tags/css-js-tag.md)

### Admin
- Register all models in an app quickly.
- Docs: [Admin](./docs/admin.md)

### Execute
- Minimal helpers for common execution patterns.
- Docs: [Execute · read_one](./docs/execute.md)


## Philosophy

Convenient, explicit shortcuts you can replace with Django builtins anytime.


## Contributing

Issues and PRs are welcome. See the tracker on GitHub.


## License

MIT — see [LICENSE](./LICENSE).
