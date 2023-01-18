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
