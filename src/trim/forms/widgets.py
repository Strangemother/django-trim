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


def checkbox(*a, **kw):
    """CheckboxInput"""
    return widgets.CheckboxInput(*a, **kw)


checkbox_select_multiple = checkboxes


def choice(*a, **kw):
    """ChoiceWidget"""
    return widgets.ChoiceWidget(*a, **kw)


class MultipleFileInput(widgets.ClearableFileInput):
    allow_multiple_selected = True


def clearable_file_input(*a, **kw):
    """ClearableFileInput"""
    return MultipleFileInput(*a, **kw)


def date(*a, **kw):
    """DateInput"""
    return widgets.DateInput(*a, **kw)


def date_time_base(*a, **kw):
    """DateTimeBaseInput"""
    return widgets.DateTimeBaseInput(*a, **kw)


def date_time(*a, **kw):
    """DateTimeInput"""
    return widgets.DateTimeInput(*a, **kw)


def email(*a, **kw):
    """EmailInput"""
    return widgets.EmailInput(*a, **kw)


def file(*a, **kw):
    """FileInput"""
    return widgets.FileInput(*a, **kw)


def base(*a, **kw):
    """Input"""
    return widgets.Input(*a, **kw)


def multi_widget(*a, **kw):
    """MultiWidget"""
    return widgets.MultiWidget(*a, **kw)


def multiple_hidden(*a, **kw):
    """MultipleHiddenInput"""
    return widgets.MultipleHiddenInput(*a, **kw)


def null_boolean_select(*a, **kw):
    """NullBooleanSelect"""
    return widgets.NullBooleanSelect(*a, **kw)


def number(*a, **kw):
    """NumberInput"""
    return widgets.NumberInput(*a, **kw)


def ordered_set(*a, **kw):
    """OrderedSet"""
    return widgets.OrderedSet(*a, **kw)


def select(*a, **kw):
    """Select"""
    return widgets.Select(*a, **kw)


def select_date(*a, **kw):
    """SelectDateWidget"""
    return widgets.SelectDateWidget(*a, **kw)


def select_multiple(*a, **kw):
    """SelectMultiple"""
    return widgets.SelectMultiple(*a, **kw)


def split_date_time(*a, **kw):
    """SplitDateTimeWidget"""
    return widgets.SplitDateTimeWidget(*a, **kw)


def split_hidden_date_time(*a, **kw):
    """SplitHiddenDateTimeWidget"""
    return widgets.SplitHiddenDateTimeWidget(*a, **kw)


def text(*a, **kw):
    """TextInput"""
    return widgets.TextInput(*a, **kw)


input = text
chars = text


def textarea(*a, **kw):
    """Textarea"""
    return widgets.Textarea(*a, **kw)


area = textarea


def time(*a, **kw):
    """TimeInput"""
    return widgets.TimeInput(*a, **kw)


def url(*a, **kw):
    """URLInput"""
    return widgets.URLInput(*a, **kw)
