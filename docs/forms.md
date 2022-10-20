
### Forms

Reduce typing on forms! Use the fields to quickly flesh out your form fields.
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


Drop in a few shortcuts to quickly infer (and plug-in) required parts for your apps. For example, we can generate a `CreateView`, `UpdateView`, `ListView` and `DeleteView` for all our models, with one line:
