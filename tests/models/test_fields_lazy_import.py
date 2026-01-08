"""
Test trim.models.fields.django lazy import and generic FK helpers.

Tests for:
- LazyImport class
- get_cached function
- contenttype_fk function
- generic_fk function
- any function
- any_model_set function
"""
import unittest

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from trim.models import fields
from trim.models.fields.django import (
    LazyImport,
    get_cached,
    GEN_C,
    CONTENT_TYPE_FIELD,
    ID_FIELD,
)


class LazyImportTest(unittest.TestCase):
    """Test the LazyImport class."""

    def test_get_GenericForeignKey(self):
        # Setup
        lazy = LazyImport()
        
        # Execute
        result = lazy.get_GenericForeignKey()
        
        # Assert
        self.assertIs(result, GenericForeignKey)

    def test_get_ContentType(self):
        # Setup
        lazy = LazyImport()
        
        # Execute
        result = lazy.get_ContentType()
        
        # Assert
        self.assertIs(result, ContentType)

    def test_getitem_GenericForeignKey(self):
        # Setup
        lazy = LazyImport()
        
        # Execute
        result = lazy['GenericForeignKey']
        
        # Assert
        self.assertIs(result, GenericForeignKey)

    def test_getitem_ContentType(self):
        # Setup
        lazy = LazyImport()
        
        # Execute
        result = lazy['ContentType']
        
        # Assert
        self.assertIs(result, ContentType)


class GetCachedTest(unittest.TestCase):
    """Test the get_cached function."""

    def setUp(self):
        # Clear cache before each test (except 'lazy')
        keys_to_remove = [k for k in GEN_C.keys() if k != 'lazy']
        for key in keys_to_remove:
            GEN_C.pop(key, None)

    def test_get_cached_ContentType_first_time(self):
        # Setup - ensure not cached
        self.assertNotIn('ContentType', GEN_C)
        
        # Execute
        result = get_cached('ContentType')
        
        # Assert
        self.assertIs(result, ContentType)
        self.assertIn('ContentType', GEN_C)

    def test_get_cached_GenericForeignKey_first_time(self):
        # Setup - ensure not cached
        self.assertNotIn('GenericForeignKey', GEN_C)
        
        # Execute
        result = get_cached('GenericForeignKey')
        
        # Assert
        self.assertIs(result, GenericForeignKey)
        self.assertIn('GenericForeignKey', GEN_C)

    def test_get_cached_returns_cached_value(self):
        # Setup - pre-cache a value
        GEN_C['ContentType'] = ContentType
        
        # Execute
        result = get_cached('ContentType')
        
        # Assert
        self.assertIs(result, ContentType)


class ContentTypeFKTest(unittest.TestCase):
    """Test the contenttype_fk function."""

    def test_contenttype_fk_default(self):
        # Setup & Execute
        field = fields.contenttype_fk()
        
        # Assert
        self.assertIsInstance(field, models.ForeignKey)
        self.assertIs(field.remote_field.model, ContentType)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_contenttype_fk_with_string_model(self):
        # Setup & Execute
        field = fields.contenttype_fk('contenttypes.ContentType')
        
        # Assert
        self.assertIsInstance(field, models.ForeignKey)

    def test_contenttype_fk_with_model_class(self):
        # Setup & Execute
        field = fields.contenttype_fk(ContentType)
        
        # Assert
        self.assertIsInstance(field, models.ForeignKey)
        self.assertIs(field.remote_field.model, ContentType)


class GenericFKTest(unittest.TestCase):
    """Test the generic_fk function."""

    def test_generic_fk_default(self):
        # Setup & Execute
        field = fields.generic_fk()
        
        # Assert
        self.assertIsInstance(field, GenericForeignKey)
        self.assertEqual(field.ct_field, CONTENT_TYPE_FIELD)
        self.assertEqual(field.fk_field, ID_FIELD)

    def test_generic_fk_custom_fields(self):
        # Setup & Execute
        field = fields.generic_fk('my_content_type', 'my_object_id')
        
        # Assert
        self.assertIsInstance(field, GenericForeignKey)
        self.assertEqual(field.ct_field, 'my_content_type')
        self.assertEqual(field.fk_field, 'my_object_id')

    def test_generic_fk_with_kwargs(self):
        # Setup & Execute
        field = fields.generic_fk(
            content_type_field='custom_ct',
            id_field='custom_id'
        )
        
        # Assert
        self.assertIsInstance(field, GenericForeignKey)
        self.assertEqual(field.ct_field, 'custom_ct')
        self.assertEqual(field.fk_field, 'custom_id')


class AnyModelSetTest(unittest.TestCase):
    """Test the any_model_set function."""

    def test_any_model_set_default(self):
        # Setup & Execute
        gfk, ct_fk, obj_id = fields.any_model_set()
        
        # Assert
        self.assertIsInstance(gfk, GenericForeignKey)
        self.assertIsInstance(ct_fk, models.ForeignKey)
        self.assertIsInstance(obj_id, models.PositiveIntegerField)
        self.assertTrue(ct_fk.blank)
        self.assertTrue(ct_fk.null)

    def test_any_model_set_with_field_names(self):
        # Setup & Execute
        gfk, ct_fk, obj_id = fields.any_model_set(
            'custom_content_type',
            'custom_object_id'
        )
        
        # Assert
        self.assertIsInstance(gfk, GenericForeignKey)
        self.assertEqual(gfk.ct_field, 'custom_content_type')
        self.assertEqual(gfk.fk_field, 'custom_object_id')

    def test_any_model_set_with_nil_false(self):
        # Setup & Execute
        gfk, ct_fk, obj_id = fields.any_model_set(nil=False)
        
        # Assert
        self.assertIsInstance(gfk, GenericForeignKey)
        self.assertIsInstance(ct_fk, models.ForeignKey)
        self.assertIsInstance(obj_id, models.PositiveIntegerField)

    def test_any_model_set_returns_tuple_of_three(self):
        # Setup & Execute
        result = fields.any_model_set()
        
        # Assert
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)


class AnyTest(unittest.TestCase):
    """Test the any function (prefix-based any_model_set)."""

    def test_any_with_prefix(self):
        # Setup & Execute
        gfk, ct_fk, obj_id = fields.any('owner')
        
        # Assert
        self.assertIsInstance(gfk, GenericForeignKey)
        self.assertEqual(gfk.ct_field, 'owner_content_type')
        self.assertEqual(gfk.fk_field, 'owner_object_id')

    def test_any_with_empty_prefix(self):
        # Setup & Execute
        gfk, ct_fk, obj_id = fields.any('')
        
        # Assert
        self.assertIsInstance(gfk, GenericForeignKey)
        self.assertEqual(gfk.ct_field, 'content_type')
        self.assertEqual(gfk.fk_field, 'object_id')

    def test_any_with_no_prefix(self):
        # Setup & Execute
        gfk, ct_fk, obj_id = fields.any(None)
        
        # Assert
        self.assertIsInstance(gfk, GenericForeignKey)
        self.assertEqual(gfk.ct_field, 'content_type')
        self.assertEqual(gfk.fk_field, 'object_id')

    def test_any_with_prefix_and_custom_fields(self):
        # Setup & Execute
        gfk, ct_fk, obj_id = fields.any(
            'product',
            content_type_field='product_type',
            id_field='product_pk'
        )
        
        # Assert
        self.assertIsInstance(gfk, GenericForeignKey)
        # Custom fields should override prefix-based names
        self.assertEqual(gfk.ct_field, 'product_type')
        self.assertEqual(gfk.fk_field, 'product_pk')

    def test_any_alias(self):
        # Setup & Execute & Assert
        self.assertIs(fields.any_model, fields.any)


class GenericFKIntegrationTest(unittest.TestCase):
    """Integration tests for generic FK pattern."""

    def test_complete_generic_fk_pattern(self):
        # Setup - simulate a model definition pattern
        # Execute
        content_type = fields.contenttype_fk()
        object_id = fields.pos_int()
        content_object = fields.generic_fk('content_type', 'object_id')
        
        # Assert
        self.assertIsInstance(content_type, models.ForeignKey)
        self.assertIsInstance(object_id, models.PositiveIntegerField)
        self.assertIsInstance(content_object, GenericForeignKey)
        self.assertEqual(content_object.ct_field, 'content_type')
        self.assertEqual(content_object.fk_field, 'object_id')

    def test_any_model_set_unpacking(self):
        # Setup & Execute - simulate model field unpacking
        owner, owner_ct, owner_id = fields.any_model_set(
            'owner_content_type',
            'owner_object_id'
        )
        
        # Assert - verify all three fields are correct types
        self.assertIsInstance(owner, GenericForeignKey)
        self.assertIsInstance(owner_ct, models.ForeignKey)
        self.assertIsInstance(owner_id, models.PositiveIntegerField)
        self.assertEqual(owner.ct_field, 'owner_content_type')
        self.assertEqual(owner.fk_field, 'owner_object_id')

    def test_any_prefix_pattern(self):
        # Setup & Execute - using prefix shorthand
        hobby, hobby_ct, hobby_id = fields.any('hobby')
        
        # Assert
        self.assertIsInstance(hobby, GenericForeignKey)
        self.assertEqual(hobby.ct_field, 'hobby_content_type')
        self.assertEqual(hobby.fk_field, 'hobby_object_id')


if __name__ == '__main__':
    unittest.main()
