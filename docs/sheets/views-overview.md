# Views Cheat Sheets

`trim.views` combines common Django class-based views with focused helpers for CRUD generation, authentication, pagination, JSON responses, file delivery, and custom 404 handling.

The detailed sheets are split by the implementation modules:

- [Base views and generators](./views-base.md)
- [Authentication and ownership](./views-auth.md)
- [List ordering and pagination](./views-list.md)
- [JSON and serialized views](./views-serialized.md)
- [File responses](./views-download.md)
- [Custom 404 views](./views-errors.md)

## Import

For the common public surface:

```py
from trim import views
```

For a direct module import:

```py
from trim.views.serialized import JsonDetailView
```

## Basic View

```py
from trim import views

class ProductListView(views.ListView):
    model = Product
    template_name = "products/product_list.html"
```

`trim.views` re-exports many Django generic views, including `View`, `TemplateView`, `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`, and `FormView`. They behave like their Django equivalents. The Trim-specific helpers are documented in the linked sheets.
