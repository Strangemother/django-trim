from collections import defaultdict

classes = defaultdict(tuple)

def hook_model_mixin_class(cls):
    """Given an autoloaded AutoModelMixin, stash the model against the target
    parent model. These mixings are applied at loadout.
    """
    # print('Register', cls)
    model_name = cls.Meta.model_name

    if not isinstance(model_name, str):
        _m = model_name._meta
        model_name = f"{_m.model.__module__}{_m.object_name}"
    classes[model_name] += (cls, )

def get_classes():
    return classes


class AutoModelMixin(object):
    """Apply to a class, as an extension of the target class:


        from trim.models import AutoModelMixin

        class HyperlinkList(AutoModelMixin):

            def get_hyperlinks(self):
                return Hyperlink.get_user_models(self)

            class Meta:
                # The target app 'baskets' and its model 'Cart'
                model_name = fields.get_user_model() #  'otherapp.Person'
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        hook_model_mixin_class(cls)


def hook_init_model_mixins(sender):
    # print('Hook init', sender)
    meta = sender._meta
    an = meta.app_label
    mn = meta.model_name
    on = meta.object_name

    short_model = f"{an}.{on}"
    module_model = f"{meta.model.__name__}.{meta.model.__module__}"
    model_name = f"{meta.model.__module__}{meta.object_name}"
    g = lambda x: classes.get(x, None) or ()
    lists = g(short_model) + g(module_model) + g(on) + g(model_name)
    # print(" -- > hooks: ", short_model, module_model, on, model_name)
    # print(" -- > ", len(lists))
    bind_mixins(sender, lists)


def bind_mixins(sender, lists):
    for _class in lists:
        for k in dir(_class):
            if k.startswith('_'):
                continue
            v = getattr(_class, k)
            setattr(sender, k, v)


def hook_waiting_model_mixins():
    # print('Hook models')
    # Get the classes,
    # append methods to models
    pass
