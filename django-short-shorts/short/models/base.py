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


def grab_models(_models, ignore=None):
    ignore = ignore or ()
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
