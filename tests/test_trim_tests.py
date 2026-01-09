"""
Test the trim.tests module itself to ensure testing utilities work correctly.
"""

import pytest
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic import DetailView, ListView, UpdateView

from trim.tests import (MixinOrderError, assert_mixin_order,
                        assert_view_has_permission, assert_view_requires_login,
                        assert_views_mixin_order, get_view_permissions)


# Test views with correct order
class CorrectView(LoginRequiredMixin, UpdateView):
    """Properly ordered view"""

    pass


class CorrectPermissionView(PermissionRequiredMixin, ListView):
    """Properly ordered view with permissions"""

    permission_required = "myapp.view_model"


# Test views with incorrect order
class IncorrectView(UpdateView, LoginRequiredMixin):
    """Incorrectly ordered view - mixin after view"""

    pass


class IncorrectPermissionView(DetailView, PermissionRequiredMixin):
    """Incorrectly ordered view - mixin after view"""

    permission_required = "myapp.change_model"


# Test views with no auth mixins
class PlainView(ListView):
    """View without any auth mixins"""

    pass


class TestMixinOrderValidation:
    """Test mixin order validation functions"""

    def test_correct_order_passes(self):
        """Correctly ordered views should pass validation"""
        is_valid, error = assert_mixin_order(CorrectView, raise_exception=False)
        assert is_valid
        assert error is None

    def test_correct_permission_view_passes(self):
        """Correctly ordered permission views should pass"""
        is_valid, error = assert_mixin_order(
            CorrectPermissionView, raise_exception=False
        )
        assert is_valid
        assert error is None

    def test_incorrect_order_fails(self):
        """Incorrectly ordered views should fail validation"""
        with pytest.raises(MixinOrderError) as exc_info:
            assert_mixin_order(IncorrectView)

        error_msg = str(exc_info.value)
        assert "IncorrectView" in error_msg
        assert "LoginRequiredMixin" in error_msg
        assert "UpdateView" in error_msg

    def test_incorrect_order_no_exception(self):
        """Test non-raising mode returns error info"""
        is_valid, error = assert_mixin_order(IncorrectView, raise_exception=False)
        assert not is_valid
        assert error is not None
        assert "IncorrectView" in error

    def test_plain_view_passes(self):
        """Views without auth mixins should pass (nothing to validate)"""
        is_valid, error = assert_mixin_order(PlainView, raise_exception=False)
        assert is_valid
        assert error is None


class TestModuleValidation:
    """Test module-wide view validation"""

    def test_validate_correct_module(self):
        """Module with only correct views should pass"""
        import types

        # Create a mock module with correct views
        mock_module = types.ModuleType("mock_views")
        mock_module.CorrectView = CorrectView
        mock_module.CorrectPermissionView = CorrectPermissionView

        errors = assert_views_mixin_order(mock_module, raise_exception=False)
        assert len(errors) == 0

    def test_validate_incorrect_module(self):
        """Module with incorrect views should fail"""
        import types

        mock_module = types.ModuleType("mock_views")
        mock_module.IncorrectView = IncorrectView
        mock_module.IncorrectPermissionView = IncorrectPermissionView

        errors = assert_views_mixin_order(mock_module, raise_exception=False)
        assert len(errors) == 2

    def test_validate_mixed_module_raises(self):
        """Module with any incorrect view should raise"""
        import types

        mock_module = types.ModuleType("mock_views")
        mock_module.CorrectView = CorrectView
        mock_module.IncorrectView = IncorrectView

        with pytest.raises(MixinOrderError):
            assert_views_mixin_order(mock_module, raise_exception=True)


class TestPermissionInspection:
    """Test permission inspection utilities"""

    def test_get_permissions_from_view(self):
        """Should extract permissions from view class"""
        info = get_view_permissions(CorrectPermissionView)

        assert info["permissions"] == ["myapp.view_model"]
        assert info["login_required"] is False
        assert info["any"] is False

    def test_get_login_required(self):
        """Should detect login requirement"""
        info = get_view_permissions(CorrectView)

        assert info["login_required"] is True

    def test_plain_view_has_no_requirements(self):
        """Plain views should have empty requirements"""
        info = get_view_permissions(PlainView)

        assert info["permissions"] == []
        assert info["login_required"] is False
        assert info["user_owned"] is False

    def test_assert_has_permission_passes(self):
        """Should pass when permission exists"""
        assert_view_has_permission(CorrectPermissionView, "myapp.view_model")

    def test_assert_has_permission_fails(self):
        """Should fail when permission missing"""
        with pytest.raises(AssertionError) as exc_info:
            assert_view_has_permission(CorrectPermissionView, "myapp.delete_model")

        assert "does not require permission" in str(exc_info.value)

    def test_assert_requires_login_passes(self):
        """Should pass when login required"""
        assert_view_requires_login(CorrectView)

    def test_assert_requires_login_fails(self):
        """Should fail when login not required"""
        with pytest.raises(AssertionError) as exc_info:
            assert_view_requires_login(PlainView)

        assert "does not require login" in str(exc_info.value)


class TestMultiplePermissions:
    """Test views with multiple permissions"""

    def test_multiple_permissions_list(self):
        """Should handle list of permissions"""

        class MultiPermView(PermissionRequiredMixin, ListView):
            permission_required = ["myapp.view_model", "myapp.change_model"]

        info = get_view_permissions(MultiPermView)
        assert len(info["permissions"]) == 2
        assert "myapp.view_model" in info["permissions"]
        assert "myapp.change_model" in info["permissions"]

    def test_single_permission_string(self):
        """Should handle single permission as string"""
        info = get_view_permissions(CorrectPermissionView)
        assert info["permissions"] == ["myapp.view_model"]
