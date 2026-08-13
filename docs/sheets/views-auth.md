# Views: Authentication and Ownership

`trim.views.auth` provides authentication-related view imports plus mixins for staff-only and object-owner access checks.

## Import

```py
from trim import views
```

Django's `LoginView` and `LogoutView` are available through the module:

```py
class LoginView(views.LoginView):
    template_name = "registration/login.html"

class LogoutView(views.LogoutView):
    next_page = "/"
```

## Helpers and Mixins

| Object | Example | Purpose |
| --- | --- | --- |
| `is_staff_or_admin` | `allowed = views.is_staff_or_admin(request.user)` | Returns `True` for a superuser or staff user. |
| `IsStaffMixin` | `class StaffView(views.IsStaffMixin, views.DetailView): ...` | Allows active staff or superusers only. |
| `UserOwnedMixin` | `class AddressView(views.UserOwnedMixin, views.DetailView): ...` | Allows the requesting user to access their own object, with optional staff access. |
| `MissingField` | `raise views.MissingField("user")` | Exception raised when the ownership field is absent from the object. |

## Staff-Only View

```py
class StaffReportView(views.IsStaffMixin, views.TemplateView):
    template_name = "reports/staff.html"
```

`IsStaffMixin.test_func()` requires both `request.user.is_active` and either `is_staff` or `is_superuser`.

## User-Owned View

```py
class AddressDetailView(views.UserOwnedMixin, views.DetailView):
    model = Address
    user_field = "creator"
    user_allow_staff = True
    template_name = "locality/address_detail.html"
```

Configuration:

- `user_field` defaults to `"user"` and names the object attribute containing the owner.
- `user_allow_staff` defaults to `False`; set it to `True` to allow active staff/admin users.
- The requesting user must be active and own the object unless staff access is enabled.

The mixin calls `get_object()`, so it works with `DetailView`, `UpdateView`, and other object-based views. A missing `user_field` raises `MissingField` instead of silently denying access.

## Permissioned Alias

The `Permissioned` alias is defined in `trim.views.base` but commonly used with authentication views:

```py
class EditAccountView(views.Permissioned, views.UpdateView):
    permission_required = "accounts.change_account"
    model = Account
    fields = ["display_name"]
```
