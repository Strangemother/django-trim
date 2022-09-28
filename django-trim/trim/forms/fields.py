"""Django form fields as a drop-in for existing fields.
Mix and match with existing components to transition through trim bits

    from trim.forms import fields

    class ProductQuestionForm(forms.Form):
        product_id = forms.CharField(widget=fields.widgets.hidden())
        message = fields.text(attrs={
                'placeholder': 'Does this include a spare flux-capacitor?'
            })

"""

from django import forms
from . import widgets


def boolean(*a, **kw):
    """A standard `forms.BooleanField` field."""
    return forms.BooleanField(*a,**kw)


def boolean_false(*a, **kw):
    """A standard `forms.BooleanField` field with the `required` as `False`
    for a boolean with a default False value."""
    kw.setdefault('required', False)
    return boolean(*a, **kw)

def boolean_true(*a, **kw):
    """A standard `forms.BooleanField` field with the `required` as `False`
    for a boolean with a default False value."""
    kw.setdefault('initial', True)
    return boolean(*a, **kw)


def chars(*a, **kw):
    """A standard `forms.CharField` field."""
    return forms.CharField(*a,**kw)


def password(*a, **kw):
    """A standard `forms.CharField` field. with a password input widget"""
    widget = widgets.password()
    kw.setdefault('widget', widget)
    return char(*a, **kw)


def text(*a, attrs=None,rows=3, cols=30, **kw):
    """A standard `forms.CharField` field. with a TextArea input widget"""
    attrs = attrs or {'rows': rows, 'cols': cols}
    widget = widgets.textarea(attrs=attrs)
    kw.setdefault('widget', widget)
    return char(*a, **kw)


def choice(*a, **kw):
    """A standard `forms.ChoiceField` field."""
    return forms.ChoiceField(*a,**kw)


def date(*a, **kw):
    """A standard `forms.DateField` field."""
    return forms.DateField(*a,**kw)


def datetime(*a, **kw):
    """A standard `forms.DateTimeField` field."""
    return forms.DateTimeField(*a,**kw)


def decimal(*a, **kw):
    """A standard `forms.DecimalField` field."""
    return forms.DecimalField(*a,**kw)


def duration(*a, **kw):
    """A standard `forms.DurationField` field."""
    return forms.DurationField(*a,**kw)


def email(*a, **kw):
    """A standard `forms.EmailField` field."""
    return forms.EmailField(*a,**kw)


def file(*a, **kw):
    """A standard `forms.FileField` field."""
    return forms.FileField(*a,**kw)


def file_path(*a, **kw):
    """A standard `forms.FilePathField` field."""
    return forms.FilePathField(*a,**kw)


def float(*a, **kw):
    """A standard `forms.FloatField` field."""
    return forms.FloatField(*a,**kw)


def generic_ip_address(*a, **kw):
    """A standard `forms.GenericIPAddressField` field."""
    return forms.GenericIPAddressField(*a,**kw)


def image(*a, **kw):
    """A standard `forms.ImageField` field."""
    return forms.ImageField(*a,**kw)

def integer(*a, **kw):
    """A standard `forms.IntegerField` field."""
    return forms.IntegerField(*a,**kw)


def json(*a, **kw):
    """A standard `forms.JSONField` field."""
    return forms.JSONField(*a,**kw)


def multiple_choice(*a, **kw):
    """A standard `forms.MultipleChoiceField` field."""
    return forms.MultipleChoiceField(*a,**kw)


def null_boolean(*a, **kw):
    """A standard `forms.NullBooleanField` field."""
    return forms.NullBooleanField(*a,**kw)


def regex(*a, **kw):
    """A standard `forms.RegexField` field."""
    return forms.RegexField(*a,**kw)


def slug(*a, **kw):
    return forms.SlugField(*a,**kw)


def time(*a, **kw):
    """A standard `forms.TimeField` field."""
    return forms.TimeField(*a,**kw)


def typed_choice(*a, **kw):
    """A standard `forms.TypedChoiceField` field."""
    return forms.TypedChoiceField(*a,**kw)


def typed_multiple_choice(*a, **kw):
    """A standard `forms.TypedMultipleChoiceField` field."""
    return forms.TypedMultipleChoiceField(*a,**kw)


def url(*a, **kw):
    """A standard `forms.URLField` field."""
    return forms.URLField(*a,**kw)


def uuid(*a, **kw):
    """A standard `forms.UUIDField` field."""
    return forms.UUIDField(*a,**kw)


def combo(*a, **kw):
    """A standard `forms.ComboField` field."""
    return forms.ComboField(*a,**kw)


def multi_value(*a, **kw):
    """A standard `forms.MultiValueField` field."""
    return forms.MultiValueField(*a,**kw)


def split_datetime(*a, **kw):
    """A standard `forms.SplitDateTimeField` field."""
    return forms.SplitDateTimeField(*a,**kw)



img = image
int = integer
pwd = password
bool = boolean
bool_false = boolean_false
bool_true = boolean_true
str = char = chars
textarea = text
