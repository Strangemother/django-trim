from django import forms
from . import widgets


def boolean(*a, **kw):
    return forms.BooleanField(*a,**kw)

def boolean_false(*a, **kw):
    kw.setdefault('required', False)
    return boolean(*a, **kw)

def chars(*a, **kw):
    return forms.CharField(*a,**kw)


def password(*a, **kw):
    widget = widgets.PasswordInput()
    kw.setdefault('widget', widget)
    return char(*a, **kw)

def text(*a, attrs=None,rows=3, cols=30, **kw):
    attrs = attrs or {'rows': rows, 'cols': cols}
    widget = widgets.Textarea(attrs=attrs)
    kw.setdefault('widget', widget)
    return char(*a, **kw)


def choice(*a, **kw):
    return forms.ChoiceField(*a,**kw)


def date(*a, **kw):
    return forms.DateField(*a,**kw)


def datetime(*a, **kw):
    return forms.DateTimeField(*a,**kw)


def decimal(*a, **kw):
    return forms.DecimalField(*a,**kw)


def duration(*a, **kw):
    return forms.DurationField(*a,**kw)


def email(*a, **kw):
    return forms.EmailField(*a,**kw)


def file(*a, **kw):
    return forms.FileField(*a,**kw)


def file_path(*a, **kw):
    return forms.FilePathField(*a,**kw)


def float(*a, **kw):
    return forms.FloatField(*a,**kw)


def generic_ip_address(*a, **kw):
    return forms.GenericIPAddressField(*a,**kw)


def image(*a, **kw):
    return forms.ImageField(*a,**kw)

def integer(*a, **kw):
    return forms.IntegerField(*a,**kw)


def json(*a, **kw):
    return forms.JSONField(*a,**kw)


def multiple_choice(*a, **kw):
    return forms.MultipleChoiceField(*a,**kw)


def null_boolean(*a, **kw):
    return forms.NullBooleanField(*a,**kw)


def regex(*a, **kw):
    return forms.RegexField(*a,**kw)


def slug(*a, **kw):
    return forms.SlugField(*a,**kw)


def time(*a, **kw):
    return forms.TimeField(*a,**kw)


def typed_choice(*a, **kw):
    return forms.TypedChoiceField(*a,**kw)


def typed_multiple_choice(*a, **kw):
    return forms.TypedMultipleChoiceField(*a,**kw)


def url(*a, **kw):
    return forms.URLField(*a,**kw)


def uuid(*a, **kw):
    return forms.UUIDField(*a,**kw)


def combo(*a, **kw):
    return forms.ComboField(*a,**kw)


def multi_value(*a, **kw):
    return forms.MultiValueField(*a,**kw)


def split_datetime(*a, **kw):
    return forms.SplitDateTimeField(*a,**kw)



img = image
int = integer
pwd = password
bool = boolean
bool_false = boolean_false
str = char = chars
textarea = text
