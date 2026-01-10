"""
The "live" models tool provides a fast access method to all the existing
installed models using a single concat string, resolving to the model.

This can replace a standard model import, or the django get_model import:


with get_model:

    from django.apps import apps

    ShippingAccount = apps.get_model('baskets.ShippingAccount')
    cart_owner = self.get_object().cart.owner
    user_addresses = ShippingAccount.objects.filter(owner=cart_owner, deleted=False)

after:

    from trim import live

    owner = self.get_object().cart.owner
    user_addresses = live.baskets.ShippingAccount.objects.filter(
            owner=owner, deleted=False
        )
"""

from django.apps import apps


class MagicModelApp(object):
    """The top level 'live' model import, expecting a string caller:

    live = MagicModelApp()
    live.appname

    """

    def __getattribute__(self, k):
        # Use __getattribute__ to intercept all attribute access, not just missing ones
        # This allows us to properly raise AttributeError for special attributes
        # before __getattr__ is even called
        if k.startswith("_") or k in (
            "__class__",
            "__dict__",
            "__wrapped__",
            "__name__",
            "__qualname__",
        ):
            # Delegate to parent for special attributes
            return object.__getattribute__(self, k)
        # Return a MagicModelModel for app name lookups
        return MagicModelModel(k)


class MagicModelModel(object):
    """A return value from the live appname collection, returning
    a model upon a key call:

        live.appname.ModelName
        <appname.ModelName>
    """

    def __init__(self, appname):
        object.__setattr__(self, "appname", appname)

    def __getattribute__(self, k):
        # Use __getattribute__ to intercept all attribute access
        if k.startswith("_") or k in ("appname",):
            # Allow access to our internal appname attribute
            # Delegate to parent for special attributes
            return object.__getattribute__(self, k)
        # Return the model from Django's registry
        appname = object.__getattribute__(self, "appname")
        return apps.get_model(appname, k)


# class MagicModelProps(object):

#     def __init__(self, appname, modelname):
#         self.appname = appname
#         self.modelname = modelname

#     def __getattr__(self, k):

live = MagicModelApp()
