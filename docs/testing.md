# Testing Utilities

`trim.tests` provides utilities to validate your view configurations, ensuring best practices and catching common mistakes during development.

## Table of Contents

+ [Quick Start](#quick-start)
+ [Mixin Order Validation](#mixin-order-validation)
+ [Permission Inspection](#permission-inspection)
+ [API Reference](#api-reference)

---

## Quick Start

Import testing utilities in your test files:

```py
from django.test import TestCase
from trim import tests as trim_tests
from myapp import views

class ViewSecurityTests(TestCase):
    def test_view_mixin_order(self):
        """Ensure mixins are in correct order"""
        trim_tests.assert_mixin_order(views.SecureEditView)
    
    def test_all_views(self):
        """Validate all views in the module"""
        trim_tests.assert_views_mixin_order(views)
```

---

## Mixin Order Validation

### Why Order Matters

Django's Method Resolution Order (MRO) determines which methods are called first. Authentication mixins **must** come before view classes to intercept requests:

```py
# ✅ Correct - Mixin runs first
class SecureView(IsStaffMixin, UpdateView):
    pass

# ❌ Wrong - View runs first, bypassing auth check
class InsecureView(UpdateView, IsStaffMixin):
    pass
```

### `assert_mixin_order()`

Validates that authentication/permission mixins appear before view classes in the MRO.

```py
from trim.tests import assert_mixin_order
from myapp.views import MySecureView

# In your test:
def test_mixin_order(self):
    assert_mixin_order(MySecureView)
```

**Detects these mixins:**
- `LoginRequiredMixin`
- `PermissionRequiredMixin`
- `UserPassesTestMixin`
- `AccessMixin`
- Any subclass (including `trim.views.IsStaffMixin`, `UserOwnedMixin`, etc.)

**Error Output:**

```
MixinOrderError: Incorrect mixin order in MySecureView:
  MRO: MySecureView -> UpdateView -> UserPassesTestMixin -> SingleObjectMixin -> View
  Problems:
    - UserPassesTestMixin (position 2) appears AFTER UpdateView (position 1)
  Fix: Place auth mixins BEFORE view classes:
    class MySecureView(AuthMixin, ViewClass):
```

### `assert_views_mixin_order()`

Validates **all** view classes in a module:

```py
from trim.tests import assert_views_mixin_order
from myapp import views

class ViewTests(TestCase):
    def test_all_views_configured_correctly(self):
        """Ensure all views have correct mixin order"""
        assert_views_mixin_order(views)
```

**Non-raising mode** (collect all errors):

```py
def test_collect_errors(self):
    errors = assert_views_mixin_order(views, raise_exception=False)
    if errors:
        self.fail(f"Found {len(errors)} mixin order issues:\n" + 
                  "\n---\n".join(errors))
```

---

## Permission Inspection

### `get_view_permissions()`

Extract permission and authentication requirements from a view:

```py
from trim.tests import get_view_permissions

info = get_view_permissions(MySecureView)
print(info)
# {
#     'permissions': ['myapp.change_model', 'myapp.delete_model'],
#     'any': False,  # Requires ALL permissions
#     'login_required': True,
#     'staff_required': True,
#     'user_owned': False,
#     'user_field': None
# }
```

**Return Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `permissions` | `list[str]` | Required Django permissions |
| `any` | `bool` | If `True`, user needs ANY permission (not ALL) |
| `login_required` | `bool` | View requires authentication |
| `staff_required` | `bool` | View has a `test_func` (heuristic for staff checks) |
| `user_owned` | `bool` | View uses `UserOwnedMixin` |
| `user_field` | `str` or `None` | Field name for user ownership check |

### `assert_view_has_permission()`

Verify a view requires a specific permission:

```py
from trim.tests import assert_view_has_permission

def test_edit_permission(self):
    assert_view_has_permission(
        views.ArticleEditView,
        'blog.change_article'
    )
```

Raises `AssertionError` if the permission is not required.

### `assert_view_requires_login()`

Verify a view requires authentication:

```py
from trim.tests import assert_view_requires_login

def test_profile_requires_login(self):
    assert_view_requires_login(views.UserProfileView)
```

---

## API Reference

### Core Functions

#### `assert_mixin_order(view_class, raise_exception=True)`

Validate mixin order for a single view class.

**Parameters:**
- `view_class`: View class to validate
- `raise_exception`: If `False`, returns `(is_valid, error_message)` tuple

**Returns:** `(True, None)` if valid

**Raises:** `MixinOrderError` if invalid (when `raise_exception=True`)

---

#### `assert_views_mixin_order(module, raise_exception=True)`

Validate all views in a module.

**Parameters:**
- `module`: Python module containing view classes
- `raise_exception`: If `False`, returns list of error messages

**Returns:** `[]` if all valid, or list of errors

**Raises:** `MixinOrderError` on first error (when `raise_exception=True`)

---

#### `get_view_permissions(view_class)`

Extract permission and auth requirements.

**Parameters:**
- `view_class`: View class to inspect

**Returns:** `dict` with keys:
- `permissions`, `any`, `login_required`, `staff_required`, `user_owned`, `user_field`

---

#### `assert_view_has_permission(view_class, permission)`

Assert view requires specific permission.

**Raises:** `AssertionError` if permission not required

---

#### `assert_view_requires_login(view_class)`

Assert view requires authentication.

**Raises:** `AssertionError` if login not required

---

### Helper Functions

#### `get_mro_position(klass, target_class)`

Get position of a class in the Method Resolution Order.

**Returns:** `int` position, or `-1` if not found

---

#### `find_auth_mixins(klass)`

Find all auth/permission mixins in a view.

**Returns:** `list` of `(mixin_class, position)` tuples

---

#### `find_view_base(klass)`

Find the base Django view class.

**Returns:** `(view_class, position)` tuple, or `(None, -1)`

---

## Complete Example

```py
# tests/test_views.py
from django.test import TestCase
from trim import tests as trim_tests
from myapp import views


class ViewConfigurationTests(TestCase):
    """Validate view security configuration"""
    
    def test_all_views_mixin_order(self):
        """All views must have correct mixin order"""
        trim_tests.assert_views_mixin_order(views)
    
    def test_article_edit_security(self):
        """Article edit requires correct permissions"""
        trim_tests.assert_mixin_order(views.ArticleEditView)
        trim_tests.assert_view_has_permission(
            views.ArticleEditView,
            'blog.change_article'
        )
    
    def test_profile_requires_auth(self):
        """User profile requires login"""
        trim_tests.assert_view_requires_login(views.UserProfileView)
    
    def test_admin_dashboard_permissions(self):
        """Admin dashboard has correct config"""
        info = trim_tests.get_view_permissions(views.AdminDashboardView)
        
        self.assertTrue(info['staff_required'])
        self.assertTrue(info['login_required'])
    
    def test_user_owned_resources(self):
        """User-owned views configured correctly"""
        info = trim_tests.get_view_permissions(views.AddressDetailView)
        
        self.assertTrue(info['user_owned'])
        self.assertEqual(info['user_field'], 'owner')


class IndividualViewTests(TestCase):
    """Test specific view configurations"""
    
    def test_dangerous_view_not_misconfigured(self):
        """Critical views must have correct security"""
        critical_views = [
            views.DeleteUserView,
            views.AdminPanelView,
            views.PaymentProcessView,
        ]
        
        for view in critical_views:
            with self.subTest(view=view.__name__):
                trim_tests.assert_mixin_order(view)
                # Ensure it has SOME form of protection
                info = trim_tests.get_view_permissions(view)
                self.assertTrue(
                    info['permissions'] or 
                    info['login_required'] or 
                    info['staff_required'],
                    f"{view.__name__} has no security configuration!"
                )
```

---

## Best Practices

### 1. Test Early, Test Often

Add mixin order tests as soon as you create secured views:

```py
def test_new_secure_view(self):
    trim_tests.assert_mixin_order(views.NewSecureView)
```

### 2. Use Module-Wide Tests

Test all views at once to catch issues:

```py
def test_all_views(self):
    trim_tests.assert_views_mixin_order(views)
```

### 3. Document Security Requirements

Combine tests with documentation:

```py
def test_payment_view_security(self):
    """Payment view requires:
    - User authentication
    - 'payments.process_payment' permission
    - User ownership of payment method
    """
    view = views.ProcessPaymentView
    trim_tests.assert_mixin_order(view)
    trim_tests.assert_view_has_permission(view, 'payments.process_payment')
    
    info = trim_tests.get_view_permissions(view)
    self.assertTrue(info['user_owned'])
```

### 4. CI/CD Integration

Run these tests in your continuous integration pipeline to prevent security misconfigurations from reaching production.

---

## Related

- [Authenticated Views](views/authed-views.md)
- [Views Overview](views/readme.md)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
