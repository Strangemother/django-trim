from django.db import models
from short import rand
from django.contrib.auth import get_user_model as orig_get_user_model
from uuid import uuid4 as orig_uuid4

sys_bool = bool

def defaults(args, params, nil_sub=True, nil_key='nil', **kw):

    if nil_sub:
        # nil subtract, or substitution
        #  Nil. being blank+null - where nil=True
        if ('nil' in kw) or ('nil' in params):
            val = kw.get('nil', None) or params.get('nil', None)

            if isinstance(val, sys_bool):
                # if the given value is a single bool,
                # unpack and multiply into the count of
                # args for the blank_null func,
                val = [val] * 2
                kw.update(**blank_null(*val))

    for k,v in kw.items():
        if k == nil_key:
            continue
        params.setdefault(k, v)
    params.pop('nil', None)
    return params


def blank_null(b=True, n=True):
    return {'blank':b, 'null': n}


def url(*a, **kw):
    """A django `models.URLField` passing any arguments and keyword arguments

    provide as a standard field:

        class MyModel(models.Model):
            url = shorts.url(max_length=2000)

    A CharField for a URL, validated by URLValidator.
    The default form widget for this field is a URLInput.
    Like all CharField subclasses, URLField takes the optional max_length
    argument. If you don’t specify max_length, a default of 200 is used.

        class URLField(max_length=200, **options)
    """
    # kw.setdefault('max_length', 200)
    # defaults(kw, **blank_null())
    defaults(a, kw, nil=True, max_length=200)
    return models.URLField(**kw)


def text(*a, **kw):
    """
    """
    # defaults(kw, **blank_null())
    kw = defaults(a, kw, nil=True)
    return models.TextField(*a, **kw)


def chars(first_var=None, *a, **kw):
    """
    """

    # Rearrange the params, if the first var is callable, it's the default func,
    # if an int, it's the max_length
    # If the default= exists, raise an error
    default_max_length = 255
    max_length = default_max_length

    if callable(first_var):
        # Set as default
        max_length = kw.get('max_length', None)
        if kw.get('default', None) is not None:
            s = ('shorts.chars(*default_or_max_length, **params) accepts a'
                ' "default" keyword argument or a function as the first'
                ' argument. Not both.')
            # chars(255)
            # chars(max_length=255)
            # chars(255, default=default_func)
            # chars(default_func)
            # chars(default=default_func)
            # chars(max_length=255, default=default_func)
            # not:
            # chars(func, default=default_func)

            raise Exception(s)

        kw.setdefault('default', first_var)

    if max_length is None:
        max_length = default_max_length

    kw = defaults(a, kw, max_length=max_length, nil=True)
    return models.CharField(*a,**kw)


def rand_str(*a, **kw):
    kw = defaults(a, kw, default=rand.rand_str)
    return chars(*a, **kw)


# def text(*args, **kw):
#     """
#     """
#     kw = defaults(args, kw, nil=True)
#     return models.TextField(*args, **kw)


def null_bool(*a, **kw):
    """A true/false field.

    The default form widget for this field is NullBooleanSelect as null=True.
    The default value of BooleanField is None when Field.default isn’t defined.
    """
    kw = defaults(a, kw, nil=True)
    return boolean(*a, **kw)


def true_bool(*a, **kw):
    """A true/false field. default True

    The default form widget for this field is CheckboxInput, or NullBooleanSelect if null=True.
    The default value of BooleanField is None when Field.default isn’t defined.
    """
    kw = defaults(a, kw, default=True)
    return boolean(*a, **kw)


def false_bool(*a, **kw):
    """A true/false field. default False

    The default form widget for this field is CheckboxInput, or NullBooleanSelect if null=True.
    The default value of BooleanField is None when Field.default isn’t defined.
    """
    kw = defaults(a, kw, default=False)
    return boolean(*a, **kw)


def boolean(*a, **kw):
    """A true/false field.

    The default form widget for this field is CheckboxInput, or NullBooleanSelect if null=True.
    The default value of BooleanField is None when Field.default isn’t defined.
    """
    return models.BooleanField(*a, **kw)


def blank_dt(*a, **kw):
    kw = defaults(a, kw, nil=True)
    return datetime(*a, **kw)


# def blank_date(*a, **kw):
#     kw = defaults(a, kw, nil=True)
#     return date(*a, **kw)


def date(*a, **kw):
    return models.DateField(*a, **kw)


def dt_created(*a, **kw):
    """
    """
    kw.setdefault('auto_now_add', True)
    return datetime(*a, **kw)


def dt_updated(*a, **kw):
    """
    """
    kw.setdefault('auto_now', True)
    return datetime(*a, **kw)


def datetime(*a, **kw):
    kw = defaults(a, kw)
    return models.DateTimeField(*a, **kw)


def integer(*a, **kw):
    """
    """
    value = None
    if len(a) > 0:
        value = a[0]
        a = a[1:]

    if value is not None:
        kw.setdefault('default', value)
    kw = defaults(a, kw)
    return models.IntegerField(*a, **kw)


def get_user_model():
    return orig_get_user_model()


def fk(other, *a, on_delete=None, **kw):
    kw = defaults(a, kw, on_delete=on_delete or models.CASCADE)
    return models.ForeignKey(other, *a, **kw)


def user_fk(*a,**kw):
    kw = defaults(a, kw, nil=True)
    return fk(get_user_model(), *a, **kw)


def m2m(other, *a, **kw):
    """
    """
    kw = defaults(a, kw, blank=True)
    return models.ManyToManyField(other, *a, **kw)


def o2o(other, *a, on_delete=None, **kw):
    kw = defaults(a, kw, on_delete=on_delete or models.CASCADE)
    return models.OneToOneField(other, *a, **kw)


def user_o2o(*a, **kw):
    return o2o(get_user_model(), *a, **kw)


def image(*a, **kw):
    """
    """
    kw = defaults(a, kw, blank=True)
    return models.ImageField(*a, **kw)


def auto(*a, **kw):
    """An IntegerField that automatically increments according to available IDs.
    You usually won’t need to use this directly;
    a primary key field will automatically be added to your model if you
    don’t specify otherwise.

        class AutoField(**options)

    See Automatic primary key fields.
    """
    kw = defaults(a, kw)
    return models.AutoField(*a, **kw)


def big_auto(*a, **kw):
    """ A 64-bit integer, much like an AutoField except that it is guaranteed to
    fit numbers from 1 to 9223372036854775807.

        class BigAutoField(**options)
    """
    kw = defaults(a, kw)
    return models.BigIntegerField(*a, **kw)


def big_int(*a, **kw):
    """A 64-bit integer, much like an IntegerField except that it is guaranteed
    to fit numbers from -9223372036854775808 to 9223372036854775807.

        class BigIntegerField(**options)

    The default form widget for this field is a NumberInput.
    """
    kw = defaults(a, kw, nil=True)
    return models.DurationField(*a, **kw)


def binary(*a, bytes=2_097_152, **kw):
    #class BinaryField(max_length=None, **options)
    # A field to store raw binary data. It can be assigned bytes, bytearray, or memoryview.

    # By default, BinaryField sets editable to False, in which case it can’t be included in a ModelForm.

    # BinaryField has one extra optional argument:
        # BinaryField.max_length
        # The maximum length (in bytes) of the field.
        # The maximum length is enforced in Django’s validation using
        # MaxLengthValidator.
    kw = defaults(a, kw, bytes=bytes, nil=True)
    return models.BinaryField(*a, **kw)


def decimal(*a, digits=19, places=10, **kw):
    """A fixed-precision decimal number, represented in Python by a Decimal instance.
    It validates the input using DecimalValidator.

        class DecimalField(max_digits=None, decimal_places=None, **options)

    Has two required arguments:

    DecimalField.max_digits
        The maximum number of digits allowed in the number.
        Note that this number must be greater than or equal to decimal_places.

    DecimalField.decimal_places
        The number of decimal places to store with the number.

    For example, to store numbers up to 999.99 with a resolution of 2 decimal places,
    you’d use:
    models.DecimalField(..., max_digits=5, decimal_places=2)
    And to store numbers up to approximately one billion with a resolution of 10 decimal places:
    models.DecimalField(..., max_digits=19, decimal_places=10)
    """
    kw = defaults(a, kw, nil=True)
    return models.DecimalField(*a, digits=digits, places=places, **kw)


def duration(*a, **kw):
    """A field for storing periods of time - modeled in Python by timedelta.
    When used on PostgreSQL, the data type used is an interval and on
    Oracle the data type is INTERVAL DAY(9) TO SECOND(6).
    Otherwise a big_int of microseconds is used.

        class DurationField(**options)

    Note:

    Arithmetic with DurationField works in most cases. However on all
    databases other than PostgreSQL, comparing the value of a DurationField
    to arithmetic on DateTimeField instances will not work as expected.
    """

    kw = defaults(a, kw, nil=True)
    return models.DurationField(*a, **kw)


def email(*a, **kw):
    """A CharField that checks that the value is a valid email address
    using EmailValidator.

        class EmailField(max_length=254, **options)
    """

    kw = defaults(a, kw, nil=True)
    return models.EmailField(*a, **kw)


def file(*a, **kw):
    """A file-upload field.

        class FileField(upload_to=None, max_length=100, **options)
    """
    kw = defaults(a, kw, nil=True)
    return models.FileField(*a, **kw)


def filepath(*a, **kw):
    """A CharField whose choices are limited to the filenames in a certain
    directory on the filesystem. Has some special arguments, of which the
    first is required:

        class FilePathField(path='', match=None, recursive=False,
            allow_files=True, allow_folders=False, max_length=100,
            **options)

    FilePathField.path
        Required.
        The absolute filesystem path to a directory from which this
        FilePathField should get its choices. Example: "/home/images".

    path may also be a callable, such as a function to dynamically set
    the path at runtime. Example:

        import os
        from django.conf import settings
        from django.db import models

        def images_path(*a, **kw):
            return os.path.join(settings.LOCAL_FILE_DIR, 'images')

        class MyModel(models.Model):
            file = models.FilePathField(path=images_path)
    """
    kw = defaults(a, kw, nil=True)
    return models.FilePathField(*a, **kw)


def float_(*a, **kw):
    """A floating-point number represented in Python by a float instance.
    class FloatField(**options)

    The default form widget for this field is a NumberInput when localize is
    False or TextInput otherwise.

    """
    kw = defaults(a, kw, nil=True)
    return models.FloatField(*a, **kw)


def ip_addr(*a, **kw):
    """
    An IPv4 or IPv6 address, in string format (e.g. 192.0.2.30 or 2a02:42fe::4).
    The default form widget for this field is a TextInput.

        class GenericIPAddressField(protocol='both', unpack_ipv4=False, **options)

    The IPv6 address normalization follows RFC 4291#section-2.2 section 2.2,
    including using the IPv4 format suggested in paragraph 3 of that section,
    like ::ffff:192.0.2.0. For example, 2001:0::0:01 would be normalized to
    2001::1, and ::ffff:0a0a:0a0a to ::ffff:10.10.10.10. All characters are
    converted to lowercase.

    GenericIPAddressField.protocol
        Limits valid inputs to the specified protocol. Accepted values are
        'both' (default), 'IPv4' or 'IPv6'. Matching is case insensitive.

    GenericIPAddressField.unpack_ipv4
        Unpacks IPv4 mapped addresses like ::ffff:192.0.2.1. If this option
        is enabled that address would be unpacked to 192.0.2.1. Default is
        disabled. Can only be used when protocol is set to 'both'.

    If you allow for blank values, you have to allow for null values since
    blank values are stored as null.
    """
    kw = defaults(a, kw, nil=True)
    return models.GenericIPAddressField(*a, **kw)


def json(*a, **kw):
    """
    A field for storing JSON encoded data. In Python the data is represented
    in its Python native format: dictionaries, lists, strings, numbers,
    booleans and None.

        class JSONField(encoder=None, decoder=None, **options)

    JSONField is supported on MariaDB 10.2.7+, MySQL 5.7.8+, Oracle,
    PostgreSQL, and SQLite (with the JSON1 extension enabled).

    JSONField.encoder
        An optional json.JSONEncoder subclass to serialize data types not
        supported by the standard JSON serializer (e.g. datetime.datetime or
        UUID). For example, you can use the DjangoJSONEncoder class.

    Defaults to json.JSONEncoder.

    JSONField.decoder
        An optional json.JSONDecoder subclass to deserialize the value
        retrieved from the database. The value will be in the format chosen
        by the custom encoder (most often a string). Your deserialization
        may need to account for the fact that you can’t be certain of the
        input type. For example, you run the risk of returning a datetime
        that was actually a string that just happened to be in the same
        format chosen for datetimes.

    Defaults to json.JSONDecoder.

    If you give the field a default, ensure it’s an immutable object,
    such as a str, or a callable object that returns a fresh mutable
    object each time, such as dict or a function.
    Providing a mutable default object like default={} or default=[]
    shares the one object between all model instances.
    """
    kw = defaults(a, kw, nil=True)
    return models.JSONField(*a, **kw)


def pos_big_int(*a, **kw):
    """Like a PositiveIntegerField, but only allows values under a certain
    (database-dependent) point. Values from 0 to 9223372036854775807 are safe
    in all databases supported by Django.

        class PositiveBigIntegerField(**options)
    """

    kw = defaults(a, kw, nil=True)
    return models.PositiveBigIntegerField(*a, **kw)


def pos_int(*a, **kw):
    """Like an IntegerField, but must be either positive or zero (0). Values
    from 0 to 2147483647 are safe in all databases supported by Django. The
    value 0 is accepted for backward compatibility reasons.

        class PositiveIntegerField(**options)
    """

    kw = defaults(a, kw, nil=True)
    return models.PositiveIntegerField(*a, **kw)


def pos_small_int(*a, **kw):
    """Like a PositiveIntegerField, but only allows values under a certain
    (database-dependent) point. Values from 0 to 32767 are safe in all
    databases supported by Django.

        class PositiveSmallIntegerField(**options)
    """
    kw = defaults(a, kw, max_length=50, nil=True)
    return models.PositiveSmallIntegerField(*a, **kw)


def slug(*a, **kw):
    """Slug is a newspaper term. A slug is a short label for something,
    containing only letters, numbers, underscores or hyphens. They’re generally
    used in URLs.

        class SlugField(max_length=50, **options)
    """
    kw = defaults(a, kw, max_length=50, nil=True)
    return models.SlugField(*a, **kw)


def small_auto(*a, **kw):
    """Like an AutoField, but only allows values under a certain
    (database-dependent) limit. Values from 1 to 32767 are safe in all
    databases supported by Django.

        class SmallAutoField(**options)
    """

    kw = defaults(a, kw, nil=True)
    return models.SmallAutoField(*a, **kw)


def small_int(*a, **kw):
    """Like an IntegerField, but only allows values under a certain
    (database-dependent) point. Values from -32768 to 32767 are safe in all
    databases supported by Django.

        class SmallIntegerField(**options)
    """

    kw = defaults(a, kw, nil=True)
    return models.SmallIntegerField(*a, **kw)


def time(*a, **kw):
    """
    A time, represented in Python by a datetime.time instance. Accepts the same auto-population options as DateField.

        class TimeField(auto_now=False, auto_now_add=False, **options)

    The default form widget for this field is a TimeInput. The admin adds some JavaScript shortcuts.
    """
    kw = defaults(a, kw, nil=True)
    return models.TimeField(*a, **kw)


def uuid_null(*a, **kw):
    kw = defaults(a, kw, nil=True)
    return uuid(*a, **kw)


def pk_uuid(*a, **kw):
    # return models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return uuid(primary_key=True, default=orig_uuid4, editable=False)


def uuid(*a, **kw):
    """A field for storing universally unique identifiers.
    Uses Python’s UUID class.

    When used on PostgreSQL, this stores in a uuid datatype, otherwise in
    a char(32).

        class UUIDField(**options)

    Universally unique identifiers are a good alternative to AutoField for
    primary_key. The database will not generate the UUID for you, so it is
    recommended to use default:

        import uuid
        from django.db import models

        class MyUUIDModel(models.Model):
            id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
            # other fields


    Note that a callable (with the parentheses omitted) is passed to default,
    not an instance of UUID.

    """
    kw  = defaults(a, kw, editable=False, default=orig_uuid4)
    return models.UUIDField(*a, **kw)

def str_uuid(*a, **kw):
    kw  = defaults(a, kw, default=orig_uuid4)
    return chars(*a, **kw)

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class LazyImport:
    def get_GenericForeignKey(self):
        from django.contrib.contenttypes.fields import GenericForeignKey
        return GenericForeignKey

    def get_ContentType(self):
        from django.contrib.contenttypes.models import ContentType
        # from django.contrib.contenttypes.fields import GenericForeignKey
        return ContentType

    def __getitem__(self, name):
        return getattr(self, f'get_{name}')()


GEN_C = {
    'lazy': LazyImport()
}


def get_cached(name):
    v = GEN_C.get(name, None)
    if v is None:
        v = GEN_C[name] = GEN_C['lazy'][name]
    return v


def contenttype_fk(content_type=None, *a, **kw):

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    is_str = isinstance(content_type, str)
    ContentType = get_cached('ContentType')
    content_type = apps.get_model(content_type) if is_str else content_type
    content_type = ContentType if content_type is None else content_type
    kw  = defaults(a, kw, on_delete=models.CASCADE)
    return fk(content_type, **kw)


def generic_fk(content_type_field='content_type', id_field='object_id', **kw):
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    kw  = defaults(None, kw)
    GenericForeignKey = get_cached('GenericForeignKey')

    return GenericForeignKey(content_type_field, id_field)


def any_model_set(*a, nil=True, **kw):
    """
    Apply a generic foreignkey insertion on a model using three fields:

        GenericForeignKey   the field to manipulate: e.g. "Product.parent_entity"
        FK: ContentType     The FK content_type, to store the ContentType model filter
        Pos Int             The key of the target model.

    Apply to the class as three arguments,

        class Product(models.Model):
            owner, content_type, object_id = shorts.any_model_set()

    The name of `content_type` and `object_id` should match the key values
    through the GenericForeignKey:


        class Product(models.Model):
            ( hobby,
              hobby_content_type,
              hobby_pk) = shorts.any_model_set(
                                             "hobby_content_type",
                                             "hobby_pk"
                                             )

    The first two parameters for the `any_model_set` function should match the
    fields collected within the class:

        class Product(models.Model):
            owner, owner_content_type, owner_object_id = shorts.any_model_set(
                                    # owner Generif FK target attributes.
                                    'owner_content_type', 'owner_object_id')

            (hobby,
             hobby_content_type,
             hobby_object_id) = shorts.any_model_set(
                                        'hobby_content_type',
                                        'hobby_object_id'
                                    )


    Use the field through the primary field name, in this case `owner`:

        item = Product.objects.get(100)
        item.owner = Other.objects.get(id=200)
        item.save()
    """
    return (
            generic_fk(*a, nil=nil),
            contenttype_fk(nil=nil),
            pos_int(nil=nil)
        )

auto_small = small_auto
auto_big = big_auto
int_small = small_int
int_big = big_int
int_pos = pos_int
int_small_pos = pos_small_int
int_big_pos = pos_big_int
int_ = integer
int = integer

bool_null = null_bool
bool_true = true_bool
bool_false = false_bool
bool = boolean

dt_blank = blank_dt

o2o_user = user_o2o
fk_user = user_fk

