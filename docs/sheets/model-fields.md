# Model Fields Cheat Sheet

`trim.models.fields` provides concise, Django-compatible model field helpers. The helpers return normal Django fields, while supplying useful defaults for common cases such as nullable values, timestamps, user relationships, UUID primary keys, and generic relations.

## Import

```py
from django.db import models
from trim.models import fields
```

Use the helpers inside a Django model exactly as you would use fields from `django.db.models`:

```py
class Example(models.Model):
    name = fields.chars()
    created, updated = fields.dt_cu_pair()
```

Most helpers accept Django field arguments and keyword options. `nil=True` applies `blank=True, null=True` where supported. Helpers that represent relationships use Django's normal `on_delete`, `related_name`, and `through` options.

## Text and String Fields

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `chars` | `name = fields.chars(max_length=120)` | `CharField`; defaults to `max_length=255`. A callable first argument can be used as the default. |
| `text` | `description = fields.text()` | `TextField`. |
| `url` | `website = fields.url()` | `URLField`; defaults to `max_length=200`. |
| `email` | `address = fields.email()` | `EmailField`; defaults to nullable and blank. |
| `slug` | `slug = fields.slug()` | `SlugField`; defaults to `max_length=50`. |
| `rand_str` | `code = fields.rand_str()` | `CharField` with a random-string default. |
| `str_uuid` | `token = fields.str_uuid()` | `CharField` with a UUID callable as its default. |
| `ip_addr` | `address = fields.ip_addr()` | `GenericIPAddressField` for IPv4 or IPv6 addresses. |

## Boolean Fields

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `boolean` | `enabled = fields.boolean(default=True)` | Standard `BooleanField`. |
| `null_bool` | `choice = fields.null_bool()` | `BooleanField` with `blank=True, null=True`. |
| `true_bool` | `is_active = fields.true_bool()` | `BooleanField(default=True)`. |
| `false_bool` | `is_archived = fields.false_bool()` | `BooleanField(default=False)`. |

## Dates and Times

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `date` | `due_date = fields.date()` | `DateField`. |
| `datetime` | `scheduled_at = fields.datetime()` | `DateTimeField`. |
| `blank_dt` | `completed_at = fields.blank_dt()` | `DateTimeField` with `blank=True, null=True`. |
| `dt_created` | `created_at = fields.dt_created()` | `DateTimeField(auto_now_add=True)`. Set when the row is first created. |
| `dt_updated` | `updated_at = fields.dt_updated()` | `DateTimeField(auto_now=True)`. Updated whenever the row is saved. |
| `dt_cu_pair` | `created, updated = fields.dt_cu_pair()` | Returns `(dt_created(), dt_updated())`, useful for the standard created/updated pair. |
| `duration` | `elapsed = fields.duration()` | `DurationField`, represented by Python `timedelta`. |
| `time` | `start_time = fields.time()` | `TimeField`. |

## Numeric Fields

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `integer` | `priority = fields.integer(1)` | `IntegerField`; the first positional value becomes the default. |
| `big_int` | `population = fields.big_int()` | `BigIntegerField`. |
| `small_int` | `rank = fields.small_int()` | `SmallIntegerField`. |
| `pos_int` | `count = fields.pos_int()` | `PositiveIntegerField`. |
| `pos_big_int` | `total = fields.pos_big_int()` | `PositiveBigIntegerField`. |
| `pos_small_int` | `score = fields.pos_small_int()` | `PositiveSmallIntegerField`. |
| `float_` | `ratio = fields.float_()` | `FloatField`. Use the helper name `float_` because `float` is a Python built-in. |
| `decimal` | `price = fields.decimal(digits=10, places=2)` | `DecimalField`; defaults to `max_digits=19, decimal_places=10`. |

## Automatic and UUID Keys

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `auto` | `legacy_id = fields.auto()` | `AutoField`. Django normally creates the primary key automatically, so use this only when explicit. |
| `small_auto` | `sequence = fields.small_auto()` | `SmallAutoField`. |
| `big_auto` | `sequence = fields.big_auto()` | `BigAutoField`. |
| `uuid` | `public_id = fields.uuid()` | `UUIDField(editable=False, default=uuid4)`. |
| `uuid_null` | `optional_id = fields.uuid_null()` | UUID field with `blank=True, null=True`, plus the UUID default. |
| `pk_uuid` | `id = fields.pk_uuid()` | Non-editable UUID primary key using `uuid4`. |

## Relationships

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `fk` | `category = fields.fk("catalog.Category")` | `ForeignKey`; defaults to `on_delete=models.CASCADE`. |
| `user_fk` | `owner = fields.user_fk()` | Foreign key to Django's configured user model; nullable and blank by default. |
| `self_fk` | `parent = fields.self_fk()` | Self-referencing foreign key; nullable and blank by default. |
| `o2o` | `profile = fields.o2o("accounts.Profile")` | `OneToOneField`; defaults to `on_delete=models.CASCADE`. |
| `user_o2o` | `settings = fields.user_o2o()` | One-to-one relation to the configured user model. |
| `m2m` | `tags = fields.m2m("catalog.Tag")` | `ManyToManyField`; defaults to `blank=True`. |
| `user_m2m` | `members = fields.user_m2m()` | Many-to-many relation to the configured user model. |
| `self_m2m` | `related = fields.self_m2m()` | Self-referencing many-to-many relation. |

Pass an explicit deletion policy when the default is not appropriate:

```py
category = fields.fk("catalog.Category", on_delete=models.PROTECT)
```

`ManyToManyField` does not support `null`; use `blank=True` to make it optional.

## Files and Structured Values

| Helper | Example | Result and defaults |
| --- | --- | --- |
| `file` | `attachment = fields.file(upload_to="attachments/")` | `FileField`; defaults to nullable and blank. |
| `image` | `photo = fields.image(upload_to="photos/")` | `ImageField`; defaults to `blank=True`. Requires Pillow for image validation. |
| `filepath` | `source = fields.filepath(path="/srv/imports")` | `FilePathField`; `path` is required and points to a filesystem directory. |
| `binary` | `payload = fields.binary(bytes=1024)` | `BinaryField`; `bytes` supplies the maximum byte length and defaults to `2_097_152`. Binary fields are non-editable by default in Django. |
| `json` | `metadata = fields.json(default=dict)` | `JSONField`. Use a callable such as `dict` or `list` for mutable defaults. |

## Generic Relations

A generic relation is represented by three model attributes: a `GenericForeignKey`, a `ContentType` foreign key, and a positive object ID.

| Helper | Example | Result |
| --- | --- | --- |
| `contenttype_fk` | `content_type = fields.contenttype_fk()` | Foreign key to `django.contrib.contenttypes.models.ContentType`. |
| `generic_fk` | `content_object = fields.generic_fk()` | `GenericForeignKey("content_type", "object_id")`; this is not a database column. |
| `any` | `owner, owner_content_type, owner_object_id = fields.any(prefix="owner")` | Returns the three attributes needed for a named generic relation. |
| `any_model_set` | `target, content_type, object_id = fields.any_model_set("content_type", "object_id")` | Low-level three-field generic relation builder. |

Example:

```py
class Activity(models.Model):
    target, target_content_type, target_object_id = fields.any(prefix="target")
```

Use `contenttype_fk` and `generic_fk` directly when you need custom attribute names:

```py
class Bookmark(models.Model):
    content_type = fields.contenttype_fk()
    object_id = fields.pos_int()
    content_object = fields.generic_fk("content_type", "object_id")
```

`add_generic_key(model, field, ...)` is a runtime helper that attaches a generic relation set to an existing model class. It is not a field declaration.

## Aliases

Aliases are provided for common naming preferences. They point to the same helpers:

| Preferred helper | Aliases |
| --- | --- |
| `chars` | `str`, `string` |
| `integer` | `int`, `int_` |
| `float_` | `float` |
| `boolean` | `bool` |
| `null_bool` | `bool_null`, `boolean_null` |
| `true_bool` | `bool_true`, `boolean_true` |
| `false_bool` | `bool_false`, `boolean_false` |
| `datetime` | `dt` |
| `blank_dt` | `dt_blank` |
| `dt_created` | `created` |
| `dt_updated` | `updated` |
| `user_fk` | `fk_user` |
| `self_fk` | `fk_self` |
| `user_o2o` | `o2o_user` |
| `self_m2m` | `m2m_self` |
| `big_auto` | `auto_big` |
| `small_auto` | `auto_small` |
| `big_int` | `int_big` |
| `small_int` | `int_small` |
| `pos_int` | `int_pos` |
| `pos_small_int` | `int_small_pos` |
| `pos_big_int` | `int_big_pos` |
| `any` | `any_model` |

## Optional Wagtail Fields

These helpers are not re-exported by `from trim.models import fields`; import the optional module directly when Wagtail is installed:

```py
from trim.models.fields import wagtail

class ArticlePageOrderable(models.Model):
    image = wagtail.image_fk()
    body = wagtail.streamfield([])
```

| Helper | Example | Result |
| --- | --- | --- |
| `wagtail.streamfield` | `body = wagtail.streamfield([])` | Wagtail `StreamField`; accepts the Wagtail block definitions as its first argument. |
| `wagtail.image_fk` | `image = wagtail.image_fk()` | Foreign key to the configured Wagtail image model; defaults to `related_name="+"`. |
| `wagtail.image` | `image = wagtail.image()` | Alias for `wagtail.image_fk`. |

## Quick Rules

- Use `nil=True` for optional scalar fields when both form blankness and database `NULL` are intended.
- Use `blank=True`, not `null=True`, for optional many-to-many relations.
- Use callables for mutable defaults: `fields.json(default=dict)`, not `default={}`.
- Use `fields.pk_uuid()` when the model should use a UUID primary key instead of Django's automatic integer key.
- All helpers return Django field objects, so standard Django options remain available.
