from django.forms import widgets
from django.forms.widgets import *


def checkboxes(*a, **kw):
    """A standard `widgets.CheckboxSelectMultiple` widget."""
    return widgets.CheckboxSelectMultiple(*a, **kw)


def textarea(*a, **kw):
    """A standard `widgets.Textarea` widget."""
    return widgets.Textarea(*a, **kw)


def password(*a, **kw):
    """A standard `widgets.PasswordInput` widget."""
    return widgets.PasswordInput(*a, **kw)


def radios(*a, **kw):
    """A standard `widgets.RadioSelect` widget."""
    return widgets.RadioSelect(*a, **kw)


def hidden(*a, **kw):
    """A standard `widgets.HiddenInput` widget."""
    return widgets.HiddenInput(*a, **kw)
