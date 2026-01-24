"""
Tests for trim.apps module.

Following best practices with minimal code, PEP8 compliance, and DRY principles.
"""

from unittest.mock import MagicMock, patch, call

import pytest


@pytest.fixture
def mock_hook_waiting():
    """Fixture providing a mocked hook_waiting_model_mixins function."""
    with patch("trim.apps.hook_waiting_model_mixins") as mock_hook:
        yield mock_hook


@pytest.fixture
def mock_pre_init_connect():
    """Fixture providing a mocked pre_init.connect."""
    with patch("trim.apps.pre_init.connect") as mock_connect:
        yield mock_connect


@pytest.fixture
def mock_signals():
    """Fixture providing a mocked signals module."""
    with patch("trim.apps.signals") as mock_signals:
        yield mock_signals


@pytest.fixture
def mock_importlib():
    """Fixture providing a mocked importlib.import_module."""
    with patch("trim.apps.importlib.import_module") as mock_import:
        yield mock_import


@pytest.fixture
def mock_apps_registry():
    """Fixture providing a mocked apps.registry.apps."""
    with patch("trim.apps.apps.registry.apps") as mock_registry:
        yield mock_registry


@pytest.fixture
def mock_settings():
    """Fixture providing a mocked settings."""
    with patch("trim.apps.settings") as mock_settings:
        mock_settings.ROOT_URLCONF = "project.urls"
        yield mock_settings


class TestShortConfigReady:
    """Tests for ShortConfig.ready method."""

    def test_calls_hook_waiting_model_mixins(
        self, mock_hook_waiting, mock_pre_init_connect
    ):
        # setup
        from trim.apps import ShortConfig

        config = ShortConfig.create("trim")

        # execute
        config.ready()

        # assert
        mock_hook_waiting.assert_called_once_with()

    def test_connects_pre_init_signal(self, mock_hook_waiting, mock_pre_init_connect):
        # setup
        from trim.apps import ShortConfig
        from trim import signals

        config = ShortConfig.create("trim")

        # execute
        config.ready()

        # assert
        mock_pre_init_connect.assert_called_once_with(signals.model_pre_init)

    def test_calls_in_correct_order(self, mock_hook_waiting, mock_pre_init_connect):
        # setup
        from trim.apps import ShortConfig

        call_order = []
        mock_hook_waiting.side_effect = lambda: call_order.append("hook")
        mock_pre_init_connect.side_effect = lambda s: call_order.append("signal")

        config = ShortConfig.create("trim")

        # execute
        config.ready()

        # assert
        assert call_order == ["hook", "signal"]


class TestLiveImport:
    """Tests for live_import function."""

    def test_iterates_through_app_configs(self, mock_apps_registry, mock_settings):
        # setup
        from trim.apps import live_import

        mock_config = MagicMock()
        mock_config.label = "testapp"
        mock_config.module.__name__ = "testapp"
        mock_apps_registry.get_app_configs.return_value = [mock_config]

        with patch("trim.apps.silent_import_package_module") as mock_silent:
            mock_silent.return_value = MagicMock()

            # execute
            live_import("coolapp")

            # assert
            mock_apps_registry.get_app_configs.assert_called_once()

    def test_calls_silent_import_for_each_app(self, mock_apps_registry, mock_settings):
        # setup
        from trim.apps import live_import

        mock_config = MagicMock()
        mock_config.label = "testapp"
        mock_config.module.__name__ = "testapp"
        mock_apps_registry.get_app_configs.return_value = [mock_config]
        mock_settings.ROOT_URLCONF = "project.urls"

        with patch("trim.apps.silent_import_package_module") as mock_silent:
            mock_silent.return_value = MagicMock()

            # execute
            live_import("coolapp")

            # assert
            mock_silent.assert_any_call("testapp", "coolapp")
            mock_silent.assert_any_call("project", "coolapp")

    def test_imports_root_app_from_settings(self, mock_apps_registry, mock_settings):
        # setup
        from trim.apps import live_import

        mock_apps_registry.get_app_configs.return_value = []
        mock_settings.ROOT_URLCONF = "myproject.urls"

        with patch("trim.apps.silent_import_package_module") as mock_silent:
            mock_silent.return_value = None

            # execute
            live_import("coolapp")

            # assert
            mock_silent.assert_called_with("myproject", "coolapp")

    def test_returns_tuple_of_imported_modules(self, mock_apps_registry, mock_settings):
        # setup
        from trim.apps import live_import

        mock_config = MagicMock()
        mock_config.label = "testapp"
        mock_config.module.__name__ = "testapp"
        mock_apps_registry.get_app_configs.return_value = [mock_config]

        with patch("trim.apps.silent_import_package_module") as mock_silent:
            mock_module = MagicMock()
            mock_silent.return_value = mock_module

            # execute
            result = live_import("coolapp")

            # assert
            assert isinstance(result, tuple)
            assert mock_module in result

    def test_excludes_none_from_result(self, mock_apps_registry, mock_settings):
        # setup
        from trim.apps import live_import

        mock_config = MagicMock()
        mock_config.label = "testapp"
        mock_config.module.__name__ = "testapp"
        mock_apps_registry.get_app_configs.return_value = [mock_config]

        with patch("trim.apps.silent_import_package_module") as mock_silent:
            # First call returns None (module not found)
            mock_silent.return_value = None

            # execute
            result = live_import("coolapp")

            # assert
            assert None not in result
            assert len(result) == 0


class TestSilentImportPackageModule:
    """Tests for silent_import_package_module function."""

    def test_constructs_module_name_correctly(self, mock_importlib):
        # setup
        from trim.apps import silent_import_package_module

        mock_importlib.return_value = MagicMock()

        # execute
        silent_import_package_module("myapp", "coolmodule")

        # assert
        mock_importlib.assert_called_once_with("myapp.coolmodule")

    def test_returns_imported_module(self, mock_importlib):
        # setup
        from trim.apps import silent_import_package_module

        expected_module = MagicMock()
        mock_importlib.return_value = expected_module

        # execute
        result = silent_import_package_module("myapp", "coolmodule")

        # assert
        assert result == expected_module

    def test_returns_none_when_module_not_found(self, mock_importlib):
        # setup
        from trim.apps import silent_import_package_module

        error = ModuleNotFoundError("No module named 'myapp.coolmodule'")
        error.name = "myapp.coolmodule"
        mock_importlib.side_effect = error

        # execute
        result = silent_import_package_module("myapp", "coolmodule")

        # assert
        assert result is None

    def test_raises_when_different_module_fails(self, mock_importlib):
        # setup
        from trim.apps import silent_import_package_module

        error = ModuleNotFoundError("No module named 'other.dependency'")
        error.name = "other.dependency"
        mock_importlib.side_effect = error

        # execute & assert
        with pytest.raises(ModuleNotFoundError) as exc_info:
            silent_import_package_module("myapp", "coolmodule")

        assert exc_info.value.name == "other.dependency"
