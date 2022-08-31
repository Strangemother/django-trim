from django.forms import widgets
from django.forms.widgets import *


def checkboxes(*a, **kw):
    return widgets.CheckboxSelectMultiple(*a, **kw)


def textarea(*a, **kw):
    return widgets.Textarea(*a, **kw)


def password(*a, **kw):
    return widgets.PasswordInput(*a, **kw)


def radios(*a, **kw):
    return widgets.RadioSelect(*a, **kw)

