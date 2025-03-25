# Forms

> Reduce typing on forms! Use the `fields` to quickly flesh out your form fields.

All django fields are interchangable. Some are convenience tools such as the `trim.forms.fields.text()` TextArea input field:

_forms.py_
```py
from django import forms
from trim.forms import fields


class ContactForm(forms.Form):
    sender = fields.email(required=False) # EmailField
    cc_myself = fields.bool_false() # A boolean field if `False` prepared
    subject = fields.chars(max_length=255, required=False) # CharField
    message = fields.text(required=True) # A ready-to-go CharField with a TextArea widget
```

## Quick Forms

> Implement a prepared form on any page using the existing view and URLS. [read more in templatetags/quickforms](./quickforms.md)

Two quickform methods exist for your choosing. The _standard_ method return the real Form instance, the _instant form_ creates a finished HTML form.

```jinja
{% load quickforms %}

<form>
{% quickform "app:formview-name" %}
</form>

{% quickform.form "app:formview-name" %}
```


