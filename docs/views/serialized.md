# Serialized (JSON) Views

Quickly build JSON API views with minimal boilerplate. `trim.views.serialized` provides Django class-based views that render models and data as JSON responses, bypassing Django's complex serializer framework for simple use cases.

## Table of Contents

+ [JsonView](#jsonview) - Generic JSON response view
+ [JsonListView](#jsonlistview) - List all model objects as JSON
+ [JsonDetailView](#jsondetailview) - Single model object as JSON
+ [Customization](#customization)
+ [Best Practices](#best-practices)

---

## JsonView

Create arbitrary JSON responses without templates or Django's serializer. Perfect for custom API endpoints and simple JSON data.

### Basic Usage

```py
from trim.views import JsonView

class ApiStatusView(JsonView):
    def get_data(self):
        return {
            'status': 'ok',
            'version': '1.0.0'
        }
```

**Response:**
```json
{
    "object": {
        "status": "ok",
        "version": "1.0.0"
    }
}
```

### Configuration Options

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `prop` | `str` | `'object'` | Root key name for wrapping response data |

### Unwrapped Response

Set `prop = None` to return data without a wrapper key:

```py
class UnwrappedJsonView(JsonView):
    prop = None

    def get_data(self):
        return {
            'ok': True,
            'message': 'Direct response'
        }
```

**Response:**
```json
{
    "ok": true,
    "message": "Direct response"
}
```

### Custom Wrapper Key

```py
class CustomWrapperView(JsonView):
    prop = 'payload'

    def get_data(self):
        return {'hello': 'world'}
```

**Response:**
```json
{
    "payload": {
        "hello": "world"
    }
}
```

### Dynamic Data

```py
class UserStatsView(JsonView):
    prop = 'stats'

    def get_data(self):
        user_count = User.objects.count()
        active_count = User.objects.filter(is_active=True).count()
        
        return {
            'total_users': user_count,
            'active_users': active_count,
            'timestamp': timezone.now().isoformat()
        }
```

---

## JsonListView

Serialize a queryset of model objects to JSON. Ideal for listing resources in a JSON API.

### Basic Usage

```py
from trim.views import JsonListView

class ProductListJsonView(JsonListView):
    model = models.Product
```

**Response:**
```json
{
    "object_list": [
        {"id": 1, "name": "Widget", "price": "9.99"},
        {"id": 2, "name": "Gadget", "price": "19.99"}
    ],
    "count": 2
}
```

### Configuration Options

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `Model` | `None` | Django model to query |
| `prop` | `str` | `'object_list'` | Root key name for wrapping the list |
| `fields` | `tuple/list` | `None` | Specific fields to include (or `'__all__'`) |
| `response_extra` | `dict` | `None` | Additional data to include in response |

### Selecting Specific Fields

Control which fields are serialized:

```py
class ProductListJsonView(JsonListView):
    model = models.Product
    fields = ('id', 'name', 'price', 'created')
```

**Response:**
```json
{
    "object_list": [
        {"id": 1, "name": "Widget", "price": "9.99", "created": "2025-01-15T10:30:00Z"}
    ],
    "count": 1
}
```

### Custom Queryset

Override `get_results()` for filtered or custom queries:

```py
class ActiveProductListView(JsonListView):
    model = models.Product
    fields = ('id', 'name', 'price')

    def get_results(self):
        return self.model.objects.filter(active=True).order_by('-created')
```

### Adding Extra Response Data

Include metadata or related data using `response_extra`:

```py
class ProductListJsonView(JsonListView):
    model = models.Product
    fields = ('id', 'name', 'price')
    response_extra = {'api_version': '2.0'}

    def get_response_extra(self, result):
        base = super().get_response_extra(result)
        base['total_value'] = sum(p.price for p in result)
        return base
```

**Response:**
```json
{
    "object_list": [
        {"id": 1, "name": "Widget", "price": "9.99"}
    ],
    "count": 1,
    "api_version": "2.0",
    "total_value": "9.99"
}
```

### Custom Serialization

Override `serialize_result()` for complete control over serialization:

```py
class CustomProductListView(JsonListView):
    model = models.Product

    def serialize_result(self, result):
        # Return just IDs and names
        return [
            {'id': product.id, 'name': product.name.upper()}
            for product in result
        ]
```

---

## JsonDetailView

Serialize a single model object to JSON. Automatically handles object lookup by primary key.

### Basic Usage

```py
from trim.views import JsonDetailView

class ProductDetailJsonView(JsonDetailView):
    model = models.Product
```

**URL Pattern:**
```py
from django.urls import path

urlpatterns = [
    path('api/products/<int:pk>/', ProductDetailJsonView.as_view(), name='product-detail-json'),
]
```

**Response for `/api/products/1/`:**
```json
{
    "object": {
        "id": 1,
        "name": "Widget",
        "price": "9.99",
        "description": "A useful widget"
    }
}
```

### Configuration Options

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `Model` | `None` | Django model to query |
| `prop` | `str` | `'object'` | Root key name for wrapping the object |
| `fields` | `tuple/list` | `None` | Specific fields to include |

### Selecting Specific Fields

```py
class ProductDetailJsonView(JsonDetailView):
    model = models.Product
    fields = ('id', 'name', 'price', 'created')
```

### Custom Object Lookup

Override `get_results()` for custom lookup logic:

```py
class ProductBySlugJsonView(JsonDetailView):
    model = models.Product
    
    def get_results(self):
        slug = self.kwargs.get('slug')
        return self.model.objects.get(slug=slug)
```

**URL Pattern:**
```py
path('api/products/<slug:slug>/', ProductBySlugJsonView.as_view()),
```

### Direct JSON Response

Call `json_response()` directly for manual response generation:

```py
class ConditionalProductView(JsonDetailView):
    model = models.Product

    def get(self, request, *args, **kwargs):
        product = self.get_results()
        
        if not product.is_available:
            return JsonResponse({'error': 'Product unavailable'}, status=404)
        
        return self.json_response(obj=product)
```

---

## Customization

### Custom Serialization Logic

All JSON views use a `JsonSerializer` class internally. Override `get_serialiser()` and `get_dump_object()` for advanced control:

```py
class CustomizedListView(JsonListView):
    model = models.Product
    fields = ('id', 'name', 'price')

    def get_dump_object(self, obj):
        """Customize how each object is serialized."""
        return {
            'id': obj.id,
            'name': obj.name.upper(),
            'price': float(obj.price),
            'url': self.request.build_absolute_uri(obj.get_absolute_url())
        }
```

### Custom Response Class

Override `render_to_json_response()` to customize the `JsonResponse`:

```py
from django.http import JsonResponse

class CorsJsonView(JsonView):
    def render_to_json_response(self, context, **response_kwargs):
        response = JsonResponse(context, **response_kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response
```

---

## Best Practices

### 1. Use for Simple APIs

These views are perfect for:
- Simple CRUD JSON APIs
- Internal AJAX endpoints
- Lightweight microservices

For complex APIs with validation, nested serialization, and advanced features, consider Django REST Framework.

### 2. Field Selection

Always specify `fields` for production code to avoid exposing sensitive data:

```py
class UserListJsonView(JsonListView):
    model = User
    fields = ('id', 'username', 'email')  # Don't expose password hash!
```

### 3. Queryset Optimization

Use `select_related()` and `prefetch_related()` in `get_results()`:

```py
class OrderListJsonView(JsonListView):
    model = models.Order

    def get_results(self):
        return self.model.objects.select_related('customer').prefetch_related('items')
```

### 4. Error Handling

Add error handling for production:

```py
class SafeDetailJsonView(JsonDetailView):
    model = models.Product

    def get_results(self):
        try:
            return self.model.objects.get(pk=self.kwargs['pk'])
        except self.model.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        obj = self.get_results()
        if obj is None:
            return JsonResponse({'error': 'Not found'}, status=404)
        return self.json_response(obj=obj)
```

### 5. Combine with Permissions

Use authentication mixins for secured endpoints:

```py
from trim.views import JsonListView, Permissioned

class ProtectedProductListView(Permissioned, JsonListView):
    model = models.Product
    permission_required = 'products.view_product'
    fields = ('id', 'name', 'price')
```

---

## Quick Reference

```py
from trim.views import JsonView, JsonListView, JsonDetailView

# Generic JSON response
class DataView(JsonView):
    prop = 'data'  # or None for unwrapped
    def get_data(self):
        return {'key': 'value'}

# List of model objects
class ListAPI(JsonListView):
    model = MyModel
    fields = ('id', 'name')  # optional
    
    def get_results(self):  # optional
        return self.model.objects.filter(active=True)

# Single model object
class DetailAPI(JsonDetailView):
    model = MyModel
    fields = ('id', 'name', 'details')  # optional
```
