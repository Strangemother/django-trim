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
    def __getattr__(self, k):
        return MagicModelModel(k)


class MagicModelModel(object):
    """A return value from the live appname collection, returning
    a model upon a key call:

        live.appname.ModelName
        <appname.ModelName>
    """
    def __init__(self, appname):
        self.appname = appname

    def __getattr__(self, k):
        return apps.get_model(self.appname, k)


# class MagicModelProps(object):

#     def __init__(self, appname, modelname):
#         self.appname = appname
#         self.modelname = modelname

#     def __getattr__(self, k):

live = MagicModelApp()
