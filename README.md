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
| [Templates](./docs/templates/) | [`{% link %}` tag](./docs/templates/tags/link/readme.md) \| [`{% wrap %}` tag](./docs/templates/tags/wrap.md) \| [`{% slot %}` Tag](./docs/templates/tags/wrap-slots.md) \| [`{% updated_params %}` tag](./docs/templates/tags/updated_params.md) \| [`{% functional %}` tag](./docs/templates/tags/functional.md) \| [`{% timedelta %}` tag](./docs/templates/tags/datetime.md) |
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
+ **Auto composition** - mix behaviour across apps into existing models without modifying their definitions. [Auto Model Mixin](./docs/models/auto_model_mixin.md)
+ **Live model access** - lazy access to any installed model via `trim.live.myapp.ModelName`; no circular imports.

All `trim.models.fields` shadow the standard Django field for functional - guessable - and completely interchangable. [Read more in Fields](./docs/models/fields.md)

It works with any model, allowing you to apply methods on models without manipulating the original model definition (such as the `User` model)


You never need to `import` your models. Take a look in [Live String Docs](./docs/models/live.md)


```py
from django.db import models
from trim.models import fields, AutoModelMixin


class HenBasket(models.Model):
    chicken = fields.fk('Chicken')
    full = fields.bool_false()
    eggs = fields.int(6)
    owner = fields.user_fk()
    created, updated = fields.dt_cu_pair()

# Mix behaviour into an existing model
class UserHenBasketsAutoMixin(AutoModelMixin):
    def get_baskets(self):
        return HenBasket.objects.filter(owner=self) # Is a mixin on User

    class Meta:
        # model_name = get_user_model()
        model_name = "user.User" # Target any name or model.
```

```py
# Using the hoisted model
>> from trim.models import get_user_model
>>> User = get_user_model()
>>> User.objects.first().get_baskets()
[<baskets.HenBasket object(2)>, <baskets.HenBasket object(3)>]

>>> from trim import live
>>> live.baskets.HenBasket.objects.filter(id=3).get()
<baskets.HenBasket object(3)>
```

## Views

> Django Trim embraces class-based-views and bundles a set of useful integration mixins and trim tools

+ Instant View Permissioning
+ JSON Views | Markdown Views

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

from trim.views import JsonListView, JsonDetailView

class ExampleJsonListView(JsonListView):
    # A list of JSON objects /items/
    model = models.MyModel

class ExampleJsonDetailView(views.UserOwnedMixin, JsonDetailView):
    # A single object, /items/<str:pk>/
    model = models.MyModel


from trim.markdown.response import MarkdownTemplateResponse

class MarkdownReponseIndexView(views.TemplateView):
    response_class = MarkdownTemplateResponse
    template_name = "contact/index.md"
```

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

## Forms

Forms can be tedious. Django Trim offers functional fields, site-wide form template tags and more.

+ **[Form Fields](./docs/forms/fields-auto.md)**: Functional shortcuts for all Django form fields - less typing, same functionality
+ **Quickform**: Zero Config, Any Time, Plugged Correctly. Instantly install prepared forms into a view, utilising the form built-into the class-based `FormView`

```jinja
{% load quickforms %}

{# A rendered form, posted to /myapp/formview-name/ #}
{% quickform.form "app:formview-name" %} <!-- Ready to go POST form -->


<form>
{% quickform "app:formview-name" %} <!-- synonymous to {{ form.as_ul }} -->
</form>

```


## URLs

+ Readable URL helpers - generate named URL patterns from your view classes using `paths_named`
+ Dictionary and tuple patterns - build URL patterns from dictionaries or tuples with `paths_dict`.

```py
from trim.urls import paths_named
from . import views

app_name = 'screenshots'

urlpatterns = paths_named(views,
    # {% link "screenshots:index" "Index Page" %}
    index=('ScreenshotIndexView', '',),
    create=('ScreenshotFormView', 'new/',),
    form_success=('ScreenshotFormSuccessView', 'success/<str:id>/',),

    # {% link "screenshots:info" object.id "Screenshot Info" %}
    info=('ScreenshotRequestUpdateView', 'info/<str:id>/',),
)
```

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

> [!TIP]
> Explore the [And so much more](./docs/) directory for full documentation and many more features.


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

