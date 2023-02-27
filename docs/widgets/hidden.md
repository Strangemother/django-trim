# Hidden Form Fields

The `trim.forms.fields.hidden` and `trim.forms.widgets.hidden` function provides an easy to _hide_ form fields. It's built in a structure to allow multiple methods - for your preferred reading style:

Quick list:

```py
class HiddensForm(forms.Form):
    # All of these fields are the same

    # Classic Django
    full_django = forms.CharField(widget=widgets.HiddenInput())
    # Trim
    trim = fields.hidden_chars()
    # Trimish
    untrim = fields.hidden(fields.chars)
    # Trimmer
    trimmed = fields.chars(widget=fields.widgets.hidden())
    # Trimmed (Mix and match)
    partially_trim = forms.CharField(widget=fields.widgets.hidden())
```

**Why so many variants?**

It's just a neat feature of `trim` - it's clear typing allows abstraction when hoisting components. As all trim parts are designed to be inclusive to Django's default components, we can mix-and-match without concern.

As such we feel the _nicest_ method is `fields.hidden(fields.chars)` - but the abstraction would not be complete without a correctly trim `fields.hidden_chars()` function.

## Breakdown

A hidden form field using the standard django fields:

```py
from django import forms
from django.forms import widgets
from trim.forms import fields

class FullDjangoForm(forms.Form):
    product_id = forms.CharField(widget=widgets.HiddenInput())
    ...
```

You can mix default django components with trim parts:

```py
from django import forms
from trim.forms import fields

class FullDjangoForm(forms.Form):
    product_id = forms.CharField(widget=fields.widgets.hidden())
    ...
```

You can replace the `forms.CharField` with a `trim.form.fields.chars` field:

```py
from django import forms
from trim.forms import fields

class MostlyTrimStyleForm(forms.Form):
    product_id = fields.chars(widget=fields.widgets.hidden())
    ...
```

Or use the `hidden_chars` convenience function:

```py
from django import forms
from trim.forms import fields

class TrimStyleForm(forms.Form):
    product_id = fields.hidden_chars()
```

## Hidden Field

Use the alternate `trim.forms.fields.hidden(field)` function for easier reading:

```py
from django import forms
from trim.forms import fields

class VeryTrimStyleForm(forms.Form):
    product_id = fields.hidden(fields.chars())
```
