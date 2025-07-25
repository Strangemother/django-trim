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

## Popular Bits

Django trim is a facade to the common features of Django, providing a layer of sugar for all those daily tasks.

Some of our favourite components to quickly trim your code:

| Thing | Bits |
| --- | --- |
| [Models](./docs/models/)    | [Auto Model Mixin](./docs/models/auto_model_mixin.md) \| [Fields](./docs/models/fields.md) \| [Live String](./docs/models/live.md) |
| [Views](./docs/views/)     | [Authed Views](./docs/views/authed-views.md) \| [List View](./docs/views/list-views.md) \| [JSON Views](./docs/views/serialized.md) |
| [Forms](./docs/forms/)     | [quickforms](./docs/forms/quickforms.md) \| [`{% quickform %}` tag](./docs/templates/tags/quickform.md) |
| [URLs](./docs/urls/)      | [named urls](./docs/urls)  |
| Admin     | [`register_models`](./docs/admin.md)  |
| [Templates](./docs/templates/) | [`{% link %}` tag](./docs/templates/tags/link/readme.md) \| [`{% wrap %}` tag](./docs/templates/tags/wrap.md) \| [`{% slot %}` Tag](./docs/templates/tags/wrap-slots.md) |
| _Execute_ | [`read_one`](./docs/execute.md)


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
+ 100% compatible with existing Django components.

Head to the [docs/ for a list of components](./docs/), Some of our favourite features:

## Models

Use `trim.models` for easy to grab model fields, shortcuts, and fancy non-magic magic.


+ **Functional field helpers** - import fields and create model fields with fewer keystrokes. They shadow the standard Django field classes and are fully interchangeable.
+ **Auto composition** - mix behaviour across apps into existing models without modifying their definitions.
+ **Live model access** - lazy access to any installed model via `trim.live.myapp.ModelName`; no circular imports.

### Function Model Fields

All django fields have functional (guessable) names. Plus a few shortcuts to trim down those chars!

```py
from trim.models import fields


class HenBasket(models.Model):
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

> [!TIP]
> All `trim.models.fields` shadow the standard Django field and completely interchangable. [Read more in Fields](./docs/models/fields.md)

### Auto Composition

> Hoist model mixins automatically, from any installed app.

Put this anywhere (Perhaps in a fancy `shopping_addons` tool)

```py
# shopping_addons.models
from trim.models import AutoModelMixin

class StockPriceAutoMixin(AutoModelMixin):
    """Add "pricing" functionality to a "Stock" model
    """

    def get_price(self, vat=.13):
        return self.stock_price + (self.stock_price * vat)

    class Meta:
        # The target app 'baskets' and its model 'Cart'
        model_name = 'stocks.Stock'
```

```py
# Using the hoisted model
>>> from stocks.models import Stock
>>> stock = Stock(id=100)
>>> stock.stock_price # existing django field
10
>>> stock.get_price(.33) # Auto mixin.
13.3
```

It works with any model, allowing you to apply methods on models without manipulating the original model definition (such as the `User` model)

+ [Auto Model Mixin](./docs/models/auto_model_mixin.md)


### Live Model Access

> The `trim.live` models access provides a shortcut to your all installed your models without the need to import such as `trim.live.users.User()`

This allows you to call upon a model **when required**, not in the runtime startup. Allowing you to call upon _late models_ without the circular hell.

Gather any model using standard dotted notation `trim.live.myapp.ModelName`

```py
from trim import live

# Import any existing model from any app!
MyModel = live.myapp.ModelName

MyModel()
```

You never need to `import` your models. Take a look in [Live String Docs](./docs/models/live.md)

## Views

> Django Trim embraces class-based-views and bundles a set of useful integration mixins and trim tools


### Instant View Permissioning

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

### JSON Views

Quick and dirty JSON views wired into the django tooling

```py
from trim.views import JsonView, JsonListView, JsonDetailView

class ExampleJsonListView(JsonListView):
    # A list of JSON objects /items/
    model = models.MyModel

class ExampleJsonDetailView(JsonDetailView):
    # A single object, /items/<str:pk>/
    model = models.MyModel
```

Or just role your own:

```py
class ExampleJsonView(JsonView):
    """ returns:
        {
            "object": {
                "hello": "world"
            }
        }
    """
    def get_data(self):
        return {'hello': 'world'}
```

### Markdown Views

> Bored of writing HTML? Directly use markdown as templates

Django Trim offers a markdown block and some tags - for instant markdown:

```jinja
{% load markdown %}

<div>
    {% markdown %}
    # Markdown Block.

    Write markdown content within the template directly.
    {% endmarkdown %}
</div>
```

A markdown template response class for full markdown templating:

```py
from trim import views
from trim.markdown.response import MarkdownTemplateResponse

class MarkdownReponseIndexView(views.TemplateView):
    response_class = MarkdownTemplateResponse
    template_name = "contact/index.md"
```

## Forms

Forms can be tedious. Django Trim offers functional fields, site-wide form template tags and more.

### Zero Config, Any Time, Plugged Correctly.

Instantly install prepared forms into a view, utilising the form built-into the class-based `FormView`:

```jinja
{% load quickforms %}

{# A rendered form, posted to /myapp/formview-name/ #}
{% quickform.form "app:formview-name" %} <!-- Ready to go POST form -->


<form>
{% quickform "app:formview-name" %} <!-- synonymous to {{ form.as_ul }} -->
</form>

```

It's wired to your existing view (`app:formview-name`) Allowing you to build **one form endpoint** and use the form **everywhere**.


## URLs

> Managing the `urls.py` can be ugly in large apps. Django Trim helps with un-uglification for us lazy trimmers.

### Easy Readable URL Definitions

> Looking for instantly readable URLs? Trim it of course...

One of our favourite features is the _named_ style urls, where the keyword parameter is our `template_name`

```py
from trim.urls import paths_named
from . import views

app_name = 'screenshots'

urlpatterns = [] +  paths_named(views,
    # {% link "screenshots:index" "Index Page" %}
    index=('ScreenshotIndexView', '',),
    create=('ScreenshotFormView', 'new/',),
    form_success=('ScreenshotFormSuccessView', 'success/<str:id>/',),

    # {% link "screenshots:info" object.id "Screenshot Info" %}
    info=('ScreenshotRequestUpdateView', 'info/<str:id>/',),
)
```

> But perhaps a dictionary or tuple of URLs, connected to your class based views?

Dictionary flavour definitions, using the ClassName as the key:

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

urlpatterns = urls.paths_dict(views, trim_patterns)
```

Or maybe a more pure `tuple` of `tuples`:

```py
from trim import urls
from . import views

app_name = 'website'

trim_patterns = (
    ('NoteIndexView', 'index', '' ),
    ('EntryJsonList', 'entity-list-json', 'entry/list/json/' ),
    ('EntryDetailView', 'entry-detail-json', '<str:pk>/json/' ),
)

urlpatterns = urls.paths_tuple(views, trim_patterns)
```

## Admin

Instantly and automatically generate admin views for all your models

```py
from django.contrib import admin
from trim import admin as t_admin

from . import models

# register all models in this app.
t_admin.register_models(models)
```

## Template Tags

### Wrap Tag

Slottable, Importable, _includes_ with the `wrap` tag:

```jinja
{% load wrap slot %}

{% wrap "wraps/target.html" %}
    {% slot %}
        <p>Replace the default content with alternative HTML,
        no slot names needed.</p>
    {% endslot %}
{% endwrap %}
```

### Link Tag

Generate a hyperlink to a view with `{% link viewname arguments label %}`

```jinja
{% load link %}
{% link "appname:viewname" "Click this link!" %}
```

[And so much more](./docs/)!

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

