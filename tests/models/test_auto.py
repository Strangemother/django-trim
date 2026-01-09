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
        model_name = "testapp.TestModel"
        model = None
        app_label = "testapp"
        object_name = "TestModel"


class AutoModuleTestCase(unittest.TestCase):
    """Test case for the trim auto module."""

    def setUp(self):
        """Clear classes before each test."""
        auto.classes.clear()

    def test_auto_model_mixin_subclass_calls_hook(self):
        """Test that AutoModelMixin.__init_subclass__ calls hook_model_mixin_class."""
        from unittest.mock import patch

        with patch("trim.models.auto.hook_model_mixin_class") as mock_hook:

            class TestMixin(auto.AutoModelMixin):
                class Meta:
                    model_name = "test.Model"

            mock_hook.assert_called_once_with(TestMixin)

    def test_bind_mixins_copies_methods_to_sender(self):
        """Test that bind_mixins sets attributes from mixin classes onto sender."""

        class TestMixin:
            def custom_method(self):
                return "custom"

            public_attr = "value"

        class MockSender:
            pass

        sender = MockSender()
        auto.bind_mixins(sender, [TestMixin])

        # Should have set public attributes
        self.assertTrue(hasattr(sender, "custom_method"))
        self.assertTrue(hasattr(sender, "public_attr"))
        self.assertEqual(sender.public_attr, "value")

    def test_hook_model_mixin_class_with_string_model_name(self):
        """Test hook_model_mixin_class with a string model_name."""

        class TestMixin:
            class Meta:
                model_name = "testapp.TestModel"

        auto.hook_model_mixin_class(TestMixin)
        classes = auto.get_classes()

        self.assertIn("testapp.TestModel", classes)
        self.assertEqual(len(classes["testapp.TestModel"]), 1)
        self.assertIs(classes["testapp.TestModel"][0], TestMixin)

    def test_hook_model_mixin_class_with_model_object(self):
        """Test hook_model_mixin_class with a model object."""

        class MockModel:
            pass

        class MockMeta:
            model = MockModel
            object_name = "TestModel"

        MockModel.__module__ = "tests.models.test_auto"

        class TestMixin:
            class Meta:
                model_name = type("obj", (), {"_meta": MockMeta})()

        auto.hook_model_mixin_class(TestMixin)
        classes = auto.get_classes()

        expected_key = "tests.models.test_autoTestModel"
        self.assertIn(expected_key, classes)
        self.assertEqual(len(classes[expected_key]), 1)
        self.assertIs(classes[expected_key][0], TestMixin)

    def test_hook_model_mixin_class_multiple_registrations(self):
        """Test that multiple mixins can be registered to the same model."""

        class TestMixin1:
            class Meta:
                model_name = "app.Model"

        class TestMixin2:
            class Meta:
                model_name = "app.Model"

        auto.hook_model_mixin_class(TestMixin1)
        auto.hook_model_mixin_class(TestMixin2)
        classes = auto.get_classes()

        self.assertEqual(len(classes["app.Model"]), 2)
        self.assertIn(TestMixin1, classes["app.Model"])
        self.assertIn(TestMixin2, classes["app.Model"])

    def test_hook_model_mixin_class_different_models(self):
        """Test that mixins for different models are stored separately."""

        class TestMixin1:
            class Meta:
                model_name = "app.Model1"

        class TestMixin2:
            class Meta:
                model_name = "app.Model2"

        auto.hook_model_mixin_class(TestMixin1)
        auto.hook_model_mixin_class(TestMixin2)
        classes = auto.get_classes()

        self.assertIn("app.Model1", classes)
        self.assertIn("app.Model2", classes)
        self.assertEqual(len(classes["app.Model1"]), 1)
        self.assertEqual(len(classes["app.Model2"]), 1)
        self.assertIs(classes["app.Model1"][0], TestMixin1)
        self.assertIs(classes["app.Model2"][0], TestMixin2)
