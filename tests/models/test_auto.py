import unittest
import string

from trim.models import auto


class TestModel:
    """A mock for this shape:

        if not isinstance(model_name, str):
            _m = model_name._meta
            model_name = f"{_m.model.__module__}{_m.object_name}"
        classes[model_name] += (cls, )

        m._meta: 
            model: <class 'tests.models.test_auto.TestModel'>
            app_label: 'testapp'
            model_name: 'TestModel'
            object_name: 'TestModel'
    """
    
    class Meta:
        model_name = 'testapp.TestModel'
        model = None 
        app_label = 'testapp'
        object_name = 'TestModel'
    

class AutoModuleTestCase(unittest.TestCase):
    """Test case for the trim auto module."""

    def test_hook_model_mixin_class(self):
        """Test that hook_model_mixin_class registers classes correctly."""
        class TestModel:
            class Meta:
                model_name = 'testapp.TestModel'

        auto.hook_model_mixin_class(TestModel)
        classes = auto.get_classes()
        self.assertIn('testapp.TestModel', classes)
        self.assertEqual(len(classes['testapp.TestModel']), 1)
        self.assertIs(classes['testapp.TestModel'][0], TestModel)
