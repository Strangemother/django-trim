"""
Register your models in the admin -

    from django.contrib import admin
    from short import admin as shorts

    from . import models

    shorts.register_models(models)

"""

from django.contrib import admin

# Register your models here.
from .models import grab_models, cache_known


def register_models(models, ignore=None):
    """Register a list of models within the standard admin site register,
    calling upon short.models.grab_models() to detect the inbound models.

    Provide an ignore list to omit models from the register; in such cases as
    model pollution from app imports, or modeladmin customisation.

    string method:

        shorts.register_models(models, ignore=['GenericProduct'])

    models:

        shorts.register_models(models, ignore=[models.GenericProduct])

    With model register detection:

        shorts.register_models(models, ignore=__name__)

    Use `ignore=__name__` in conjunction with the `@short.admin.register`
    """
    return admin.site.register(grab_models(models, ignore=ignore))


def register(*a, **kw):
    """Perform a standard django `admin.register(Model)` with the model being
    _cached_ for later assessment duringthe grab models ignore filters.

    Replace `admin.register` with `shorts.register`:

        from django.contrib import admin
        from short import admin as shorts
        from . import models

        # Standard
        @admin.register(models.GenericProduct):
        class GenericProductAdmin(admin.ModelAdmin):
            pass


    Exactly the same through shorts:

        from django.contrib import admin
        from short import admin as shorts
        from . import models

        @shorts.register(models.GenericProduct)
        class GenericProductAdmin(admin.ModelAdmin):
            pass

    Utilising `shorts.register` captures the used model, therefore when
    registering generic model views, the `ignore` method may identify the module
    names to exclude:

    The standard django method:

        from . import models
        admin.site.register(models.GenericProduct,
                            models.OtherModel,
                            models.AnotherModel, ...)


    short method allows importing of _all_ models:

        from . import models
        shorts.register_models(models)

    Ignore previously registered models:

        shorts.register_models(models,
                ignore=['GenericProduct', models.Anothermodel])


    or better-yet, use the model register. The `ignore` attribute identifies
    the _current_ module e.g. `products.admin`.

        # within admin.py
        shorts.register_models(models, ignore=__name__)

        ## Synonymous to
        shorts.register_models(models, ignore='products.admin')

    Any model previously utilised by `@shorts.register` for the products module
    is automatically exlcuded.
    """
    cache_known(*a)
    return admin.register(*a, **kw)
