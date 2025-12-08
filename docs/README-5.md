<div markdown=1 align="center">

![django trim logo](./docs/logo/django-trim-logo-flat-300.png)

# Django Trim

Effortlessly trim the boilerplate in your Django projects.

[![Upload Python Package](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Strangemother/django-trim/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/django-trim?label=django-trim)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-trim)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-trim)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

---

</div>


> Trim the boilerplate from your Django projects with shortcuts for models, views, forms, URLs, template tags, and more.

## Popular Bits

Django trim is a facade to the common features of Django, providing a layer of sugar for all those daily tasks.

<table>
<tr>
<td width="50%">

### 🗄️ Models
[Functional Fields](./docs/models/fields.md) · [Auto Mixin](./docs/models/auto_model_mixin.md) · [Live Access](./docs/models/live.md)

Skip repetitive declarations with `fields.fk()`, `fields.bool_false()`, and mix behaviors into existing models without touching their code.

</td>
<td width="50%">

### 👁️ Views
[Authed](./docs/views/authed-views.md) · [List Views](./docs/views/list-views.md) · [JSON](./docs/views/serialized.md)

Class-based views with built-in auth, permissions, and instant JSON serialization.

</td>
</tr>
<tr>
<td width="50%">

### 📝 Forms
[Quickforms](./docs/forms/quickforms.md) · [`{% quickform %}`](./docs/templates/tags/quickform.md)

Zero-config form rendering. Just point to a view name and go.

</td>
<td width="50%">

### 🔗 URLs
[Functions](./docs/urls/functions.md) · [Overview](./docs/urls/readme.md)

Generate clean URL patterns from view classes with `paths_named()`.

</td>
</tr>
<tr>
<td width="50%">

### 🎨 Templates
[`{% link %}`](./docs/templates/tags/link/readme.md) · [`{% wrap %}`](./docs/templates/tags/wrap.md) · [`{% slot %}`](./docs/templates/tags/wrap-slots.md)

Advanced composition with slottable components and smart link generation.

</td>
<td width="50%">

### ⚙️ Admin & More
[register_models](./docs/admin.md) · [read_one](./docs/execute.md)

Auto-register all models and simplified query helpers.

</td>
</tr>
</table>

> [!TIP]
> New to Django or django-trim? Start with [Building a Contact Form](./docs/recipes/basic-page.md) - a complete beginner-friendly guide.

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

That's it!

### Minimal Example:

Django trim covers all the chunky parts, allowing you to rapidly run with your ideas without magic or sacrificing clarity.

Here's a fast example for a hen basket model:

```py
# models.py
from django.db import models
from trim.models import fields

class HenBasket(models.Model):
    chicken = fields.fk('Chicken')
    owner = fields.user_fk()
    full = fields.bool_false()
    eggs = fields.int(6) # args default.
    created, updated = fields.dt_cu_pair()
```

```py
# views.py
from trim import views
from .models import Product

class HenBasketListView(views.ListView):
    model = HenBasket


class HenBasketDetailView(views.DetailView):
    model = HenBasket
```

```py
# urls.py
from trim import urls
from . import views

app_name = 'baskets'

urlpatterns = urls.paths_named(views,
    list=('HenBasketListView', ('', 'baskets/'),),
    detail=('HenBasketDetailView', 'baskets/<str:pk>/',),
)
```


## Highlights and Features

`django-trim` respects Django's core principles, adding a layer of convenience for developers who love Django's power but want to type lss wrds.

+ Less typed text, same functionality
+ clear, predicable functional naming
+ Leverage conventions for faster prototyping
+ Zero lock‑in. Swap any helper for the Django builtin at any time.
+ 100% compatible with existing Django components.

Head to the [docs/ for a list of components](./docs/), Some of our favourite features:

## Feature Areas

### Models

Concise, functional shortcuts for defining Django models with less typing and zero lock-in.

**Top Features:** [Functional Fields](./docs/models/fields.md) · [Auto Model Mixin](./docs/models/auto_model_mixin.md) · [Live Model Access](./docs/models/live.md)

<details> <summary>Expand for full feature list</summary>

**Full Documentation:** [Models Overview](./docs/models/readme.md) · [Fields Reference](./docs/models/fields.md) · [Auto Model Mixin Guide](./docs/models/auto_model_mixin.md) · [Live Models](./docs/models/live.md) · [Short String](./docs/models/short_string.md)

---

**Field Helpers** — Use concise helpers for all Django field types:
+ Foreign keys: `fields.fk('ModelName')` instead of `models.ForeignKey('ModelName', on_delete=models.CASCADE)`
+ User foreign keys: `fields.user_fk()` for instant user relationships
+ Boolean fields: `fields.bool_false()`, `fields.bool_true()` with sensible defaults
+ Integer fields: `fields.int(6)` — first argument sets default value
+ DateTime pairs: `fields.dt_cu_pair()` returns `(created, updated)` timestamp fields
+ Text fields: `fields.chars(100)`, `fields.text()` for common string patterns

```python
# Before
owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='baskets')
active = models.BooleanField(default=False)

# After
owner = fields.user_fk(related_name='baskets')
active = fields.bool_false()
```

**Auto Model Mixin** — Add behavior to existing models without modifying their definitions:
+ Mix methods into any model, including Django's built-in `User` model
+ Target models by string name to avoid circular imports
+ Perfect for extending third-party app models
+ Keeps your model extensions organized and maintainable

```python
class UserBasketsMixin(AutoModelMixin):
    def get_baskets(self):
        return HenBasket.objects.filter(owner=self)
    
    class Meta:
        model_name = "auth.User"
```

**Live Model Access** — Access any installed model without imports:
+ No more circular import headaches: `live.myapp.MyModel`
+ Lazy loading ensures models are available when needed
+ Works across all installed apps
+ Clean, predictable dot notation

```python
from trim import live
# Access any model without importing
basket = live.baskets.HenBasket.objects.first()
user = live.auth.User.objects.get(id=1)
```

**Additional Features:**
+ Short string fields with automatic max length
+ Model field introspection helpers
+ Queryset shortcuts and filters
+ Model serialization helpers

---

</details>

### Views

Streamlined class-based views with built-in authentication, permissions, and serialization.

**Top Features:** [Authenticated Views](./docs/views/authed-views.md) · [JSON Views](./docs/views/serialized.md) · [List Views](./docs/views/list-views.md)

<details> <summary>Expand for full feature list</summary>

**Full Documentation:** [Views Overview](./docs/views/readme.md) · [Authenticated Views](./docs/views/authed-views.md) · [List Views](./docs/views/list-views.md) · [JSON/Serialized Views](./docs/views/serialized.md) · [File Upload/Download](./docs/views/files-up-down.md)

---

**Single Import** — All Django class-based views available from one place:
+ `from trim import views` gives you ListView, DetailView, CreateView, UpdateView, DeleteView, etc.
+ All standard Django views plus trim enhancements
+ Mix and match with standard Django views seamlessly

**Permission Mixins** — Add authentication and permissions with minimal code:
+ `views.Permissioned` — quick permission checking on any view
+ `views.UserOwnedMixin` — ensure users can only access their own objects
+ `views.StaffRequiredMixin` — restrict views to staff users
+ Configurable field checking for ownership validation

```python
class SecureBasketView(views.Permissioned, views.DetailView):
    model = HenBasket
    permission_required = 'baskets.view_henbasket'

class MyBasketsView(views.UserOwnedMixin, views.ListView):
    model = HenBasket
    user_field = 'owner'  # Check ownership on this field
    user_allow_staff = True  # Staff can see all
```

**JSON Views** — Instant API endpoints with automatic serialization:
+ `JsonListView` — return model querysets as JSON arrays
+ `JsonDetailView` — return single objects as JSON
+ Automatic field serialization with customizable field selection
+ Built-in error handling and response formatting

```python
class BasketJsonList(views.JsonListView):
    model = HenBasket
    # Automatically returns JSON array of all baskets

class BasketJsonDetail(views.JsonDetailView):
    model = HenBasket
    # Returns single basket as JSON at /baskets/<pk>/
```

**Markdown Response Views** — Render markdown templates as HTML:
+ `MarkdownTemplateResponse` for markdown-based templates
+ Write content pages in markdown, serve as HTML
+ Perfect for documentation or content-heavy pages

```python
class DocsView(views.TemplateView):
    response_class = MarkdownTemplateResponse
    template_name = "docs/index.md"
```

**File Upload/Download** — Simplified file handling views:
+ Pre-built upload views with validation
+ Secure file download views with permission checking
+ Configurable file storage locations

**Additional Features:**
+ Form views with enhanced validation
+ Redirect helpers and shortcuts
+ Context data mixins for common patterns
+ Error handling mixins

---

</details>

### Forms

Zero-config form rendering and functional field helpers for rapid form development.

**Top Features:** [Quickforms](./docs/forms/quickforms.md) · [`{% quickform %}` Tag](./docs/templates/tags/quickform.md) · [Form Fields](./docs/forms/fields-auto.md)

<details> <summary>Expand for full feature list</summary>

**Full Documentation:** [Forms Overview](./docs/forms/readme.md) · [Quickforms Guide](./docs/forms/quickforms.md) · [Quickform Template Tag](./docs/templates/tags/quickform.md) · [Form Fields Reference](./docs/forms/fields-auto.md) · [All Form Fields](./docs/forms/all-fields-form.md)

---

**Quickform Tag** — Instantly render any form in your templates:
+ Zero configuration required — just point to a view name
+ Automatically handles POST targets and CSRF tokens
+ Works with any Django FormView
+ Render full forms or just fields

### URLs

Generate clean, named URL patterns from view classes with minimal configuration.

**Top Features:** [paths_named](./docs/urls/functions.md) · [paths_dict](./docs/urls/functions.md) · [paths_tuple](./docs/urls/functions.md)

<details> <summary>Expand for full feature list</summary>

**Full Documentation:** [URLs Overview](./docs/urls/readme.md) · [URL Functions Reference](./docs/urls/functions.md)

---

**Named Patterns** — Generate URL patterns with automatic naming:
+ Use `paths_named` to create URL patterns from view classes
+ Automatic URL name generation from view class names
+ Custom names and paths in one declaration
+ Clean, readable URL configuration

```python
from trim.urls import paths_named
from . import views

app_name = 'blog'

urlpatterns = paths_named(views,
    # URL name: blog:list, path: /blog/
    list=('PostListView', ('', 'blog/'),),
    
    # URL name: blog:detail, path: /blog/<slug>/
    detail=('PostDetailView', 'blog/<slug:slug>/',),
    
    # URL name: blog:create, path: /blog/new/
    create=('PostCreateView', 'blog/new/',),
)
```

**Dictionary Patterns** — Build URL patterns from dictionaries:
+ Map view names to URL paths
+ Flexible naming with tuple syntax
+ Mix simple strings with named tuples
+ Great for prototyping and iteration

```python
from trim.urls import paths_dict
from . import views

urlpatterns = paths_dict(views, {
    'PostListView': '',
    'PostDetailView': '<slug:slug>/',
    'PostCreateView': ('create', 'new/'),  # custom name
    'PostUpdateView': ('edit', 'edit/<slug:slug>/'),
})
```

**Tuple Patterns** — Pure tuple-based URL definitions:
+ Clean, tabular format for URL configuration
+ View name, URL name, path pattern in one line
+ Easy to read and maintain
+ Perfect for large URL configurations

```python
from trim.urls import paths_tuple
from . import views

urlpatterns = paths_tuple(views, (
    ('PostListView', 'list', ''),
    ('PostDetailView', 'detail', '<slug:slug>/'),
    ('PostCreateView', 'create', 'new/'),
    ('PostJsonList', 'json-list', 'api/posts/'),
))
```

**Additional Features:**
+ Automatic prefix handling for grouped URLs
+ Regular expression pattern support
+ Include helper for nested URL configurations
+ URL reversal utilities

---

</details>

### Templates

Advanced template tags for links, slots, composition, and dynamic content rendering.

**Top Features:** [`{% link %}`](./docs/templates/tags/link/readme.md) · [`{% wrap %}`](./docs/templates/tags/wrap.md) · [`{% slot %}`](./docs/templates/tags/wrap-slots.md) · [`{% updated_params %}`](./docs/templates/tags/updated_params.md)

<details> <summary>Expand for full feature list</summary>

**Full Documentation:** [Templates Overview](./docs/templates/) · [Link Tag](./docs/templates/tags/link/readme.md) · [Wrap Tag](./docs/templates/tags/wrap.md) · [Slot Tag](./docs/templates/tags/wrap-slots.md) · [Updated Params](./docs/templates/tags/updated_params.md) · [Markdown](./docs/markdown.md) · [Functional Tag](./docs/templates/tags/functional.md) · [DateTime Tags](./docs/templates/tags/datetime.md) · [String Tags](./docs/templates/tags/strings.md) · [CSS/JS Tags](./docs/templates/tags/css-js-tag.md)

---

**Link Tag** — Generate hyperlinks with automatic URL resolution:
+ `{% link viewname %}` creates a complete `<a>` tag
+ Pass arguments for parameterized URLs
+ Customize link text, classes, and attributes
+ Automatic active state detection

```jinja
{% load link %}

{# Simple link #}
{% link "blog:list" "View Blog" %}
{# Output: <a href="/blog/">View Blog</a> #}

{# Link with arguments #}
{% link "blog:detail" post.slug "Read More" %}
{# Output: <a href="/blog/my-post/">Read More</a> #}

{# Link with classes #}
{% link "blog:create" "New Post" class="btn btn-primary" %}
```

**Wrap & Slot Tags** — Component-based template composition:
+ `{% wrap %}` includes templates with customizable slots
+ `{% slot %}` defines replaceable content areas
+ Build reusable template components
+ No slot names required for simple cases

```jinja
{% load wrap slot %}

{# components/card.html #}
<div class="card">
    <div class="card-body">
        {% slot %}
            <p>Default content here</p>
        {% endslot %}
    </div>
</div>

{# your-page.html #}
{% wrap "components/card.html" %}
    {% slot %}
        <h2>Custom Content</h2>
        <p>This replaces the default slot content.</p>
    {% endslot %}
{% endwrap %}
```

**Updated Params Tag** — Modify URL query parameters:
+ Add or update query parameters while preserving others
+ Remove specific parameters
+ Perfect for pagination, filtering, sorting
+ Maintains current URL context

```jinja
{% load updated_params %}

{# Add/update a parameter #}
<a href="?{% updated_params page=2 %}">Page 2</a>

{# Update sort, keep existing filters #}
<a href="?{% updated_params sort='date' %}">Sort by Date</a>

{# Remove a parameter #}
<a href="?{% updated_params filter=None %}">Clear Filter</a>
```

**Markdown Tag** — Write markdown directly in templates:
+ `{% markdown %}` block for inline markdown content
+ Automatic rendering to HTML
+ Great for content-heavy pages
+ Supports full markdown syntax

### Admin

Automatic admin registration for all your models with one line of code.

**Top Features:** [register_models](./docs/admin.md) · [Auto Registration](./docs/admin.md)

<details> <summary>Expand for full feature list</summary>

**Full Documentation:** [Admin Guide](./docs/admin.md)

---

**Automatic Registration** — Register all models in one command:
+ `register_models(models)` registers every model in a module
+ No need to write individual `@admin.register()` decorators
+ Automatic admin class generation with sensible defaults
+ Works with Django's built-in admin customization

```python
from django.contrib import admin
from trim import admin as t_admin
from . import models

# Register all models in this app automatically
t_admin.register_models(models)
```

**Selective Registration** — Control which models get registered:
+ Include/exclude patterns for model names
+ Register specific models only
+ Skip abstract or proxy models automatically

**Custom Admin Classes** — Use with custom admin configurations:
+ Combine with standard Django admin classes
+ Override automatic registration for specific models
+ Maintain fine-grained control when needed

```python
from trim import admin as t_admin
from . import models

# Custom admin for one model
@admin.register(models.SpecialModel)
class SpecialModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

# Auto-register the rest
t_admin.register_models(models, exclude=['SpecialModel'])
```

**Additional Features:**
+ Automatic list_display generation from model fields
+ Search field configuration helpers
+ Filter configuration from field types
+ Inline admin helpers

---

</details>

```markdown
# Heading

This is **bold** and this is *italic*.

- List item 1
- List ite
{% endmarkdown %}
```

**Functional Tag** — Inline Python expressions in templates:
+ Execute Python functions in templates
+ Pass context variables as arguments
+ Filter and transform data on the fly

**String Manipulation Tags** — Common string operations:
+ Truncation and padding helpers
+ Case conversion utilities
+ String formatting and templates

**DateTime Tags** — Time formatting and manipulation:
+ `{% timedelta %}` for relative time display
+ Human-readable date formatting
+ Timezone conversion helpers

**CSS/JS Tags** — Asset management helpers:
+ Conditional asset loading
+ Inline CSS/JS with template variables
+ Asset versioning and cache busting

**Additional Features:**
+ Form rendering helpers (quickform)
+ Conditional content blocks
+ Loop utilities and counters
+ Debug and inspection tags

---

</details>
**Functional Form Fields** — Less typing for common field types:
+ `forms.chars(max_length=100)` — CharField with cleaner syntax
+ `forms.email()` — EmailField ready to go
+ `forms.text()` — TextField for longer content
+ `forms.integer()` — IntegerField with sensible defaults
+ `forms.boolean()` — BooleanField shortcuts
+ All standard Django form fields available as functions

```python
from trim.forms import fields

class ContactForm(forms.Form):
    name = fields.chars(100)
    email = fields.email()
    message = fields.text()
    subscribe = fields.boolean(required=False)
```

**Auto Form Generation** — Generate forms from models automatically:
+ Model-to-form conversion helpers
+ Automatic field type detection
+ Include/exclude field patterns
+ Custom widget assignment

**Form Validation Helpers** — Common validation patterns:
+ Email validation shortcuts
+ Phone number validators
+ URL validation helpers
+ Custom validator composition

**Additional Features:**
+ Form widget customization helpers
+ Field ordering utilities
+ Error message customization
+ Form field grouping and layout helpers

---

</details>

### Execute

Quick database query helpers for common read patterns and execution shortcuts.

**Top Features:** [read_one](./docs/execute.md) · [Query Helpers](./docs/execute.md)

<details> <summary>Expand for full feature list</summary>

**Full Documentation:** [Execute Guide](./docs/execute.md)

---

**Read One** — Simplified single object retrieval:
+ `read_one(Model, **filters)` returns one object or None
+ No more try/except blocks for `DoesNotExist`
+ Cleaner code for common get-or-none pattern
+ Works with any Django model

```python
from trim.execute import read_one

# Instead of this:
try:
    user = User.objects.get(username='john')
except User.DoesNotExist:
    user = None

# Write this:
user = read_one(User, username='john')
```

**Query Shortcuts** — Common query patterns simplified:
+ Get or create helpers with cleaner syntax
+ First/last object retrieval
+ Existence checking utilities
+ Count shortcuts

**Execution Helpers** — Common operational patterns:
+ Bulk operation helpers
+ Transaction shortcuts
+ Query optimization utilities

**Additional Features:**
+ Model introspection helpers
+ Field value extraction
+ Related object loading shortcuts
+ Queryset composition utilities

---

</details>


---

## Philosophy

+ Generate URL patterns from view classes.
+ Readable URL helpers - generate named URL patterns from your view classes using `paths_named`
+ Dictionary and tuple patterns - build URL patterns from dictionaries or tuples with `paths_dict`.

**Docs:** [Overview](./docs/urls/readme.md) · [Helpers](./docs/urls/functions.md)

</details>

### Templates

<details> <summary>Key Features</summary>

`trim.templates` provides a set of template tags to enhance your Django templates.

+ Advanced composition with `{% link %}`, `{% wrap %}`, and `{% slot %}`.
+ Generate hyperlinks to views with `{% link viewname arguments label %}`
+ Slottable, importable includes with the `wrap` tag
+ String manipulation and utility tags

**Docs:** [Link](./docs/templates/tags/link/readme.md) · [Wrap](./docs/templates/tags/wrap.md) · [Wrap/Slot](./docs/templates/tags/wrap-slots.md) · [Strings](./docs/templates/tags/strings.md) · [Updated Params](./docs/templates/tags/updated-params.md) · [CSS/JS](./docs/templates/tags/css-js-tag.md)

</details>

### Admin

<details> <summary>Key Features</summary>

+ Register all models in an app quickly.
+ Instantly and automatically generate admin views for all your models

**Docs:** [Admin](./docs/admin.md)

</details>

### Execute

<details> <summary>Key Features</summary>

+ Minimal helpers for common execution patterns.
+ Quick database query helpers

**Docs:** [Execute · read_one](./docs/execute.md)

</details>


---

## Philosophy

I aim for the _Trim_ philosophy "convenient and thoughtless" - where a function or method should be quick to type, until I'm ready to replace them with the django builtins.


## License

This project is licensed under the terms of the MIT License.

The MIT License offers you the freedom to use, modify, and distribute this code. While it's not a formal requirement, taking a moment to acknowledge the original contributors reflects a deep-seated respect that is fundamental to the open-source community.

## Contributing

We sincerely welcome contributions! There is no barrier for entry and all input is valid input. If you find a bug or have a feature request, please open an issue. If you'd like to contribute code, please fork the repository and submit a pull request.

---

Open-source is as much about collaboration and mutual respect as it is about code. As a project committed to this ethos, we promise to always recognize and credit contributions with gratitude and respect.

We value the thoughtfulness and care put into each contribution, not to reduce them to mere numbers or to brush them off with a cavalier _"...that's what open source is..."_. A project thrives on its community's spirit and collective efforts.
