
from ..forms import list as forms
from django.utils.functional import cached_property
from django.views.generic import ListView

class OrderPaginatedListView(ListView):
    """A ListView with prepared ordering and pagination.
    """
    default_orderby = 'default_orderby_field'
    default_selected_orderby = 'name'
    default_direction = 'asc'
    ordering = f'{default_orderby}'

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

    def get_ordering_fields(self, expand=False):
        r = ()
        for k, v in self.ordering_fields:
            if (not expand) and isinstance(v,(tuple,list)):
                v = v[0]
            r += ( (k,v,), )
        return r

    def get_form(self):
        return forms.ListForm(self.request.GET)

    @cached_property
    def filter_data(self):
        return self.get_filter_data()

    def get_filter_data(self):
        f = self.get_form()
        if f.is_valid():
            d = f.cleaned_data
            d = self.format_internal(d)
            return d

        return {}

    def get_orderby_field(self, d):
        field = d.get('order_by', self.default_orderby)
        row = dict(self.get_ordering_fields(expand=True)).get(field)
        if row is None:
            # bad field.
            return self.default_orderby
        if isinstance(row, tuple):
            return row[1]
        return row
        # return field

    def get_selected_orderby(self):
        return self.filter_data.get(self.order_by_field, None) or self.default_selected_orderby

    def get_selected_direction(self):
        return self.filter_data.get(self.direction_field, None) or self.default_direction

    def format_internal(self, data):
        """Convert the form dict into something internal.
        """
        field = self.get_orderby_field(data)
        direction = data.get(self.direction_field, None)
        direction = dict(self.direction_fields).get(direction, None) or ''
        # direction = '' if direction else '-'

        ds = f'{direction}{field}'
        data['ordering'] = ds
        print('Order', ds)
        data.setdefault('paginate_by', self.paginate_by)
        user_pagination = self.clamp_paginate_by(data.get(self.paginate_by_field, None) or None)
        if user_pagination is not None:
            data['paginate_by'] = user_pagination
        return data

    def get_ordering(self):
        v = self.filter_data.get('ordering', '')
        if v is None or len(v) == 0:
            return self.ordering
        return v

    def get_paginate_by(self, queryset=None):
        v = self.paginate_by
        r = self.clamp_paginate_by(v)
        return self.filter_data.get('paginate_by', r)

    def clamp_paginate_by(self, v):
        return min(max(self.min_paginate_by, v or 0), self.max_paginate_by)
