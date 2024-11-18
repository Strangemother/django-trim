# Serialized (JSON) Views

> `trim.views.serialized` views renders models to responses as JSON.


```py
from trim.views import JsonView, JsonListView, JsonDetailView

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


class ExampleJsonListView(JsonListView):
    """ returns:
        {
            "object_list": [...]
        }
    """
    model = models.MyModel

````


## `trim.views.JsonView`

Instantly create JSON responses (without the Django Serializer). By default the
`prop` is `"object"`. If _`None`_, the result is not nested:

```py
from trim.views import JsonView

class HostIncomingJSONView(views.JsonView):
    prop = 'biscuit'

    def get_data(self):
        return {
            'ok': True
            , 'hello': 'world'
        }
```

    {
        "biscuit": {
            "hello": "world",
            'ok': True
        }
    }
