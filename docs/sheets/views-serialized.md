# Views: JSON and Serialized Responses

`trim.views.serialized` provides JSON response mixins and class-based views for returning ordinary Python data or serialized Django model results.

## Import

```py
from trim.views import JsonDetailView, JsonListView, JsonView
from trim.views.serialized import JSONResponseMixin, JSONListResponseMixin
```

## JsonView

Use `JsonView` when the response data is assembled by the view:

```py
class HealthView(JsonView):
    prop = "status"

    def get_data(self):
        return {"ok": True}
```

The response is `{"status": {"ok": true}}`. Set `prop = None` to return the data without a wrapper.

| Method | Example | Purpose |
| --- | --- | --- |
| `get_data` | `return {"ok": True}` | Supplies the Python value to encode as JSON. |
| `get_serialiser` | `serialiser = self.get_serialiser()` | Returns a `JsonSerializer`. |
| `render_to_json_response` | `return self.render_to_json_response(data)` | Returns a Django `JsonResponse`. |

## JsonListView

Use `JsonListView` for a collection of model objects:

```py
class ProductJsonListView(JsonListView):
    model = Product
    fields = ("id", "name", "price")
```

The default response property is `object_list` and includes a `count` value. Override `get_results()` to customize the queryset and `response_extra` to add fixed response data.

```py
class ProductJsonListView(JsonListView):
    model = Product
    prop = "products"
    response_extra = {"version": 1}

    def get_results(self):
        return Product.objects.filter(is_active=True)
```

## JsonDetailView

Use `JsonDetailView` for one model object selected by the URL `pk`:

```py
class ProductJsonDetailView(JsonDetailView):
    model = Product
    fields = ("id", "name", "price")
```

The response property defaults to `object`. Override `generate_response()` or `get_results()` for custom lookup/serialization.

```py
class ProductJsonDetailView(JsonDetailView):
    model = Product
    prop = "product"

    def get_results(self):
        return Product.objects.get(slug=self.kwargs["slug"])
```

## Mixins

| Mixin | Example | Purpose |
| --- | --- | --- |
| `JSONResponseMixin` | `class ApiView(JSONResponseMixin, views.TemplateView): ...` | Adds `render_to_json_response()` and a default `get_data()`. |
| `JSONListResponseMixin` | `class ApiList(JSONListResponseMixin, views.View): ...` | Serializes result collections and selects model fields. |
| `JsonSerializer` | `serializer = JsonSerializer()` | Python serializer whose default dump object is an empty mapping. |

`JSONListResponseMixin.fields` defaults to `None`, which means all available dictionary keys or model fields are selected. Set it to a tuple/list of names to restrict output.

| Method | Example | Purpose |
| --- | --- | --- |
| `get_dump_object` | `data = self.get_dump_object(product)` | Builds the field mapping for one object. |
| `get_serialiser` | `serialiser = self.get_serialiser()` | Creates a serializer configured with `get_dump_object`. |
| `serialize_result` | `data = self.serialize_result(queryset)` | Converts a result iterable into serialized Python data. |
| `get_response_extra` | `extra = self.get_response_extra(result)` | Adds count and configured `response_extra` data. |
| `json_response` | `return self.json_response(product)` | Builds and returns a detail JSON response. |
| `generate_response` | `data = self.generate_response(product)` | Builds the detail response mapping before rendering. |

All JSON values must be serializable by Django's `JsonResponse`. Treat `fields` as an API contract and avoid exposing private or sensitive model attributes.
