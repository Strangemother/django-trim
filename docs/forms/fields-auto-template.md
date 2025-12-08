# Form Fields

Reduce typing on forms! Import ready-to-use form field shortcuts.
All fields are drop-in replacements for standard Django form fields.

Here's a fast example:

_forms.py_

```py
from django import forms
from trim.forms import fields

class ContactForm(forms.Form):
    sender = fields.email(required=False)
    cc_myself = fields.bool_false()
    subject = fields.chars(max_length=255, required=False)
    message = fields.text(rows=5, required=True)
    product_id = fields.hidden_chars()
```

## Quick Reference

+ [Alphabetical](#alphabetical) - All fields in alphabetical order
+ [Typed](#typed) - Fields grouped by Django field type
+ [Aliases](#aliases) - Shorthand aliases for common fields

## Alphabetical

All available form field shortcuts:

%(table)s

## Typed

Fields organized by their underlying Django field type:

%(typed_toc)s

%(typed_tables)s

## Aliases

Convenient shorthand aliases for commonly used fields:

%(aliases_table)s

## Usage Examples

### Basic Form

```py
from django import forms
from trim.forms import fields

class ContactForm(forms.Form):
    name = fields.chars(max_length=100)
    email = fields.email()
    message = fields.text()
    send_copy = fields.bool_false()
```

### Form with Hidden Fields

```py
from django import forms
from trim.forms import fields

class ProductQuestionForm(forms.Form):
    product_id = fields.hidden_chars()
    # or using the wrapper function:
    # product_id = fields.hidden(fields.chars)
    
    question = fields.text(attrs={
        'placeholder': 'Does this include a spare flux-capacitor?'
    })
    email = fields.email()
```

### Using Widgets

```py
from django import forms
from trim.forms import fields

class UserProfileForm(forms.Form):
    username = fields.chars(max_length=50)
    password = fields.password()  # CharField with PasswordInput
    bio = fields.text(rows=10, cols=50)  # CharField with Textarea
    avatar = fields.image()
    newsletter = fields.bool_true()  # BooleanField with initial=True
```

### File Upload Forms

```py
from django import forms
from trim.forms import fields

class DocumentUploadForm(forms.Form):
    title = fields.chars(max_length=200)
    single_file = fields.file()
    multiple_files = fields.files()  # Multiple file upload with clearable input
```

### Advanced Field Configuration

```py
from django import forms
from trim.forms import fields

class AdvancedForm(forms.Form):
    # Email with custom widget attributes
    email = fields.email(attrs={'class': 'form-control', 'placeholder': 'user@example.com'})
    
    # Choice field
    category = fields.choice(choices=[
        ('tech', 'Technology'),
        ('sports', 'Sports'),
        ('news', 'News'),
    ])
    
    # Date and time fields
    event_date = fields.date()
    event_time = fields.time()
    event_datetime = fields.datetime()
    
    # Numeric fields
    age = fields.integer(min_value=0, max_value=120)
    price = fields.decimal(max_digits=10, decimal_places=2)
    rating = fields.float(min_value=0.0, max_value=5.0)
```

## Special Fields

### Hidden Field Wrapper

The `hidden()` function is special - it can wrap any field or callable to apply a hidden widget:

```py
from django import forms
from trim.forms import fields

class MyForm(forms.Form):
    # Three equivalent ways to create a hidden CharField:
    field1 = fields.hidden_chars()
    field2 = fields.hidden(fields.chars)
    field3 = fields.hidden(fields.chars())
    
    # Can also wrap any field instance:
    field4 = fields.hidden(forms.IntegerField())
```

## Benefits

- **Less Typing**: Shorter, more readable field definitions
- **Consistent API**: Functional approach across all fields
- **Drop-in Replacement**: 100%% compatible with Django's form fields
- **Widget Shortcuts**: Built-in helpers for common widget patterns (text areas, passwords, hidden fields)
- **Clear Intent**: Field names clearly communicate their purpose

## Compatibility

All `trim.forms.fields` functions return standard Django form field instances. You can:

- Mix trim fields with Django fields in the same form
- Use all standard Django field arguments and options
- Apply custom widgets, validators, and attributes
- Swap between trim and Django fields at any time

```py
from django import forms
from trim.forms import fields

class MixedForm(forms.Form):
    # Mix trim and Django fields freely
    name = fields.chars(max_length=100)
    email = forms.EmailField()  # Standard Django field
    message = fields.text()
    age = forms.IntegerField(min_value=0)  # Standard Django field
```

## Related

- [Quickforms](./quickforms.md) - Implement forms with a single template tag
- [All Fields Form](./all-fields-form.md) - Demo form with all field types
- [Model Fields](../models/fields.md) - Form field shortcuts for Django models
- [Widgets](../widgets/hidden.md) - Custom form widgets

---

_This documentation is auto-generated from `trim.forms.fields`. See `dev/gen_forms_fields_docs.py` for the generator._
