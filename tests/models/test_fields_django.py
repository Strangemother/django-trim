"""
Test trim.models.fields.django module.

Tests for Django model field helper functions with focus on:
- Field type correctness
- Default value handling
- Callable defaults
- Parameter passing
- Edge cases and error conditions
"""
import unittest
from unittest.mock import Mock
from uuid import UUID

from django.db import models
from trim.models import fields


class CharsFieldTest(unittest.TestCase):
    """Test the chars() field function."""

    def test_chars_basic(self):
        # Setup & Execute
        field = fields.chars()
        
        # Assert
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_chars_with_max_length(self):
        # Setup & Execute
        field = fields.chars(max_length=100)
        
        # Assert
        self.assertEqual(field.max_length, 100)

    def test_chars_with_callable_default(self):
        # Setup
        default_func = Mock(return_value='test_value')
        
        # Execute
        field = fields.chars(default_func)
        
        # Assert
        self.assertEqual(field.default, default_func)
        self.assertEqual(field.max_length, 255)

    def test_chars_with_callable_and_max_length(self):
        # Setup
        default_func = Mock(return_value='test')
        
        # Execute
        field = fields.chars(default_func, max_length=50)
        
        # Assert
        self.assertEqual(field.default, default_func)
        self.assertEqual(field.max_length, 50)

    def test_chars_with_callable_and_default_kwarg_raises(self):
        # Setup
        default_func = Mock(return_value='test')
        
        # Execute & Assert
        with self.assertRaises(Exception) as context:
            fields.chars(default_func, default='conflict')
        
        self.assertIn('Not both', str(context.exception))

    def test_chars_with_nil_false(self):
        # Setup & Execute
        field = fields.chars(blank=False, null=False)
        
        # Assert
        self.assertFalse(field.blank)
        self.assertFalse(field.null)


class IntegerFieldTest(unittest.TestCase):
    """Test the integer() field function."""

    def test_integer_basic(self):
        # Setup & Execute
        field = fields.integer()
        
        # Assert
        self.assertIsInstance(field, models.IntegerField)
        # Django fields always have a 'default' attribute (NOT_PROVIDED if not set)
        from django.db.models.fields import NOT_PROVIDED
        self.assertEqual(field.default, NOT_PROVIDED)

    def test_integer_with_default_value(self):
        # Setup & Execute
        field = fields.integer(18)
        
        # Assert
        self.assertEqual(field.default, 18)

    def test_integer_with_zero_default(self):
        # Setup & Execute
        field = fields.integer(0)
        
        # Assert
        self.assertEqual(field.default, 0)

    def test_integer_with_negative_default(self):
        # Setup & Execute
        field = fields.integer(-10)
        
        # Assert
        self.assertEqual(field.default, -10)


class BooleanFieldTest(unittest.TestCase):
    """Test boolean field variants."""

    def test_true_bool(self):
        # Setup & Execute
        field = fields.true_bool()
        
        # Assert
        self.assertIsInstance(field, models.BooleanField)
        self.assertTrue(field.default)

    def test_false_bool(self):
        # Setup & Execute
        field = fields.false_bool()
        
        # Assert
        self.assertIsInstance(field, models.BooleanField)
        self.assertFalse(field.default)

    def test_null_bool(self):
        # Setup & Execute
        field = fields.null_bool()
        
        # Assert
        self.assertIsInstance(field, models.BooleanField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_boolean_basic(self):
        # Setup & Execute
        field = fields.boolean()
        
        # Assert
        self.assertIsInstance(field, models.BooleanField)


class TextFieldTest(unittest.TestCase):
    """Test the text() field function."""

    def test_text_basic(self):
        # Setup & Execute
        field = fields.text()
        
        # Assert
        self.assertIsInstance(field, models.TextField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_text_with_nil_false(self):
        # Setup & Execute
        field = fields.text(blank=False, null=False)
        
        # Assert
        self.assertFalse(field.blank)
        self.assertFalse(field.null)


class URLFieldTest(unittest.TestCase):
    """Test the url() field function."""

    def test_url_basic(self):
        # Setup & Execute
        field = fields.url()
        
        # Assert
        self.assertIsInstance(field, models.URLField)
        self.assertEqual(field.max_length, 200)

    def test_url_with_custom_max_length(self):
        # Setup & Execute
        field = fields.url(max_length=2000)
        
        # Assert
        self.assertEqual(field.max_length, 2000)


class DateTimeFieldTest(unittest.TestCase):
    """Test datetime field variants."""

    def test_datetime_basic(self):
        # Setup & Execute
        field = fields.datetime()
        
        # Assert
        self.assertIsInstance(field, models.DateTimeField)

    def test_dt_created(self):
        # Setup & Execute
        field = fields.dt_created()
        
        # Assert
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.auto_now_add)

    def test_dt_updated(self):
        # Setup & Execute
        field = fields.dt_updated()
        
        # Assert
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.auto_now)

    def test_dt_cu_pair(self):
        # Setup & Execute
        created, updated = fields.dt_cu_pair()
        
        # Assert
        self.assertIsInstance(created, models.DateTimeField)
        self.assertIsInstance(updated, models.DateTimeField)
        self.assertTrue(created.auto_now_add)
        self.assertTrue(updated.auto_now)

    def test_blank_dt(self):
        # Setup & Execute
        field = fields.blank_dt()
        
        # Assert
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)


class ForeignKeyFieldTest(unittest.TestCase):
    """Test foreign key field variants."""

    def test_fk_with_model_string(self):
        # Setup & Execute
        field = fields.fk('auth.User')
        
        # Assert
        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_fk_with_custom_on_delete(self):
        # Setup & Execute
        field = fields.fk('auth.User', on_delete=models.SET_NULL)
        
        # Assert
        self.assertEqual(field.remote_field.on_delete, models.SET_NULL)

    def test_self_fk(self):
        # Setup & Execute
        field = fields.self_fk()
        
        # Assert
        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.remote_field.model, 'self')

    def test_user_fk(self):
        # Setup & Execute
        field = fields.user_fk()
        
        # Assert
        self.assertIsInstance(field, models.ForeignKey)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)


class ManyToManyFieldTest(unittest.TestCase):
    """Test many-to-many field variants."""

    def test_m2m_basic(self):
        # Setup & Execute
        field = fields.m2m('auth.User')
        
        # Assert
        self.assertIsInstance(field, models.ManyToManyField)
        self.assertTrue(field.blank)

    def test_m2m_null_becomes_blank(self):
        # Setup & Execute
        field = fields.m2m('auth.User', null=True)
        
        # Assert
        self.assertTrue(field.blank)
        self.assertFalse(hasattr(field, 'null') and field.null)

    def test_self_m2m(self):
        # Setup & Execute
        field = fields.self_m2m()
        
        # Assert
        self.assertIsInstance(field, models.ManyToManyField)
        self.assertEqual(field.remote_field.model, 'self')


class OneToOneFieldTest(unittest.TestCase):
    """Test one-to-one field variants."""

    def test_o2o_basic(self):
        # Setup & Execute
        field = fields.o2o('auth.User')
        
        # Assert
        self.assertIsInstance(field, models.OneToOneField)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_user_o2o(self):
        # Setup & Execute
        field = fields.user_o2o()
        
        # Assert
        self.assertIsInstance(field, models.OneToOneField)


class UUIDFieldTest(unittest.TestCase):
    """Test UUID field variants."""

    def test_uuid_basic(self):
        # Setup & Execute
        field = fields.uuid()
        
        # Assert
        self.assertIsInstance(field, models.UUIDField)
        self.assertFalse(field.editable)
        self.assertTrue(callable(field.default))

    def test_pk_uuid(self):
        # Setup & Execute
        field = fields.pk_uuid()
        
        # Assert
        self.assertIsInstance(field, models.UUIDField)
        self.assertTrue(field.primary_key)
        self.assertFalse(field.editable)
        self.assertTrue(callable(field.default))

    def test_uuid_null(self):
        # Setup & Execute
        field = fields.uuid_null()
        
        # Assert
        self.assertIsInstance(field, models.UUIDField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_str_uuid(self):
        # Setup & Execute
        field = fields.str_uuid()
        
        # Assert
        self.assertIsInstance(field, models.CharField)
        self.assertTrue(callable(field.default))


class NumericFieldTest(unittest.TestCase):
    """Test numeric field variants."""

    def test_big_int(self):
        # Setup & Execute
        field = fields.big_int()
        
        # Assert
        self.assertIsInstance(field, models.BigIntegerField)

    def test_small_int(self):
        # Setup & Execute
        field = fields.small_int()
        
        # Assert
        self.assertIsInstance(field, models.SmallIntegerField)

    def test_pos_int(self):
        # Setup & Execute
        field = fields.pos_int()
        
        # Assert
        self.assertIsInstance(field, models.PositiveIntegerField)

    def test_pos_small_int(self):
        # Setup & Execute
        field = fields.pos_small_int()
        
        # Assert
        self.assertIsInstance(field, models.PositiveSmallIntegerField)

    def test_pos_big_int(self):
        # Setup & Execute
        field = fields.pos_big_int()
        
        # Assert
        self.assertIsInstance(field, models.PositiveBigIntegerField)

    def test_decimal_defaults(self):
        # Setup & Execute
        field = fields.decimal()
        
        # Assert
        self.assertIsInstance(field, models.DecimalField)
        self.assertEqual(field.max_digits, 19)
        self.assertEqual(field.decimal_places, 10)

    def test_decimal_custom(self):
        # Setup & Execute
        field = fields.decimal(digits=5, places=2)
        
        # Assert
        self.assertEqual(field.max_digits, 5)
        self.assertEqual(field.decimal_places, 2)

    def test_float(self):
        # Setup & Execute
        field = fields.float()
        
        # Assert
        self.assertIsInstance(field, models.FloatField)


class AutoFieldTest(unittest.TestCase):
    """Test auto-incrementing field variants."""

    def test_auto(self):
        # Setup & Execute
        field = fields.auto()
        
        # Assert
        self.assertIsInstance(field, models.AutoField)

    def test_big_auto(self):
        # Setup & Execute
        field = fields.big_auto()
        
        # Assert
        self.assertIsInstance(field, models.BigAutoField)

    def test_small_auto(self):
        # Setup & Execute
        field = fields.small_auto()
        
        # Assert
        self.assertIsInstance(field, models.SmallAutoField)


class MiscFieldTest(unittest.TestCase):
    """Test miscellaneous field functions."""

    def test_email(self):
        # Setup & Execute
        field = fields.email()
        
        # Assert
        self.assertIsInstance(field, models.EmailField)

    def test_slug(self):
        # Setup & Execute
        field = fields.slug()
        
        # Assert
        self.assertIsInstance(field, models.SlugField)
        self.assertEqual(field.max_length, 50)

    def test_ip_addr(self):
        # Setup & Execute
        field = fields.ip_addr()
        
        # Assert
        self.assertIsInstance(field, models.GenericIPAddressField)

    def test_json(self):
        # Setup & Execute
        field = fields.json()
        
        # Assert
        self.assertIsInstance(field, models.JSONField)

    def test_duration(self):
        # Setup & Execute
        field = fields.duration()
        
        # Assert
        self.assertIsInstance(field, models.DurationField)

    def test_binary(self):
        # Setup & Execute
        field = fields.binary()
        
        # Assert
        self.assertIsInstance(field, models.BinaryField)

    def test_image(self):
        # Setup & Execute
        field = fields.image()
        
        # Assert
        self.assertIsInstance(field, models.ImageField)
        self.assertTrue(field.blank)

    def test_file(self):
        # Setup & Execute
        field = fields.file()
        
        # Assert
        self.assertIsInstance(field, models.FileField)

    def test_time(self):
        # Setup & Execute
        field = fields.time()
        
        # Assert
        self.assertIsInstance(field, models.TimeField)

    def test_date(self):
        # Setup & Execute
        field = fields.date()
        
        # Assert
        self.assertIsInstance(field, models.DateField)


class AliasTest(unittest.TestCase):
    """Test that field aliases work correctly."""

    def test_int_alias(self):
        # Setup & Execute & Assert
        self.assertIs(fields.int, fields.integer)
        self.assertIs(fields.int_, fields.integer)

    def test_str_alias(self):
        # Setup & Execute & Assert
        self.assertIs(fields.str, fields.chars)
        self.assertIs(fields.string, fields.chars)

    def test_bool_aliases(self):
        # Setup & Execute & Assert
        self.assertIs(fields.bool, fields.boolean)
        self.assertIs(fields.bool_null, fields.null_bool)
        self.assertIs(fields.bool_true, fields.true_bool)
        self.assertIs(fields.bool_false, fields.false_bool)

    def test_dt_aliases(self):
        # Setup & Execute & Assert
        self.assertIs(fields.dt, fields.datetime)
        self.assertIs(fields.created, fields.dt_created)
        self.assertIs(fields.updated, fields.dt_updated)

    def test_fk_aliases(self):
        # Setup & Execute & Assert
        self.assertIs(fields.fk_user, fields.user_fk)
        self.assertIs(fields.fk_self, fields.self_fk)

    def test_float_alias(self):
        # Setup & Execute & Assert
        self.assertIs(fields.float, fields.float_)


if __name__ == '__main__':
    unittest.main()
