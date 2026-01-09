"""
Testing utilities for django-trim.

Provides helpers to validate view configurations, mixin order, and other
common patterns when using trim shortcuts.

Example usage in your tests:

    from trim import tests as trim_tests
    from myapp import views

    class ViewConfigTest(TestCase):
        def test_mixin_order(self):
            trim_tests.assert_mixin_order(views.MySecureView)

        def test_all_views(self):
            trim_tests.assert_views_mixin_order(views)
"""

from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.test import TestCase
from django.views.generic.base import View

# Authentication/permission mixins that should come before view classes
AUTH_MIXINS = (
    AccessMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)


class MixinOrderError(AssertionError):
    """Raised when mixins are in incorrect order."""

    pass


def get_mro_position(klass, target_class):
    """
    Get the position of a class in the Method Resolution Order.

    Args:
        klass: The class to inspect
        target_class: The class to find in the MRO

    Returns:
        int: Position in MRO, or -1 if not found
    """
    try:
        return klass.__mro__.index(target_class)
    except ValueError:
        return -1


def find_auth_mixins(klass):
    """
    Find all authentication/permission mixins in a view class.

    Args:
        klass: The view class to inspect

    Returns:
        list: List of tuples (mixin_class, position_in_mro)
    """
    found = []
    for mixin in AUTH_MIXINS:
        pos = get_mro_position(klass, mixin)
        if pos >= 0:
            found.append((mixin, pos))
    return found


def find_view_base(klass):
    """
    Find the base Django view class in the MRO.

    Args:
        klass: The view class to inspect

    Returns:
        tuple: (view_class, position) or (None, -1) if not found
    """
    for i, cls in enumerate(klass.__mro__):
        # Check if it's a Django generic view (but not View itself at position 0)
        if i > 0 and issubclass(cls, View) and cls is not View:
            # Found a concrete view class
            return (cls, i)
    return (None, -1)


def assert_mixin_order(view_class, raise_exception=True):
    """
    Assert that authentication/permission mixins appear before view classes
    in the Method Resolution Order.

    This ensures mixins can properly intercept and control access before
    the view logic executes.

    Args:
        view_class: The view class to validate
        raise_exception: If True, raises MixinOrderError on failure.
                        If False, returns (is_valid, error_message)

    Returns:
        tuple: (True, None) if valid, or (False, error_message) if raise_exception=False

    Raises:
        MixinOrderError: If mixins are in wrong order and raise_exception=True

    Example:
        >>> from trim.tests import assert_mixin_order
        >>> from trim import views
        >>>
        >>> class MyView(views.IsStaffMixin, views.UpdateView):
        ...     model = MyModel
        >>>
        >>> assert_mixin_order(MyView)  # Passes
        (True, None)

        >>> class BadView(views.UpdateView, views.IsStaffMixin):
        ...     model = MyModel
        >>>
        >>> assert_mixin_order(BadView)  # Raises MixinOrderError
    """
    if not issubclass(view_class, View):
        error_msg = f"{view_class.__name__} is not a Django view class"
        if raise_exception:
            raise TypeError(error_msg)
        return (False, error_msg)

    auth_mixins = find_auth_mixins(view_class)
    view_base, view_pos = find_view_base(view_class)

    if not auth_mixins:
        # No auth mixins found, nothing to validate
        return (True, None)

    if view_pos < 0:
        # No view base found (shouldn't happen, but defensive)
        return (True, None)

    # Check each auth mixin position
    problems = []
    for mixin_class, mixin_pos in auth_mixins:
        if mixin_pos > view_pos:
            problems.append(
                f"{mixin_class.__name__} (position {mixin_pos}) "
                f"appears AFTER {view_base.__name__} (position {view_pos})"
            )

    if problems:
        mro_display = " -> ".join([cls.__name__ for cls in view_class.__mro__[:6]])
        error_msg = (
            f"Incorrect mixin order in {view_class.__name__}:\n"
            f"  MRO: {mro_display}\n"
            f"  Problems:\n    - " + "\n    - ".join(problems) + "\n"
            f"  Fix: Place auth mixins BEFORE view classes:\n"
            f"    class {view_class.__name__}(AuthMixin, ViewClass):"
        )

        if raise_exception:
            raise MixinOrderError(error_msg)
        return (False, error_msg)

    return (True, None)


def assert_views_mixin_order(module, raise_exception=True):
    """
    Validate mixin order for all view classes in a module.

    Scans the module for Django view classes and validates each one.

    Args:
        module: Python module containing view classes
        raise_exception: If True, raises on first error. If False,
                        returns list of all errors found.

    Returns:
        list: Empty if all valid, or list of error messages if raise_exception=False

    Raises:
        MixinOrderError: If any view has incorrect order and raise_exception=True

    Example:
        >>> from trim.tests import assert_views_mixin_order
        >>> from myapp import views
        >>>
        >>> # In your test file:
        >>> class ViewTests(TestCase):
        ...     def test_all_views_mixin_order(self):
        ...         assert_views_mixin_order(views)
    """
    import inspect

    errors = []

    for name, obj in inspect.getmembers(module):
        # Check if it's a class and a Django view
        if inspect.isclass(obj) and issubclass(obj, View):
            # Skip the base View class itself
            if obj is View:
                continue

            is_valid, error = assert_mixin_order(obj, raise_exception=False)
            if not is_valid:
                if raise_exception:
                    raise MixinOrderError(error)
                errors.append(error)

    return errors


def get_view_permissions(view_class):
    """
    Extract permission requirements from a view class.

    Args:
        view_class: The view class to inspect

    Returns:
        dict: Dictionary with permission info:
            - 'permissions': list of required permissions
            - 'any': bool, whether ANY permission is sufficient (vs ALL)
            - 'login_required': bool
            - 'staff_required': bool

    Example:
        >>> info = get_view_permissions(MySecureView)
        >>> print(info['permissions'])
        ['myapp.change_model', 'myapp.delete_model']
    """
    info = {
        "permissions": [],
        "any": False,
        "login_required": False,
        "staff_required": False,
        "user_owned": False,
        "user_field": None,
    }

    # Check for PermissionRequiredMixin
    if hasattr(view_class, "permission_required"):
        perms = view_class.permission_required
        if isinstance(perms, str):
            info["permissions"] = [perms]
        else:
            info["permissions"] = list(perms)

        # Check if ANY permission is sufficient
        info["any"] = getattr(view_class, "permission_required_any", False)

    # Check for LoginRequiredMixin
    info["login_required"] = issubclass(view_class, LoginRequiredMixin)

    # Check for staff requirement (trim's IsStaffMixin uses UserPassesTestMixin)
    # We detect by checking for test_func that checks is_staff
    if hasattr(view_class, "test_func"):
        # This is a heuristic - can't perfectly detect without running
        info["staff_required"] = True

    # Check for UserOwnedMixin
    if hasattr(view_class, "user_field"):
        info["user_owned"] = True
        info["user_field"] = view_class.user_field

    return info


def assert_view_has_permission(view_class, permission):
    """
    Assert that a view requires a specific permission.

    Args:
        view_class: The view class to check
        permission: Permission string (e.g., 'myapp.change_model')

    Raises:
        AssertionError: If permission is not required

    Example:
        >>> assert_view_has_permission(
        ...     MyEditView,
        ...     'myapp.change_model'
        ... )
    """
    info = get_view_permissions(view_class)
    if permission not in info["permissions"]:
        raise AssertionError(
            f"{view_class.__name__} does not require permission '{permission}'. "
            f"Current permissions: {info['permissions']}"
        )


def assert_view_requires_login(view_class):
    """
    Assert that a view requires authentication.

    Args:
        view_class: The view class to check

    Raises:
        AssertionError: If view does not require login
    """
    if not issubclass(view_class, (LoginRequiredMixin, AccessMixin)):
        raise AssertionError(
            f"{view_class.__name__} does not require login. "
            f"Add LoginRequiredMixin or another auth mixin."
        )


# Backwards compatibility alias
assert_permissions_mixin_order = assert_mixin_order
