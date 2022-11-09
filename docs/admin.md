# Admin

Instantly and automatically generate admin views for incoming models.

```py
from django.contrib import admin
from trim import admin as t_admin

from . import models

t_admin.register_models(models)
```

Or use the model detection functions to use the standard admin site register function:

_admin.py_
```py
from django.contrib import admin
from trim.models import grab_models
from . import models
# Register all discovered models, ignoring any indirect imports
admin.site.register(grab_models(models, ignore=['User']))
```
