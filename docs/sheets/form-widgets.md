# Form Widgets Cheat Sheet

`trim.forms.widgets` provides concise constructors for Django form widgets. Each helper returns a standard Django widget, so it can be passed to a form field, assigned directly to a field's `widget`, or mixed with ordinary Django widgets.

## Import

```py
from django import forms
from trim.forms import fields, widgets
```

Basic composition:

```py
class ContactForm(forms.Form):
    subject = fields.chars(widget=widgets.text())
    message = fields.text(widget=widgets.textarea(attrs={"rows": 6}))
    secret = fields.hidden_chars()
```

## Text and Choice Widgets

| Helper | Example | Django widget |
| --- | --- | --- |
| `text` | `widget = widgets.text(attrs={"placeholder": "Search"})` | `TextInput` |
| `textarea` | `widget = widgets.textarea(attrs={"rows": 5})` | `Textarea` |
| `password` | `widget = widgets.password()` | `PasswordInput` |
| `hidden` | `widget = widgets.hidden()` | `HiddenInput` |
| `base` | `widget = widgets.base()` | `Input` |
| `choice` | `widget = widgets.choice()` | `ChoiceWidget` |
| `select` | `widget = widgets.select()` | `Select` |
| `select_multiple` | `widget = widgets.select_multiple()` | `SelectMultiple` |
| `radios` | `widget = widgets.radios()` | `RadioSelect` |
| `checkbox` | `widget = widgets.checkbox()` | `CheckboxInput` |
| `checkboxes` | `widget = widgets.checkboxes()` | `CheckboxSelectMultiple` |

Example form declarations:

```py
class PreferencesForm(forms.Form):
    display_name = fields.chars(widget=widgets.text())
    color = fields.choice(widget=widgets.radios())
    topics = fields.multiple_choice(widget=widgets.checkboxes())
    enabled = fields.boolean(widget=widgets.checkbox())
```

## Date, Time, and Input Widgets

| Helper | Example | Django widget |
| --- | --- | --- |
| `date` | `widget = widgets.date(format="%Y-%m-%d")` | `DateInput` |
| `date_time_base` | `widget = widgets.date_time_base()` | `DateTimeBaseInput` |
| `date_time` | `widget = widgets.date_time()` | `DateTimeInput` |
| `time` | `widget = widgets.time(format="%H:%M")` | `TimeInput` |
| `email` | `widget = widgets.email()` | `EmailInput` |
| `url` | `widget = widgets.url()` | `URLInput` |
| `number` | `widget = widgets.number(min_value=0)` | `NumberInput` |
| `file` | `widget = widgets.file()` | `FileInput` |

## Multiple and Composite Widgets

| Helper | Example | Django widget |
| --- | --- | --- |
| `multi_widget` | `widget = widgets.multi_widget(widgets=[widgets.text(), widgets.number()])` | `MultiWidget` |
| `multiple_hidden` | `widget = widgets.multiple_hidden()` | `MultipleHiddenInput` |
| `select_date` | `widget = widgets.select_date(years=range(2020, 2031))` | `SelectDateWidget` |
| `split_date_time` | `widget = widgets.split_date_time()` | `SplitDateTimeWidget` |
| `split_hidden_date_time` | `widget = widgets.split_hidden_date_time()` | `SplitHiddenDateTimeWidget` |
| `null_boolean_select` | `widget = widgets.null_boolean_select()` | `NullBooleanSelect` |
| `ordered_set` | `widget = widgets.ordered_set()` | Django's `OrderedSet` widget utility exposed by the module |

`multi_widget` is useful when paired with a `MultiValueField`:

```py
class RangeForm(forms.Form):
    value = fields.multi_value(
        fields=[fields.integer(), fields.integer()],
        widget=widgets.multi_widget([widgets.number(), widgets.number()]),
    )
```

## File Uploads

`clearable_file_input` returns Trim's `MultipleFileInput`, a `ClearableFileInput` subclass with multiple-file support:

```py
class UploadForm(forms.Form):
    attachments = fields.files()
    custom_attachment = fields.file(
        widget=widgets.clearable_file_input(attrs={"class": "uploads"}),
    )
```

The widget sets `allow_multiple_selected = True`, and the resulting HTML input supports multiple selected files. Validate upload size, type, and authorization on the server; a widget does not provide security validation.

| Object | Example | Purpose |
| --- | --- | --- |
| `MultipleFileInput` | `widget = widgets.MultipleFileInput()` | Clearable file input configured for multiple selection. |
| `clearable_file_input` | `widget = widgets.clearable_file_input()` | Constructor for `MultipleFileInput`. |

## Aliases

| Preferred helper | Aliases |
| --- | --- |
| `checkboxes` | `checkbox_select_multiple` |
| `text` | `input`, `chars` |
| `textarea` | `area` |

The module also imports Django's widget classes with `from django.forms.widgets import *`. Prefer the Trim constructors above for the documented shortcut API, or import a Django widget directly when you need a class not represented here.

## Field Integration Patterns

Use a widget directly on a Trim field:

```py
class AccountForm(forms.Form):
    username = fields.chars(widget=widgets.text(attrs={"autocomplete": "username"}))
    password = fields.password()
    birthday = fields.date(widget=widgets.select_date())
```

Use the field convenience helpers when they already select the intended widget:

```py
class SecureForm(forms.Form):
    token = fields.hidden(fields.chars)
    message = fields.text(rows=8)
    uploads = fields.files()
```

## Related Documentation

- [Form fields cheat sheet](./form-fields.md)
- [Hidden form fields](../widgets/hidden.md)
- [Generated form field reference](../forms/fields-auto.md)
- [All-fields form example](../forms/all-fields-form.md)
- [Forms overview](../forms/readme.md)
- [Quickforms](../forms/quickforms.md)
