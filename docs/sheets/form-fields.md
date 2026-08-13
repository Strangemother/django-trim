# Form Fields Cheat Sheet

`trim.forms.fields` provides concise, drop-in helpers for Django form fields. Most helpers return the corresponding `django.forms` field unchanged, while a few add useful widgets or defaults for common form patterns.

## Import

```py
from django import forms
from trim.forms import fields
```

Use the helpers as field declarations on any Django `Form` or `ModelForm`:

```py
class ContactForm(forms.Form):
    sender = fields.email()
    subject = fields.chars(max_length=120)
    message = fields.text(rows=5)
```

The helpers pass positional and keyword arguments through to Django unless a special note below says otherwise.

## Boolean and Text Fields

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `boolean` | `published = fields.boolean()` | Standard `forms.BooleanField`. |
| `boolean_false` | `subscribe = fields.boolean_false()` | Boolean field with `required=False`, suitable for an unchecked default. |
| `boolean_true` | `accept_terms = fields.boolean_true()` | Boolean field with `initial=True`. It remains required by default. |
| `chars` | `name = fields.chars(max_length=120)` | Standard `forms.CharField`. |
| `text` | `message = fields.text(rows=5, cols=60)` | Char field using a textarea widget. Defaults to 3 rows and 30 columns. |
| `password` | `password = fields.password()` | Char field using a password widget. |
| `hidden_chars` | `record_id = fields.hidden_chars()` | Char field using a hidden widget. |
| `email` | `address = fields.email()` | Standard `forms.EmailField`; accepts an `attrs` option for widget attributes. |
| `slug` | `slug = fields.slug()` | Standard `forms.SlugField`. |
| `url` | `website = fields.url()` | Standard `forms.URLField`. |
| `uuid` | `external_id = fields.uuid()` | Standard `forms.UUIDField`. |

Customize the textarea attributes directly when the defaults are not enough:

```py
message = fields.text(attrs={"class": "long-message", "rows": 8})
```

`text` uses the supplied `attrs` mapping as-is; when `attrs` is omitted, it creates one from `rows` and `cols`.

## Choices

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `choice` | `color = fields.choice(choices=[("r", "Red"), ("b", "Blue")])` | Standard `forms.ChoiceField`. |
| `multiple_choice` | `colors = fields.multiple_choice(choices=[("r", "Red"), ("b", "Blue")])` | Standard `forms.MultipleChoiceField`. |
| `typed_choice` | `age = fields.typed_choice(choices=[("18", "Adult")], coerce=int)` | Standard `forms.TypedChoiceField`; converts the selected value with `coerce`. |
| `typed_multiple_choice` | `ages = fields.typed_multiple_choice(choices=[("18", "Adult")], coerce=int)` | Standard `forms.TypedMultipleChoiceField`. |
| `combo` | `contact = fields.combo(fields=[fields.chars(max_length=120), fields.email()])` | Validates one value against each field in the supplied `fields` list. |
| `null_boolean` | `legacy_flag = fields.null_boolean()` | Standard `forms.NullBooleanField` for a nullable boolean choice. |

Choice helpers normally require `choices` (and `coerce` for typed variants) to be useful. Use Django's normal `required`, `empty_label`, and validation options where supported.

## Date, Time, and Numeric Fields

| Helper | Example | Result |
| --- | --- | --- |
| `date` | `birthday = fields.date()` | Standard `forms.DateField`. |
| `datetime` | `starts_at = fields.datetime()` | Standard `forms.DateTimeField`. |
| `split_datetime` | `appointment = fields.split_datetime()` | Standard `forms.SplitDateTimeField`, commonly rendered as separate date and time inputs. |
| `time` | `starts = fields.time()` | Standard `forms.TimeField`. |
| `decimal` | `amount = fields.decimal(max_digits=10, decimal_places=2)` | Standard `forms.DecimalField`. |
| `duration` | `length = fields.duration()` | Standard `forms.DurationField`. |
| `float` | `score = fields.float()` | Standard `forms.FloatField`. |
| `integer` | `quantity = fields.integer(min_value=0)` | Standard `forms.IntegerField`. |

## Files and Structured Values

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `file` | `attachment = fields.file()` | Standard `forms.FileField`. |
| `files` | `attachments = fields.files()` | File field with a clearable file input configured for multiple files. |
| `file_path` | `source = fields.file_path(path="/srv/imports")` | Standard `forms.FilePathField`; `path` is required. |
| `image` | `photo = fields.image()` | Standard `forms.ImageField`; image validation requires Pillow. |
| `json` | `metadata = fields.json()` | Standard `forms.JSONField`. |

`files()` is a convenience field with the multiple-file widget already configured. For a custom upload widget, use `file(widget=...)` with a widget from `trim.forms.fields.widgets`.

## IP and Pattern Validation

| Helper | Example | Result |
| --- | --- | --- |
| `generic_ip_address` | `ip = fields.generic_ip_address(protocol="both")` | Standard `forms.GenericIPAddressField`; accepts IPv4 and IPv6 by default. |
| `regex` | `ticket = fields.regex(r"^[A-Z]{3}-[0-9]+$")` | Standard `forms.RegexField`; validates against the supplied regular expression. |

## Composite and Model Fields

| Helper | Example | Result and notes |
| --- | --- | --- |
| `multi_value` | `value = fields.multi_value(fields=[fields.chars(), fields.integer()])` | Standard `forms.MultiValueField`; normally subclassed with a `compress()` implementation for combining values. |
| `modelchoice` | `author = fields.modelchoice(queryset=Author.objects.all())` | Standard `forms.ModelChoiceField`; requires a queryset. |
| `hidden` | `token = fields.hidden(fields.chars)` | Applies a hidden widget to a callable or field instance. |

`hidden` supports both a field factory and an existing field:

```py
record_id = fields.hidden(fields.chars)
email = fields.hidden(fields.email(required=False))
```

Calling `fields.hidden()` without a field creates a hidden `CharField` through `hidden_chars()`:

```py
csrf_token = fields.hidden()
```

## Aliases

Aliases point to the same helpers and are available for shorter or familiar names:

| Preferred helper | Aliases |
| --- | --- |
| `boolean` | `bool` |
| `boolean_false` | `false_bool`, `bool_false` |
| `boolean_true` | `true_bool`, `bool_true` |
| `chars` | `str`, `char`, `chars_hidden` |
| `password` | `pwd` |
| `integer` | `int` |
| `image` | `img` |
| `text` | `textarea` |
| `hidden` | `hide` |
| `files` | `file_multi`, `multi_file` |

`chars_hidden` is an alias for `chars`, not for `hidden_chars`; use `hidden_chars` when the field itself should render with a hidden widget.

## Widget Integration

The special helpers use widgets from the sibling `trim.forms.fields.widgets` module. Import it directly when constructing a custom field/widget combination:

```py
from trim.forms import fields
from trim.forms.fields import widgets

class UploadForm(forms.Form):
    attachment = fields.file(widget=widgets.clearable_file_input())
    internal_id = fields.hidden(fields.integer)
```

## Related Documentation

- [Form widgets cheat sheet](./form-widgets.md)
- [Hidden form fields](../widgets/hidden.md)
- [Generated form field reference](../forms/fields-auto.md)
- [All-fields form example](../forms/all-fields-form.md)
- [Forms overview](../forms/readme.md)
- [Quickforms](../forms/quickforms.md)

## Quick Rules

- Use `required=False` for optional form input; form fields do not use model-field `null=True`.
- Supply `choices` to choice fields and a `queryset` to `modelchoice`.
- Use `attrs` on `email` or `text` to customize the rendered widget attributes.
- Use `fields.hidden(...)` when the field should remain in the form data but not be visible.
- Use `fields.files()` for the built-in multiple-file input behavior.
- The helpers are thin wrappers, so Django's normal field options and validation behavior still apply.
