# Copilot Instructions for `django-trim`

## Overview
- **Purpose:** `django-trim` is a productivity layer for Django, providing concise, functional shortcuts for models, views, forms, URLs, admin, and templates. It aims to reduce boilerplate and speed up common Django tasks without sacrificing clarity or compatibility.
- **Structure:** Core code is in `src/trim/` and `build/lib/trim/`. Documentation is in `docs/`. Example usages and patterns are in the `README.md` and `docs/` subfolders.

## Key Patterns & Conventions
- **Functional Field Helpers:** Use `from trim.models import fields` for model fields (e.g., `fields.fk('ModelName')`, `fields.bool_false()`). These shadow Django fields and are interchangeable.
- **Auto Model Mixins:** Use `trim.models.AutoModelMixin` to add behavior to existing models without modifying their definitions. See `docs/models/auto_model_mixin.md`.
- **Live Model Access:** Access any installed model via `trim.live.app.ModelName` (no import needed).
- **Views:** Use `from trim import views` for class-based views and mixins. Permissioning and JSON/Markdown views are available. See `docs/views/`.
- **URL Patterns:** Use `trim.urls.paths_named`, `paths_dict`, or `paths_tuple` to generate URL patterns from view classes. See `docs/urls/`.
- **Forms:** Use `quickform` template tag for zero-config forms. See `docs/forms/quickforms.md`.
- **Admin:** Register all models in an app with `trim.admin.register_models(models)`.
- **Template Tags:** Use `{% wrap %}`, `{% slot %}`, and `{% link %}` for advanced template composition. See `docs/templates/tags/`.

## Developer Workflows
- **Testing:** Run all tests with `python run_test.py` (uses pytest). Test files are in `src/trim/tests.py` and possibly other submodules.
- **Installation:** Install with `pip install django-trim`. Add `'trim'` to `INSTALLED_APPS` in Django settings.
- **Docs:** See `docs/` for detailed usage and examples. The `README.md` provides a high-level overview and code snippets.

## Project-Specific Notes
- **No Magic:** All helpers are explicit and compatible with Django's built-ins. You can swap out `trim` components for Django's at any time.
- **Naming:** Functions and helpers are named for clarity and brevity (e.g., `fields.int(6)`, `views.Permissioned`).
- **Extensibility:** Mixins and helpers are designed to be layered and composed.
- **Location:** Prefer editing/adding features in `src/trim/` (not `build/`).

## Examples
- **Model:**
  ```python
  from trim.models import fields
  class HenBasket(models.Model):
      chicken = fields.fk('Chicken')
      owner = fields.user_fk()
      full = fields.bool_false()
      eggs = fields.int(6)
      created, updated = fields.dt_cu_pair()
  ```
- **View:**
  ```python
  from trim import views
  class HenBasketListView(views.ListView):
      model = HenBasket
  ```
- **URLs:**
  ```python
  from trim.urls import paths_named
  urlpatterns = paths_named(views, list=('HenBasketListView', ('', 'baskets/'),))
  ```
- **Admin:**
  ```python
  from trim import admin as t_admin
  t_admin.register_models(models)
  ```

## Where to Look
- `src/trim/` — main codebase
- `docs/` — documentation and usage patterns
- `README.md` — high-level overview and quickstart

---
For more, see the [docs/ directory](../docs/) and code comments in `src/trim/`.
