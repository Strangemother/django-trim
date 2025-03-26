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

## Ignoring existing ModelAdmin

Django prohibits registering a model more than once. If you have existing `ModelAdmin` interfaces, _ignore_ their associated models to ensure compatibility:

```py
from django.contrib import admin
from trim import admin as t_admin

from . import models

@admin.register(models.FlowStep)
class FlowStepAdmin(admin.ModelAdmin):
    list_display = ('question', 'index', 'seen', 'answered')


@admin.register(models.UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'awarded_score', 'is_correct')



@admin.register(models.UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choices', 'score', 'is_correct')

t_admin.register_models(models,
        # Ignore already registered models.
        ignore=['UserScore', 'UserAnswer', 'FlowStep']
    )
```


