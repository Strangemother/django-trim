

## Order Paginated ListView

A Listview with the pagination, ordering, and _GET_ form intergration.

+ Ordering
+ Pagination
+ Form submission

Replace a `ListView` with an `OrderPaginatedListView` and you're good to go:

```py
from trim import OrderPaginatedListView

class ShoppingCardListView(OrderPaginatedListView):
    """A ListView with prepared ordering and pagination.
    """
    default_orderby = 'title' # any applicable field.
    default_selected_orderby = 'name' # any applicable field
    default_direction = 'asc'

    min_paginate_by = 10
    max_paginate_by = 200
    paginate_by = 50

    order_by_field = 'order_by'
    paginate_by_field = 'count'
    direction_field = 'direction'

    ordering_fields = (
        # ext. val, ext. label, int. key
        ('name', ('Name', 'short_description')),
        ('cost', ('Price', 'cached_current_price',)),
        ('product', ('Product ID', 'product_id')),
    )

    direction_fields = (
        ('asc', '',),
        ('desc', '-',),
    )
```

The _submit_ your form fields. The _names_ of the fields are shadowed as to not announce the backend stack:

+ `count`: int page count
+ `page`: int current page
+ `direction`: asc | desc

In the URL:

    http://localhost:8000/cart/?page=2&count=10&direction=asc

---

Under the hood this uses `trim.forms.list.ListForm` for GET Form parsing (nice and safe.)