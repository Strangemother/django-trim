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

| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `boolean`               | `BooleanField`             |  --  | A standard `forms.BooleanField` field.
| `boolean_false`         | `BooleanField`             |  --  | A standard `forms.BooleanField` field with the `required` as `False`
| `boolean_true`          | `BooleanField`             |  --  | A standard `forms.BooleanField` field with the `required` as `False`
| `chars`                 | `CharField`                |  --  | A standard `forms.CharField` field.
| `choice`                | `ChoiceField`              |  --  | A standard `forms.ChoiceField` field.
| `combo`                 | `ComboField`               |  --  | A standard `forms.ComboField` field.
| `date`                  | `DateField`                |  --  | A standard `forms.DateField` field.
| `datetime`              | `DateTimeField`            |  --  | A standard `forms.DateTimeField` field.
| `decimal`               | `DecimalField`             |  --  | A standard `forms.DecimalField` field.
| `duration`              | `DurationField`            |  --  | A standard `forms.DurationField` field.
| `email`                 | `EmailField`               |  --  | A standard `forms.EmailField` field.
| `file`                  | `FileField`                |  --  | A standard `forms.FileField` field.
| `file_path`             | `FilePathField`            |  --  | A standard `forms.FilePathField` field.
| `files`                 | `Custom/Special`           |  --  | A _muliple_ Standard form file field, with a clearable input.
| `float`                 | `FloatField`               |  --  | A standard `forms.FloatField` field.
| `generic_ip_address`    | `GenericIPAddressField`    |  --  | A standard `forms.GenericIPAddressField` field.
| `hidden`                | `Custom/Special`           |  --  | Wrap a callable or field instance with `hidden()` to automatically
| `hidden_chars`          | `Custom/Special`           |  --  | _no docs_
| `image`                 | `ImageField`               |  --  | A standard `forms.ImageField` field.
| `integer`               | `IntegerField`             |  --  | A standard `forms.IntegerField` field.
| `json`                  | `JSONField`                |  --  | A standard `forms.JSONField` field.
| `modelchoice`           | `ModelChoiceField`         |  --  | A standard `forms.ModelChoiceField` field.
| `multi_value`           | `MultiValueField`          |  --  | A standard `forms.MultiValueField` field.
| `multiple_choice`       | `MultipleChoiceField`      |  --  | A standard `forms.MultipleChoiceField` field.
| `null_boolean`          | `NullBooleanField`         |  --  | A standard `forms.NullBooleanField` field.
| `password`              | `CharField`                |  --  | A standard `forms.CharField` field. with a password input widget
| `regex`                 | `RegexField`               |  --  | A standard `forms.RegexField` field.
| `slug`                  | `SlugField`                |  --  | _no docs_
| `split_datetime`        | `SplitDateTimeField`       |  --  | A standard `forms.SplitDateTimeField` field.
| `text`                  | `CharField`                |  --  | A standard `forms.CharField` field. with a TextArea input widget
| `time`                  | `TimeField`                |  --  | A standard `forms.TimeField` field.
| `typed_choice`          | `TypedChoiceField`         |  --  | A standard `forms.TypedChoiceField` field.
| `typed_multiple_choice` | `TypedMultipleChoiceField` |  --  | A standard `forms.TypedMultipleChoiceField` field.
| `url`                   | `URLField`                 |  --  | A standard `forms.URLField` field.
| `uuid`                  | `UUIDField`                |  --  | A standard `forms.UUIDField` field.

## Typed

Fields organized by their underlying Django field type:

+ [BooleanField](#BooleanField)
+ [CharField](#CharField)
+ [ChoiceField](#ChoiceField)
+ [ComboField](#ComboField)
+ [DateField](#DateField)
+ [DateTimeField](#DateTimeField)
+ [DecimalField](#DecimalField)
+ [DurationField](#DurationField)
+ [EmailField](#EmailField)
+ [FileField](#FileField)
+ [FilePathField](#FilePathField)
+ [Custom/Special](#CustomSpecial)
+ [FloatField](#FloatField)
+ [GenericIPAddressField](#GenericIPAddressField)
+ [ImageField](#ImageField)
+ [IntegerField](#IntegerField)
+ [JSONField](#JSONField)
+ [ModelChoiceField](#ModelChoiceField)
+ [MultiValueField](#MultiValueField)
+ [MultipleChoiceField](#MultipleChoiceField)
+ [NullBooleanField](#NullBooleanField)
+ [RegexField](#RegexField)
+ [SlugField](#SlugField)
+ [SplitDateTimeField](#SplitDateTimeField)
+ [TimeField](#TimeField)
+ [TypedChoiceField](#TypedChoiceField)
+ [TypedMultipleChoiceField](#TypedMultipleChoiceField)
+ [URLField](#URLField)
+ [UUIDField](#UUIDField)



## BooleanField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `boolean`       | `BooleanField` |  --  | A standard `forms.BooleanField` field.
| `boolean_false` | `BooleanField` |  --  | A standard `forms.BooleanField` field with the `required` as `False`
| `boolean_true`  | `BooleanField` |  --  | A standard `forms.BooleanField` field with the `required` as `False`

[top](#Typed)


## CharField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `chars`    | `CharField` |  --  | A standard `forms.CharField` field.
| `password` | `CharField` |  --  | A standard `forms.CharField` field. with a password input widget
| `text`     | `CharField` |  --  | A standard `forms.CharField` field. with a TextArea input widget

[top](#Typed)


## ChoiceField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `choice` | `ChoiceField` |  --  | A standard `forms.ChoiceField` field.

[top](#Typed)


## ComboField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `combo` | `ComboField` |  --  | A standard `forms.ComboField` field.

[top](#Typed)


## DateField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `date` | `DateField` |  --  | A standard `forms.DateField` field.

[top](#Typed)


## DateTimeField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `datetime` | `DateTimeField` |  --  | A standard `forms.DateTimeField` field.

[top](#Typed)


## DecimalField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `decimal` | `DecimalField` |  --  | A standard `forms.DecimalField` field.

[top](#Typed)


## DurationField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `duration` | `DurationField` |  --  | A standard `forms.DurationField` field.

[top](#Typed)


## EmailField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `email` | `EmailField` |  --  | A standard `forms.EmailField` field.

[top](#Typed)


## FileField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `file` | `FileField` |  --  | A standard `forms.FileField` field.

[top](#Typed)


## FilePathField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `file_path` | `FilePathField` |  --  | A standard `forms.FilePathField` field.

[top](#Typed)


## Custom/Special


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `files`        | `Custom/Special` |  --  | A _muliple_ Standard form file field, with a clearable input.
| `hidden`       | `Custom/Special` |  --  | Wrap a callable or field instance with `hidden()` to automatically
| `hidden_chars` | `Custom/Special` |  --  | _no docs_

[top](#Typed)


## FloatField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `float` | `FloatField` |  --  | A standard `forms.FloatField` field.

[top](#Typed)


## GenericIPAddressField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `generic_ip_address` | `GenericIPAddressField` |  --  | A standard `forms.GenericIPAddressField` field.

[top](#Typed)


## ImageField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `image` | `ImageField` |  --  | A standard `forms.ImageField` field.

[top](#Typed)


## IntegerField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `integer` | `IntegerField` |  --  | A standard `forms.IntegerField` field.

[top](#Typed)


## JSONField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `json` | `JSONField` |  --  | A standard `forms.JSONField` field.

[top](#Typed)


## ModelChoiceField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `modelchoice` | `ModelChoiceField` |  --  | A standard `forms.ModelChoiceField` field.

[top](#Typed)


## MultiValueField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `multi_value` | `MultiValueField` |  --  | A standard `forms.MultiValueField` field.

[top](#Typed)


## MultipleChoiceField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `multiple_choice` | `MultipleChoiceField` |  --  | A standard `forms.MultipleChoiceField` field.

[top](#Typed)


## NullBooleanField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `null_boolean` | `NullBooleanField` |  --  | A standard `forms.NullBooleanField` field.

[top](#Typed)


## RegexField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `regex` | `RegexField` |  --  | A standard `forms.RegexField` field.

[top](#Typed)


## SlugField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `slug` | `SlugField` |  --  | _no docs_

[top](#Typed)


## SplitDateTimeField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `split_datetime` | `SplitDateTimeField` |  --  | A standard `forms.SplitDateTimeField` field.

[top](#Typed)


## TimeField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `time` | `TimeField` |  --  | A standard `forms.TimeField` field.

[top](#Typed)


## TypedChoiceField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `typed_choice` | `TypedChoiceField` |  --  | A standard `forms.TypedChoiceField` field.

[top](#Typed)


## TypedMultipleChoiceField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `typed_multiple_choice` | `TypedMultipleChoiceField` |  --  | A standard `forms.TypedMultipleChoiceField` field.

[top](#Typed)


## URLField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `url` | `URLField` |  --  | A standard `forms.URLField` field.

[top](#Typed)


## UUIDField


| Name | Django Field | Alias | Description
| --- | --- | --- | ---
| `uuid` | `UUIDField` |  --  | A standard `forms.UUIDField` field.

[top](#Typed)

## Aliases

Convenient shorthand aliases for commonly used fields:

| Alias | Points To |
| --- | --- |
| `bool` | `boolean` |
| `bool_false` | `boolean_false` |
| `bool_true` | `boolean_true` |
| `char` | `chars` |
| `chars_hidden` | `chars` |
| `false_bool` | `boolean_false` |
| `file_multi` | `files` |
| `hide` | `hidden` |
| `img` | `image` |
| `int` | `integer` |
| `multi_file` | `files` |
| `pwd` | `password` |
| `str` | `chars` |
| `textarea` | `text` |
| `true_bool` | `boolean_true` |

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
- **Drop-in Replacement**: 100% compatible with Django's form fields
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
