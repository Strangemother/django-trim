

## favicon_path

Implement your favicon as a static redirect

```py
# (primary) urls.py
from trim.urls import favicon_path

urlpatterns = [
    ...
    favicon_path('favicon.ico'),
]
```

## Other Functions

+ path_include
+ paths_named
+ paths_tuple
+ paths_dict
+ template_view
+ as_templates
+ error_handlers