from collections import defaultdict

classes = defaultdict(tuple)

def hook_model_mixin_class(cls):
    """Given an autoloaded AutoModelMixin, stash the model against the target
    parent model. These mixings are applied at loadout.
    """
    # print('Register', cls)
    model_name = cls.Meta.model_name
    classes[model_name] += (cls, )

def get_classes():
    return classes


class AutoModelMixin(object):

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
    g = lambda x: classes.get(x, None) or ()
    lists = g(short_model) + g(module_model) + g(on)
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
