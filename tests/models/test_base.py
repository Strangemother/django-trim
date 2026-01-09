"""Tests for trim.models.base module."""

from unittest.mock import patch

import pytest
from django.db import models as django_models

from trim.models.base import MODEL_CACHE, cache_known, get_model, grab_models, is_model


# Test fixtures
class RegularClass:
    """A regular non-model class."""

    pass


class MockModel(django_models.Model):
    """A proper Django model for testing."""

    class Meta:
        app_label = "tests"


class AbstractModel(django_models.Model):
    """An abstract Django model."""

    class Meta:
        abstract = True
        app_label = "tests"


@pytest.fixture(autouse=True)
def clear_model_cache():
    """Clear MODEL_CACHE before each test."""
    MODEL_CACHE.clear()
    yield
    MODEL_CACHE.clear()


class TestIsModel:
    """Tests for is_model function."""

    def test_returns_true_for_django_model(self):
        # setup
        name = "MockModel"
        unit = MockModel
        # execute
        result = is_model(name, unit)
        # assert
        assert result is True

    def test_returns_false_for_dunder_names(self):
        # setup
        name = "__builtins__"
        unit = MockModel
        # execute
        result = is_model(name, unit)
        # assert
        assert result is False

    def test_returns_false_for_non_class(self):
        # setup
        name = "some_function"
        unit = lambda x: x
        # execute
        result = is_model(name, unit)
        # assert
        assert result is False

    def test_returns_false_for_regular_class(self):
        # setup
        name = "RegularClass"
        unit = RegularClass
        # execute
        result = is_model(name, unit)
        # assert
        assert result is False

    def test_returns_false_for_string(self):
        # setup
        name = "test"
        unit = "not a class"
        # execute
        result = is_model(name, unit)
        # assert
        assert result is False

    def test_returns_true_for_abstract_model(self):
        # setup
        name = "AbstractModel"
        unit = AbstractModel
        # execute
        result = is_model(name, unit)
        # assert
        assert result is True


class TestCacheKnown:
    """Tests for cache_known function."""

    def test_caches_single_model(self):
        # setup
        cache_known(MockModel)
        # execute & assert
        assert MockModel._meta.label in MODEL_CACHE
        assert MockModel._meta.model_name in MODEL_CACHE
        assert MODEL_CACHE[MockModel._meta.label] == MockModel

    def test_caches_multiple_models(self):
        # setup
        class Model1(django_models.Model):
            class Meta:
                app_label = "app1"

        class Model2(django_models.Model):
            class Meta:
                app_label = "app2"

        # execute
        cache_known(Model1, Model2)
        # assert
        assert Model1._meta.label in MODEL_CACHE
        assert Model2._meta.label in MODEL_CACHE

    def test_overwrites_existing_cache(self):
        # setup
        MODEL_CACHE["tests.MockModel"] = "old_value"
        # execute
        cache_known(MockModel)
        # assert
        assert MODEL_CACHE["tests.MockModel"] == MockModel


class TestGrabModels:
    """Tests for grab_models function."""

    @pytest.fixture
    def mock_module(self):
        """Create a mock module with mixed members."""

        class Module:
            MockModel = MockModel
            RegularClass = RegularClass
            __dunder__ = "value"
            some_var = 42

        return Module()

    def test_returns_only_models(self, mock_module):
        # execute
        result = grab_models(mock_module)
        # assert
        assert MockModel in result
        assert RegularClass not in result
        assert len(result) == 1

    def test_ignores_string_name(self, mock_module):
        # execute
        result = grab_models(mock_module, ignore="MockModel")
        # assert
        assert MockModel not in result
        assert len(result) == 0

    def test_ignores_tuple_of_names(self, mock_module):
        # setup
        class AnotherModel(django_models.Model):
            class Meta:
                app_label = "tests"

        mock_module.AnotherModel = AnotherModel
        # execute
        result = grab_models(mock_module, ignore=("MockModel",))
        # assert
        assert MockModel not in result
        assert AnotherModel in result

    def test_ignore_accepts_tuple_of_strings(self, mock_module):
        # setup - ignore expects strings, not model classes
        # execute
        result = grab_models(mock_module, ignore=("MockModel",))
        # assert
        assert MockModel not in result

    def test_ignores_model_class_in_tuple(self, mock_module):
        # setup - ignore can accept model classes too
        # execute
        result = grab_models(mock_module, ignore=(MockModel,))
        # assert
        assert MockModel not in result

    def test_ignores_mixed_types(self, mock_module):
        # setup
        class AnotherModel(django_models.Model):
            class Meta:
                app_label = "tests"

        mock_module.AnotherModel = AnotherModel
        # execute - mix of strings and classes
        result = grab_models(mock_module, ignore=("MockModel", AnotherModel))
        # assert
        assert MockModel not in result
        assert AnotherModel not in result

    def test_ignores_abstract_models(self):
        # setup
        class Module:
            AbstractModel = AbstractModel

        # execute
        result = grab_models(Module())
        # assert
        assert AbstractModel not in result

    def test_ignores_admin_pattern(self, mock_module):
        # setup
        cache_known(MockModel)
        MODEL_CACHE["tests.admin"] = MockModel
        # execute
        result = grab_models(mock_module, ignore="tests.admin")
        # assert
        assert MockModel not in result

    def test_handles_none_ignore(self, mock_module):
        # execute
        result = grab_models(mock_module, ignore=None)
        # assert
        assert MockModel in result


class TestGetModel:
    """Tests for get_model function."""

    @patch("django.apps.apps.get_model")
    def test_forwards_args_to_django_apps(self, mock_get_model):
        # setup
        mock_get_model.return_value = MockModel
        # execute
        result = get_model("tests", "MockModel")
        # assert
        mock_get_model.assert_called_once_with("tests", "MockModel")
        assert result == MockModel

    @patch("django.apps.apps.get_model")
    def test_forwards_kwargs_to_django_apps(self, mock_get_model):
        # setup
        mock_get_model.return_value = MockModel
        # execute
        result = get_model(
            app_label="tests", model_name="MockModel", require_ready=False
        )
        # assert
        mock_get_model.assert_called_once_with(
            app_label="tests", model_name="MockModel", require_ready=False
        )
        assert result == MockModel

    @patch("django.apps.apps.get_model")
    def test_forwards_mixed_args_and_kwargs(self, mock_get_model):
        # setup
        mock_get_model.return_value = MockModel
        # execute
        result = get_model("tests", model_name="MockModel")
        # assert
        mock_get_model.assert_called_once_with("tests", model_name="MockModel")
        assert result == MockModel
