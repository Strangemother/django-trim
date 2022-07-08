from django.apps import apps


__ALL__ = (
    'get_model'
)


def get_model(*a, **kw):
    return apps.get_model(*a, **kw)
