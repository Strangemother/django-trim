# Views: Ordering and Pagination

`OrderPaginatedListView` in `trim.views.list` extends Django's `ListView` with query-string ordering and bounded pagination.

## Import

```py
from trim.views import OrderPaginatedListView
```

## Basic Usage

```py
class ProductListView(OrderPaginatedListView):
    model = Product
    ordering_fields = (
        ("name", ("Name", "short_description")),
        ("cost", ("Price", "cached_current_price")),
    )
```

The view reads these query-string fields by default:

| Setting | Default | Meaning |
| --- | --- | --- |
| `order_by_field` | `"order_by"` | Selected key from `ordering_fields`. |
| `paginate_by_field` | `"count"` | Requested page size. |
| `direction_field` | `"direction"` | Selected key from `direction_fields`. |
| `default_orderby` | `"default_orderby_field"` | Fallback ordering field. |
| `default_selected_orderby` | `"name"` | Selected ordering key when none is supplied. |
| `default_direction` | `"asc"` | Fallback direction. |
| `min_paginate_by` | `10` | Smallest accepted page size. |
| `max_paginate_by` | `200` | Largest accepted page size. |
| `paginate_by` | `50` | Default page size. |

## Ordering Configuration

Each `ordering_fields` item is `(query_key, label_or_definition)`:

```py
class ProductListView(OrderPaginatedListView):
    ordering_fields = (
        ("name", ("Name", "short_description")),
        ("cost", ("Price", "cached_current_price")),
    )
    direction_fields = (("asc", ""), ("desc", "-"))
```

`get_ordering()` returns the validated field with its direction prefix, such as `"short_description"` or `"-cached_current_price"`. Unknown ordering keys fall back to `default_orderby`.

## Methods

| Method | Example | Purpose |
| --- | --- | --- |
| `get_ordering_fields` | `fields = self.get_ordering_fields(expand=True)` | Returns configured ordering keys and values; expanded values include the underlying field name. |
| `get_form` | `form = self.get_form()` | Returns `trim.forms.list.ListForm(self.request.GET)`. |
| `get_filter_data` | `data = self.get_filter_data()` | Validates query parameters and formats them for the view. |
| `get_orderby_field` | `field = self.get_orderby_field(data)` | Resolves a requested key to its underlying model field. |
| `get_selected_orderby` | `key = self.get_selected_orderby()` | Returns the selected ordering key. |
| `get_selected_direction` | `direction = self.get_selected_direction()` | Returns the selected direction key. |
| `format_internal` | `data = self.format_internal(data)` | Adds normalized `ordering` and bounded `paginate_by` values. |
| `get_ordering` | `ordering = self.get_ordering()` | Returns the final Django ordering expression. |
| `get_paginate_by` | `size = self.get_paginate_by()` | Returns the bounded page size. |
| `clamp_paginate_by` | `size = self.clamp_paginate_by(500)` | Clamps a value to `min_paginate_by` and `max_paginate_by`. |

The view uses `cached_property` for `filter_data`, so the request query parameters are parsed once per view instance.
