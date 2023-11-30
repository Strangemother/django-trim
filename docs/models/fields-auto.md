# Fields

Reduce typing on models! Import ready-to-use fields for your models.
All fields shadow the existing django field.

Here's a fast example:

_models.py_

```py
from django.db import models
from trim.models import fields

class ContactMessage(models.Model):
    user = fields.user_fk(nil=True)
    sender = fields.email(nil=True)
    cc_myself = fields.bool_false()
    subject = fields.chars(max_length=255, nil=True)
    message = fields.text(nil=False)
    created, updated = fields.dt_cu_pair()
```

+ [Alphabetical](#alphabetical)

## Alphabetical

| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `auto`                | `AutoField`                 |  --  | A standard `AutoField` passing all arguments.
| `auto_big`            | `BigAutoField`              | `big_auto` | A 64-bit integer, much like an AutoField except that it is guaranteed to
| `auto_small`          | `SmallAutoField`            | `small_auto` | Like an AutoField, but only allows values under a certain
| `big_auto`            | `BigAutoField`              |  --  | A 64-bit integer, much like an AutoField except that it is guaranteed to
| `big_int`             | `BigIntegerField`           |  --  | A 64-bit integer, much like an IntegerField except that it is guaranteed
| `binary`              | `BinaryField`               |  --  | A standard `BinaryField` with the first argument as the target byte max
| `blank_dt`            | `DateTimeField`             |  --  | A standard `DateTimeField` with default `null=True`
| `blank_null`          | `dict`                      |  --  | _no docs_
| `bool`                | `BooleanField`              | `boolean` | A standard `BooleanField` passing all arguments.
| `bool_false`          | `BooleanField`              | `false_bool` | A standard `BooleanField` with default `False`
| `bool_null`           | `BooleanField`              | `null_bool` | A standard `BooleanField` with default `null=True`
| `bool_true`           | `BooleanField`              | `true_bool` | A standard `BooleanField` with default `True`
| `boolean`             | `BooleanField`              |  --  | A standard `BooleanField` passing all arguments.
| `boolean_false`       | `BooleanField`              | `false_bool` | A standard `BooleanField` with default `False`
| `boolean_null`        | `BooleanField`              | `null_bool` | A standard `BooleanField` with default `null=True`
| `boolean_true`        | `BooleanField`              | `true_bool` | A standard `BooleanField` with default `True`
| `chars`               | `CharField`                 |  --  | A standard `models.CharField` passing the standard fields.
| `contenttype_fk`      | `ForeignKey`                |  --  | _no docs_
| `created`             | `DateTimeField`             | `dt_created` | A standard `DateTimeField` with default `auto_now_add=True`
| `date`                | `DateField`                 |  --  | A standard `DateTimeField` passing all arguments
| `datetime`            | `DateTimeField`             |  --  | A standard `DateTimeField` passing all arguments
| `decimal`             | `DecimalField`              |  --  | A standard `DecimalField` with defaults `max_digits=19` and
| `dt`                  | `DateTimeField`             | `datetime` | A standard `DateTimeField` passing all arguments
| `dt_blank`            | `DateTimeField`             | `blank_dt` | A standard `DateTimeField` with default `null=True`
| `dt_created`          | `DateTimeField`             |  --  | A standard `DateTimeField` with default `auto_now_add=True`
| `dt_cu_pair`          | `tuple`                     |  --  | A tuple pair of `DateTimeField`, first item `created`, second `updated`.
| `dt_updated`          | `DateTimeField`             |  --  | A standard `DateTimeField` with default `auto_now=True`
| `duration`            | `DurationField`             |  --  | A standard `DurationField`
| `email`               | `EmailField`                |  --  | A CharField that checks that the value is a valid email address
| `false_bool`          | `BooleanField`              |  --  | A standard `BooleanField` with default `False`
| `file`                | `FileField`                 |  --  | A file-upload field.
| `filepath`            | `FilePathField`             |  --  | A CharField whose choices are limited to the filenames in a certain
| `fk`                  | `ForeignKey`                |  --  | A standard `ForeignKey` with the first argument as the _other_ model.
| `fk_self`             | `ForeignKey`                | `self_fk` | A standard `ForeignKey` with the _other_ model as the `"self"`
| `fk_user`             | `ForeignKey`                | `user_fk` | A standard `ForeignKey` with the _other_ model as the `get_user_model()`
| `float`               | `FloatField`                | `float_` | A floating-point number represented in Python by a float instance.
| `float_`              | `FloatField`                |  --  | A floating-point number represented in Python by a float instance.
| `generic_fk`          | `GenericForeignKey`         |  --  | Return the standard GenericForeignKey, providing a content type field and
| `get_user_model`      | `ModelBase`                 |  --  | Return the user model using the original django
| `image`               | `ImageField`                |  --  | A standard `ImageField` passing all arguments
| `int`                 | `IntegerField`              | `integer` | A standard `IntegerField` with the first argument as the default
| `int_`                | `IntegerField`              | `integer` | A standard `IntegerField` with the first argument as the default
| `int_big`             | `BigIntegerField`           | `big_int` | A 64-bit integer, much like an IntegerField except that it is guaranteed
| `int_big_pos`         | `PositiveBigIntegerField`   | `pos_big_int` | Like a PositiveIntegerField, but only allows values under a certain
| `int_pos`             | `PositiveIntegerField`      | `pos_int` | Like an IntegerField, but must be either positive or zero (0). Values
| `int_small`           | `SmallIntegerField`         | `small_int` | Like an IntegerField, but only allows values under a certain
| `int_small_pos`       | `PositiveSmallIntegerField` | `pos_small_int` | Like a PositiveIntegerField, but only allows values under a certain
| `integer`             | `IntegerField`              |  --  | A standard `IntegerField` with the first argument as the default
| `ip_addr`             | `GenericIPAddressField`     |  --  | _no docs_
| `json`                | `JSONField`                 |  --  | _no docs_
| `m2m`                 | `ManyToManyField`           |  --  | A standard `ManyToManyField` accepting the `other` reference of string
| `m2m_self`            | `ManyToManyField`           | `self_m2m` | A many to many field (through `m2m`) refering to _self_
| `null_bool`           | `BooleanField`              |  --  | A standard `BooleanField` with default `null=True`
| `o2o`                 | `OneToOneField`             |  --  | A standard `OneToOneField` with the _other_ model as the first argument
| `o2o_user`            | `OneToOneField`             | `user_o2o` | A standard `OneToOneField` with the _other_ model as the `get_user_model()`
| `orig_get_user_model` | `ModelBase`                 | `get_user_model` | _no docs_
| `orig_uuid4`          | `UUID`                      | `uuid4` | Generate a random UUID.
| `pk_uuid`             | `UUIDField`                 |  --  | Return a standard `UUIDField` field through `uuid()`, with the
| `pos_big_int`         | `PositiveBigIntegerField`   |  --  | Like a PositiveIntegerField, but only allows values under a certain
| `pos_int`             | `PositiveIntegerField`      |  --  | Like an IntegerField, but must be either positive or zero (0). Values
| `pos_small_int`       | `PositiveSmallIntegerField` |  --  | Like a PositiveIntegerField, but only allows values under a certain
| `rand_str`            | `CharField`                 |  --  | Return a standard `CharField` with a default value of a random string
| `self_fk`             | `ForeignKey`                |  --  | A standard `ForeignKey` with the _other_ model as the `"self"`
| `self_m2m`            | `ManyToManyField`           |  --  | A many to many field (through `m2m`) refering to _self_
| `slug`                | `SlugField`                 |  --  | Slug is a newspaper term. A slug is a trim label for something,
| `small_auto`          | `SmallAutoField`            |  --  | Like an AutoField, but only allows values under a certain
| `small_int`           | `SmallIntegerField`         |  --  | Like an IntegerField, but only allows values under a certain
| `str`                 | `CharField`                 | `chars` | A standard `models.CharField` passing the standard fields.
| `str_uuid`            | `CharField`                 |  --  | Return a standard `CharField` through `chars()`, the default value
| `string`              | `CharField`                 | `chars` | A standard `models.CharField` passing the standard fields.
| `text`                | `TextField`                 |  --  | A standard `models.TextField` passing the standard arguments.
| `time`                | `TimeField`                 |  --  | Return a standard `TimeField`
| `true_bool`           | `BooleanField`              |  --  | A standard `BooleanField` with default `True`
| `updated`             | `DateTimeField`             | `dt_updated` | A standard `DateTimeField` with default `auto_now=True`
| `url`                 | `URLField`                  |  --  | A django `models.URLField` passing any arguments and keyword arguments
| `user_fk`             | `ForeignKey`                |  --  | A standard `ForeignKey` with the _other_ model as the `get_user_model()`
| `user_m2m`            | `ManyToManyField`           |  --  | Create a many to many relationship to the user model,
| `user_o2o`            | `OneToOneField`             |  --  | A standard `OneToOneField` with the _other_ model as the `get_user_model()`
| `uuid`                | `UUIDField`                 |  --  | Return a standard `UUIDField`, with editable=False and the default
| `uuid_null`           | `UUIDField`                 |  --  | Return a standard `UUIDField` through `uuid()`.

## Typed

+ [AutoField](#AutoField)
+ [BigAutoField](#BigAutoField)
+ [SmallAutoField](#SmallAutoField)
+ [BigIntegerField](#BigIntegerField)
+ [BinaryField](#BinaryField)
+ [DateTimeField](#DateTimeField)
+ [dict](#dict)
+ [BooleanField](#BooleanField)
+ [CharField](#CharField)
+ [ForeignKey](#ForeignKey)
+ [DateField](#DateField)
+ [DecimalField](#DecimalField)
+ [tuple](#tuple)
+ [DurationField](#DurationField)
+ [EmailField](#EmailField)
+ [FileField](#FileField)
+ [FilePathField](#FilePathField)
+ [FloatField](#FloatField)
+ [GenericForeignKey](#GenericForeignKey)
+ [ModelBase](#ModelBase)
+ [ImageField](#ImageField)
+ [IntegerField](#IntegerField)
+ [PositiveBigIntegerField](#PositiveBigIntegerField)
+ [PositiveIntegerField](#PositiveIntegerField)
+ [SmallIntegerField](#SmallIntegerField)
+ [PositiveSmallIntegerField](#PositiveSmallIntegerField)
+ [GenericIPAddressField](#GenericIPAddressField)
+ [JSONField](#JSONField)
+ [ManyToManyField](#ManyToManyField)
+ [OneToOneField](#OneToOneField)
+ [UUID](#UUID)
+ [UUIDField](#UUIDField)
+ [SlugField](#SlugField)
+ [TextField](#TextField)
+ [TimeField](#TimeField)
+ [URLField](#URLField)



## AutoField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `auto` | `AutoField` |  --  | A standard `AutoField` passing all arguments.

[top](#Typed)


## BigAutoField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `auto_big` | `BigAutoField` | `big_auto` | A 64-bit integer, much like an AutoField except that it is guaranteed to
| `big_auto` | `BigAutoField` |  --  | A 64-bit integer, much like an AutoField except that it is guaranteed to

[top](#Typed)


## SmallAutoField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `auto_small` | `SmallAutoField` | `small_auto` | Like an AutoField, but only allows values under a certain
| `small_auto` | `SmallAutoField` |  --  | Like an AutoField, but only allows values under a certain

[top](#Typed)


## BigIntegerField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `big_int` | `BigIntegerField` |  --  | A 64-bit integer, much like an IntegerField except that it is guaranteed
| `int_big` | `BigIntegerField` | `big_int` | A 64-bit integer, much like an IntegerField except that it is guaranteed

[top](#Typed)


## BinaryField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `binary` | `BinaryField` |  --  | A standard `BinaryField` with the first argument as the target byte max

[top](#Typed)


## DateTimeField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `blank_dt`   | `DateTimeField` |  --  | A standard `DateTimeField` with default `null=True`
| `created`    | `DateTimeField` | `dt_created` | A standard `DateTimeField` with default `auto_now_add=True`
| `datetime`   | `DateTimeField` |  --  | A standard `DateTimeField` passing all arguments
| `dt`         | `DateTimeField` | `datetime` | A standard `DateTimeField` passing all arguments
| `dt_blank`   | `DateTimeField` | `blank_dt` | A standard `DateTimeField` with default `null=True`
| `dt_created` | `DateTimeField` |  --  | A standard `DateTimeField` with default `auto_now_add=True`
| `dt_updated` | `DateTimeField` |  --  | A standard `DateTimeField` with default `auto_now=True`
| `updated`    | `DateTimeField` | `dt_updated` | A standard `DateTimeField` with default `auto_now=True`

[top](#Typed)


## dict


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `blank_null` | `dict` |  --  | _no docs_

[top](#Typed)


## BooleanField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `bool`          | `BooleanField` | `boolean` | A standard `BooleanField` passing all arguments.
| `bool_false`    | `BooleanField` | `false_bool` | A standard `BooleanField` with default `False`
| `bool_null`     | `BooleanField` | `null_bool` | A standard `BooleanField` with default `null=True`
| `bool_true`     | `BooleanField` | `true_bool` | A standard `BooleanField` with default `True`
| `boolean`       | `BooleanField` |  --  | A standard `BooleanField` passing all arguments.
| `boolean_false` | `BooleanField` | `false_bool` | A standard `BooleanField` with default `False`
| `boolean_null`  | `BooleanField` | `null_bool` | A standard `BooleanField` with default `null=True`
| `boolean_true`  | `BooleanField` | `true_bool` | A standard `BooleanField` with default `True`
| `false_bool`    | `BooleanField` |  --  | A standard `BooleanField` with default `False`
| `null_bool`     | `BooleanField` |  --  | A standard `BooleanField` with default `null=True`
| `true_bool`     | `BooleanField` |  --  | A standard `BooleanField` with default `True`

[top](#Typed)


## CharField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `chars`    | `CharField` |  --  | A standard `models.CharField` passing the standard fields.
| `rand_str` | `CharField` |  --  | Return a standard `CharField` with a default value of a random string
| `str`      | `CharField` | `chars` | A standard `models.CharField` passing the standard fields.
| `str_uuid` | `CharField` |  --  | Return a standard `CharField` through `chars()`, the default value
| `string`   | `CharField` | `chars` | A standard `models.CharField` passing the standard fields.

[top](#Typed)


## ForeignKey


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `contenttype_fk` | `ForeignKey` |  --  | _no docs_
| `fk`             | `ForeignKey` |  --  | A standard `ForeignKey` with the first argument as the _other_ model.
| `fk_self`        | `ForeignKey` | `self_fk` | A standard `ForeignKey` with the _other_ model as the `"self"`
| `fk_user`        | `ForeignKey` | `user_fk` | A standard `ForeignKey` with the _other_ model as the `get_user_model()`
| `self_fk`        | `ForeignKey` |  --  | A standard `ForeignKey` with the _other_ model as the `"self"`
| `user_fk`        | `ForeignKey` |  --  | A standard `ForeignKey` with the _other_ model as the `get_user_model()`

[top](#Typed)


## DateField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `date` | `DateField` |  --  | A standard `DateTimeField` passing all arguments

[top](#Typed)


## DecimalField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `decimal` | `DecimalField` |  --  | A standard `DecimalField` with defaults `max_digits=19` and

[top](#Typed)


## tuple


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `dt_cu_pair` | `tuple` |  --  | A tuple pair of `DateTimeField`, first item `created`, second `updated`.

[top](#Typed)


## DurationField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `duration` | `DurationField` |  --  | A standard `DurationField`

[top](#Typed)


## EmailField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `email` | `EmailField` |  --  | A CharField that checks that the value is a valid email address

[top](#Typed)


## FileField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `file` | `FileField` |  --  | A file-upload field.

[top](#Typed)


## FilePathField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `filepath` | `FilePathField` |  --  | A CharField whose choices are limited to the filenames in a certain

[top](#Typed)


## FloatField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `float`  | `FloatField` | `float_` | A floating-point number represented in Python by a float instance.
| `float_` | `FloatField` |  --  | A floating-point number represented in Python by a float instance.

[top](#Typed)


## GenericForeignKey


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `generic_fk` | `GenericForeignKey` |  --  | Return the standard GenericForeignKey, providing a content type field and

[top](#Typed)


## ModelBase


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `get_user_model`      | `ModelBase` |  --  | Return the user model using the original django
| `orig_get_user_model` | `ModelBase` | `get_user_model` | _no docs_

[top](#Typed)


## ImageField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `image` | `ImageField` |  --  | A standard `ImageField` passing all arguments

[top](#Typed)


## IntegerField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `int`     | `IntegerField` | `integer` | A standard `IntegerField` with the first argument as the default
| `int_`    | `IntegerField` | `integer` | A standard `IntegerField` with the first argument as the default
| `integer` | `IntegerField` |  --  | A standard `IntegerField` with the first argument as the default

[top](#Typed)


## PositiveBigIntegerField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `int_big_pos` | `PositiveBigIntegerField` | `pos_big_int` | Like a PositiveIntegerField, but only allows values under a certain
| `pos_big_int` | `PositiveBigIntegerField` |  --  | Like a PositiveIntegerField, but only allows values under a certain

[top](#Typed)


## PositiveIntegerField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `int_pos` | `PositiveIntegerField` | `pos_int` | Like an IntegerField, but must be either positive or zero (0). Values
| `pos_int` | `PositiveIntegerField` |  --  | Like an IntegerField, but must be either positive or zero (0). Values

[top](#Typed)


## SmallIntegerField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `int_small` | `SmallIntegerField` | `small_int` | Like an IntegerField, but only allows values under a certain
| `small_int` | `SmallIntegerField` |  --  | Like an IntegerField, but only allows values under a certain

[top](#Typed)


## PositiveSmallIntegerField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `int_small_pos` | `PositiveSmallIntegerField` | `pos_small_int` | Like a PositiveIntegerField, but only allows values under a certain
| `pos_small_int` | `PositiveSmallIntegerField` |  --  | Like a PositiveIntegerField, but only allows values under a certain

[top](#Typed)


## GenericIPAddressField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `ip_addr` | `GenericIPAddressField` |  --  | _no docs_

[top](#Typed)


## JSONField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `json` | `JSONField` |  --  | _no docs_

[top](#Typed)


## ManyToManyField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `m2m`      | `ManyToManyField` |  --  | A standard `ManyToManyField` accepting the `other` reference of string
| `m2m_self` | `ManyToManyField` | `self_m2m` | A many to many field (through `m2m`) refering to _self_
| `self_m2m` | `ManyToManyField` |  --  | A many to many field (through `m2m`) refering to _self_
| `user_m2m` | `ManyToManyField` |  --  | Create a many to many relationship to the user model,

[top](#Typed)


## OneToOneField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `o2o`      | `OneToOneField` |  --  | A standard `OneToOneField` with the _other_ model as the first argument
| `o2o_user` | `OneToOneField` | `user_o2o` | A standard `OneToOneField` with the _other_ model as the `get_user_model()`
| `user_o2o` | `OneToOneField` |  --  | A standard `OneToOneField` with the _other_ model as the `get_user_model()`

[top](#Typed)


## UUID


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `orig_uuid4` | `UUID` | `uuid4` | Generate a random UUID.

[top](#Typed)


## UUIDField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `pk_uuid`   | `UUIDField` |  --  | Return a standard `UUIDField` field through `uuid()`, with the
| `uuid`      | `UUIDField` |  --  | Return a standard `UUIDField`, with editable=False and the default
| `uuid_null` | `UUIDField` |  --  | Return a standard `UUIDField` through `uuid()`.

[top](#Typed)


## SlugField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `slug` | `SlugField` |  --  | Slug is a newspaper term. A slug is a trim label for something,

[top](#Typed)


## TextField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `text` | `TextField` |  --  | A standard `models.TextField` passing the standard arguments.

[top](#Typed)


## TimeField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `time` | `TimeField` |  --  | Return a standard `TimeField`

[top](#Typed)


## URLField


| Name | Field Name | Alias | Help
| --- | --- | --- | ---
| `url` | `URLField` |  --  | A django `models.URLField` passing any arguments and keyword arguments

[top](#Typed)
