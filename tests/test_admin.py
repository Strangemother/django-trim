"""
Tests for trim.admin module.

Following best practices with minimal code, PEP8 compliance, and DRY principles.
"""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_admin_site():
    """Fixture providing a mocked admin.site.register."""
    with patch("trim.admin.admin.site.register") as mock_register:
        yield mock_register


@pytest.fixture
def mock_admin_register():
    """Fixture providing a mocked admin.register."""
    with patch("trim.admin.admin.register") as mock_register:
        yield mock_register


@pytest.fixture
def mock_grab_models():
    """Fixture providing a mocked grab_models function."""
    with patch("trim.admin.grab_models") as mock_grab:
        yield mock_grab


@pytest.fixture
def mock_cache_known():
    """Fixture providing a mocked cache_known function."""
    with patch("trim.admin.cache_known") as mock_cache:
        yield mock_cache


class TestRegisterModels:
    """Tests for register_models function."""

    def test_calls_admin_register_with_grab_models_result(
        self, mock_admin_site, mock_grab_models
    ):
        # setup
        from trim import admin as trims

        mock_models = MagicMock()
        mock_grab_models.return_value = ["Model1", "Model2"]

        # execute
        trims.register_models(mock_models)

        # assert
        mock_grab_models.assert_called_once_with(mock_models, ignore=None)
        mock_admin_site.assert_called_once_with(["Model1", "Model2"])

    def test_passes_ignore_parameter_to_grab_models(
        self, mock_admin_site, mock_grab_models
    ):
        # setup
        from trim import admin as trims

        mock_models = MagicMock()
        ignore_list = ["IgnoredModel"]
        mock_grab_models.return_value = ["Model1"]

        # execute
        trims.register_models(mock_models, ignore=ignore_list)

        # assert
        mock_grab_models.assert_called_once_with(mock_models, ignore=ignore_list)
        mock_admin_site.assert_called_once_with(["Model1"])

    def test_returns_admin_register_result(self, mock_admin_site, mock_grab_models):
        # setup
        from trim import admin as trims

        mock_models = MagicMock()
        expected_result = MagicMock()
        mock_grab_models.return_value = ["Model1"]
        mock_admin_site.return_value = expected_result

        # execute
        result = trims.register_models(mock_models)

        # assert
        assert result == expected_result


class TestRegister:
    """Tests for register decorator function."""

    def test_calls_cache_known_with_args(self, mock_cache_known, mock_admin_register):
        # setup
        from trim import admin as trims

        mock_model = MagicMock()

        # execute
        trims.register(mock_model)

        # assert
        mock_cache_known.assert_called_once_with(mock_model)

    def test_calls_admin_register_with_args_and_kwargs(
        self, mock_cache_known, mock_admin_register
    ):
        # setup
        from trim import admin as trims

        mock_model = MagicMock()
        mock_kwarg = {"site": "custom_site"}

        # execute
        trims.register(mock_model, **mock_kwarg)

        # assert
        mock_admin_register.assert_called_once_with(mock_model, **mock_kwarg)

    def test_returns_admin_register_result(self, mock_cache_known, mock_admin_register):
        # setup
        from trim import admin as trims

        mock_model = MagicMock()
        expected_result = MagicMock()
        mock_admin_register.return_value = expected_result

        # execute
        result = trims.register(mock_model)

        # assert
        assert result == expected_result

    def test_caches_before_registering(self, mock_cache_known, mock_admin_register):
        # setup
        from trim import admin as trims

        call_order = []
        mock_cache_known.side_effect = lambda *a: call_order.append("cache")
        mock_admin_register.side_effect = lambda *a, **k: call_order.append("register")

        mock_model = MagicMock()

        # execute
        trims.register(mock_model)

        # assert
        assert call_order == ["cache", "register"]
