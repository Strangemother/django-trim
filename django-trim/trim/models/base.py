# from django.db import models

# Create your models here.
from django.db import models as django_models
import inspect

def is_model(name, unit):
    if name.startswith('__'):
        return False

    if inspect.isclass(unit):
        return django_models.Model in inspect.getmro(unit)

    return False

MODEL_CACHE = {}

def cache_known(*_models):
    for m in _models:
        MODEL_CACHE[m._meta.label] = MODEL_CACHE[m._meta.model_name] = m


def grab_models(_models, ignore=None):
    ignore = ignore or ()
    if isinstance(ignore, str):
        if ignore.endswith('.admin'):
            # filter for any cached model, starting with the
            # same key
            a = ignore.split('.')[0]
            a_dot = f'{a}.'
            keep = {y for x,y in MODEL_CACHE.items() if x.startswith(a_dot)}
            ignore = tuple(keep)

    items = ()

    for name in dir(_models):
        unit = getattr(_models, name)
        meta = getattr(unit, '_meta', None)
        if ((name in ignore)
             or (unit in ignore)
             or (meta and (meta.abstract is True))):
            continue
        if is_model(name, unit):
            items += (unit, )
    return items


from django.apps import apps


def get_model(*a, **kw):
    return apps.get_model(*a, **kw)
