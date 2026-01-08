"""
Test trim.signals module.

Simple tests for signal handlers and string formatters.
"""
import unittest
from unittest.mock import patch

from django.db.models import Model
from trim.signals import str_printer, repr_printer, model_pre_init


class StrPrinterTest(unittest.TestCase):
    """Test str_printer function."""

    def test_with_trim_string(self):
        # Setup
        class Obj:
            _trim_string = 'My String'
        
        # Execute & Assert
        self.assertEqual(str_printer(Obj()), 'My String')

    def test_with_get_method(self):
        # Setup
        class Obj:
            def get_trim_string(self):
                return 'From Method'
        
        # Execute & Assert
        self.assertEqual(str_printer(Obj()), 'From Method')

    def test_with_trim_props_single(self):
        # Setup
        class Obj:
            _trim_props = 'name'
            name = 'Alice'
        
        # Execute & Assert
        self.assertEqual(str_printer(Obj()), 'Alice')

    def test_with_trim_props_tuple(self):
        # Setup
        class Obj:
            _trim_props = ('name', 'age')
            name = 'Bob'
            age = 25
        
        # Execute
        result = str_printer(Obj())
        
        # Assert
        self.assertIn('name=', result)
        self.assertIn('Bob', result)

    def test_with_alts(self):
        # Setup
        class Obj:
            _custom = 'Custom'
        
        # Execute & Assert
        self.assertEqual(str_printer(Obj(), alts=('_custom',)), 'Custom')

    def test_format_interpolation(self):
        # Setup
        class Obj:
            _trim_string = 'User {self.name}'
            name = 'Charlie'
        
        # Execute & Assert
        self.assertEqual(str_printer(Obj()), 'User Charlie')


class ReprPrinterTest(unittest.TestCase):
    """Test repr_printer function."""

    def test_basic_format(self):
        # Setup
        class Product:
            pk = 123
            _trim_string = 'Widget'
        
        # Execute & Assert
        self.assertEqual(repr_printer(Product()), "<Product(123) 'Widget'>")

    def test_with_trim_string_repr_alt(self):
        # Setup
        class Item:
            pk = 99
            _trim_string_repr = 'Repr Format'
            _trim_string = 'Normal'
        
        # Execute
        result = repr_printer(Item())
        
        # Assert
        self.assertIn('Repr Format', result)
        self.assertNotIn('Normal', result)


class ModelPreInitTest(unittest.TestCase):
    """Test model_pre_init signal handler."""

    @patch('trim.signals.hook_init_model_mixins')
    def test_sets_str_methods_with_trim_string(self, mock_hook):
        # Setup
        class FakeModel:
            _trim_string = 'test'
            __str__ = Model.__str__
            __repr__ = Model.__repr__
        
        # Execute
        model_pre_init(FakeModel, args=(), kwargs={})
        
        # Assert
        self.assertEqual(FakeModel.__str__, str_printer)
        self.assertEqual(FakeModel.__repr__, repr_printer)

    @patch('trim.signals.hook_init_model_mixins')
    def test_sets_str_methods_with_trim_props(self, mock_hook):
        # Setup
        class FakeModel:
            _trim_props = ('field',)
            __str__ = Model.__str__
            __repr__ = Model.__repr__
        
        # Execute
        model_pre_init(FakeModel, args=(), kwargs={})
        
        # Assert
        self.assertEqual(FakeModel.__str__, str_printer)
        self.assertEqual(FakeModel.__repr__, repr_printer)

    @patch('trim.signals.hook_init_model_mixins')
    def test_doesnt_override_custom_methods(self, mock_hook):
        # Setup
        custom = lambda self: 'custom'
        
        class FakeModel:
            _trim_string = 'test'
            __str__ = custom
            __repr__ = custom
        
        # Execute
        model_pre_init(FakeModel, args=(), kwargs={})
        
        # Assert
        self.assertEqual(FakeModel.__str__, custom)
        self.assertEqual(FakeModel.__repr__, custom)


if __name__ == '__main__':
    unittest.main()
