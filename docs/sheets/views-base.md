# Views: Base and Generators

`trim.views.base` provides shared mixins, model discovery, and dynamic class generators for common model views. Generated classes are inserted into the requested module and can be used like ordinary Django class-based views.

## Import

```py
from trim import views
from trim.views import base
```

Most applications only need the public facade:

```py
from trim.views import crud, history
```

## Django View Classes

These Django generic views are imported and exposed by the module:

```py
class ProductListView(views.ListView):
    model = Product

class ProductDetailView(views.DetailView):
    model = Product
```

Commonly available classes include `View`, `TemplateView`, `FormView`, `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`, and the date archive views. They retain Django's normal behavior and options.

`Permissioned` is an alias for Django's `PermissionRequiredMixin`:

```py
class EditProductView(views.Permissioned, views.UpdateView):
    model = Product
    fields = "__all__"
    permission_required = "catalog.change_product"
```

## Shared Helpers

| Helper | Example | Purpose |
| --- | --- | --- |
| `first_bit` | `app = views.first_bit("catalog.products")` | Returns the first dot-separated component, such as `catalog`. |
| `extract_location` | `app, prefix, name = views.extract_location(Product)` | Returns the app name, lower-case first name component, and class name used by generators. |
| `ensure_tuple` | `models = views.ensure_tuple(Product)` | Wraps a non-list/tuple value in a one-item tuple. |
| `copy_update` | `props = views.copy_update({"model": Product}, fields="__all__")` | Copies a mapping and applies additional values. |
| `create_class_slot` | `slot = views.create_class_slot(views.ListView, model=Product)` | Builds the internal mixin/class-definition pair used by generators. |

These helpers are useful when extending the generators; normal view declarations usually do not need them.

## CRUD Generation

`crud(model, ...)` creates five classes in this order: list, create, update, detail, and delete.

```py
from catalog.models import Product
from trim.views import crud

ProductListView, ProductCreateView, ProductUpdateView, ProductDetailView, ProductDeleteView = crud(
    Product,
    class_module_name=__name__,
)
```

Defaults applied by `crud`:

- `model` is assigned to every generated class.
- Create and update views use `fields = "__all__"`.
- Delete, create, and update views use a success URL based on `<app>:<model>-list` unless `success_url` is supplied.
- Generated names follow `<ModelName><ParentViewName>`, such as `ProductListView`.

Provide shared class attributes with keyword arguments:

```py
crud(
    Product,
    class_module_name=__name__,
    template_name="catalog/product_form.html",
    success_url="catalog:product-list",
)
```

## CRUD Generation for Multiple Models

`crud_classes` repeats `crud` for one or more models. If `model_class` is omitted, it discovers models using the target module and installed Django apps.

```py
views = crud_classes(
    target_name=__name__,
    model_class=(Product, Category),
    class_module_name=__name__,
)
```

Useful arguments:

- `model_class`: one model or an iterable of models.
- `models`: explicit fallback model collection for discovery.
- `module_needles`: module names to restrict discovery, or `False`/`"__ALL__"` to disable filtering.
- `success_url` and `success_url_bit`: control generated success URLs.
- Additional keyword arguments become class attributes.

## History View Generation

The `history` helper creates date-based archive views:

```py
from trim.views import history

ProductArchiveView, ProductDateDetailView, ProductDayArchiveView, ProductMonthArchiveView, ProductTodayArchiveView, ProductWeekArchiveView, ProductYearArchiveView = history(
    Product,
    class_module_name=__name__,
    date_field="created",
)
```

`history_classes` repeats this generation for multiple models:

```py
archive_views = views.history_classes(
    target_name=__name__,
    model_class=(Product, Category),
    class_module_name=__name__,
    date_field="created",
)
```

The generated classes use Django's `ArchiveIndexView`, `DateDetailView`, `DayArchiveView`, `MonthArchiveView`, `TodayArchiveView`, `WeekArchiveView`, and `YearArchiveView`.

## Lower-Level Generation

| Helper | Example | Purpose |
| --- | --- | --- |
| `discover_models` | `models = views.discover_models(__name__, models=[Product])` | Finds installed models for a target app/module. |
| `gen_thin_packs` | `packs = views.gen_thin_packs((views.ListView,), {"model": Product})` | Builds generator input packs. |
| `thin_parts_gen` | `view = views.thin_parts_gen((views.ListView,), "Product", {"model": Product}, __name__)` | Builds generated classes from view parts. |
| `gen_packed_views` | `view = views.gen_packed_views("Product", __name__, packs)` | Creates classes from packed definitions. |
| `gen_class` | `view = views.gen_class("Product", (views.ListView,), {"model": Product}, __name__)` | Dynamically creates and registers one view class. |

`gen_class` uses `safe=True` by default and returns an existing class with the same generated name rather than replacing it. Pass `safe=False` only when replacement is intentional.

## ShortMixin

`ShortMixin` adds Trim's template lookup conventions and a `model_name` context value:

```py
class ProductListView(views.ShortMixin, views.ListView):
    model = Product
```

The mixin checks the normal Django template name, then `crud/<name>.html`, mapped-name variants, and Trim's built-in CRUD templates.
