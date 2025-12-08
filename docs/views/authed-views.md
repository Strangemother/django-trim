# Authenticated & Permissioned Views

Quickly integrate authentication and permission checks into your views using `trim` mixins. These mixins provide declarative access control for Admin, Staff, and User-owned resources.

## Table of Contents

+ [Permissioned](#permissioned)
+ [IsStaffMixin](#isstaffmixin)
+ [UserOwnedMixin](#userownedmixin)
+ [Combining Mixins](#combining-mixins)
+ [Best Practices](#best-practices)

---

## Permissioned

`trim.views.Permissioned` is an alias for Django's `PermissionRequiredMixin`, providing a shorter, more convenient import for permission-based access control.

### Basic Usage

```py
from trim import views

class EditIndexView(views.Permissioned, views.TemplateView):
    permission_required = 'pages.change_mymodel'
    template_name = 'pages/edit_index.html'
```

### Multiple Permissions

You can require multiple permissions using a list or tuple:

```py
class SecureEditView(views.Permissioned, views.UpdateView):
    permission_required = ['pages.change_mymodel', 'pages.view_mymodel']
    # User must have ALL listed permissions
    model = models.MyModel
```

### Permission Logic

By default, the user must have **all** permissions listed. To require **any** permission instead:

```py
class FlexibleEditView(views.Permissioned, views.UpdateView):
    permission_required = ['pages.change_mymodel', 'pages.delete_mymodel']
    permission_required_any = True  # User needs ANY of the permissions
    model = models.MyModel
```

### Customizing Denied Behavior

```py
class CustomDeniedView(views.Permissioned, views.TemplateView):
    permission_required = 'pages.change_mymodel'
    permission_denied_message = "You don't have permission to edit this page."
    login_url = '/accounts/login/'  # Redirect unauthenticated users here
    raise_exception = True  # Raise 403 instead of redirecting (default: False)
```

**Note**: Permission strings follow the format `'app_label.codename'` (e.g., `'myapp.change_modelname'`).

---

## IsStaffMixin

Restricts access to staff or admin users only. This mixin uses `UserPassesTestMixin` internally and checks both `is_staff` and `is_superuser` flags.

### Basic Usage

```py
from trim import views

class StaffDashboardView(views.IsStaffMixin, views.TemplateView):
    template_name = 'admin/dashboard.html'
```

### How It Works

The mixin allows access if the user:
- Is authenticated (`is_active = True`)
- Is staff (`is_staff = True`) **OR**
- Is a superuser (`is_superuser = True`)

### Example: Staff-Only ListView

```py
class StaffUserListView(views.IsStaffMixin, views.ListView):
    model = User
    template_name = 'admin/users_list.html'
    context_object_name = 'users'
```

### Denied Access

Unauthenticated users are redirected to the login page (configurable via `LOGIN_URL` setting). Authenticated non-staff users receive a 403 Forbidden response.

---

## UserOwnedMixin

Ensures that the object being accessed belongs to the requesting user. This is ideal for user-specific resources like profiles, addresses, or personal settings.

### Basic Usage

```py
from trim import views

class AddressDetailView(views.UserOwnedMixin, views.DetailView):
    model = models.Address
    user_field = 'creator'  # Field on Address model that references the User
    template_name = 'locality/address_detail.html'
```

### Configuration Options

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `user_field` | `str` | `'user'` | Field name on the model that references the owning user |
| `user_allow_staff` | `bool` | `False` | If `True`, staff/admin can access any user's objects |

### Example: User Profile with Staff Override

```py
class UserProfileView(views.UserOwnedMixin, views.DetailView):
    model = models.UserProfile
    user_field = 'user'
    user_allow_staff = True  # Admins can view any profile
    template_name = 'accounts/profile_detail.html'
```

In this example:
- Regular users can only view their own profile
- Staff and admin users can view any user's profile

### Example: Editing User-Owned Content

```py
class EditAddressView(views.UserOwnedMixin, views.UpdateView):
    model = models.Address
    user_field = 'owner'
    fields = ['street', 'city', 'zip_code']
    template_name = 'locality/address_form.html'
    success_url = '/addresses/'
```

### Error Handling

If the specified `user_field` doesn't exist on the model, a `MissingField` exception is raised:

```py
# If 'creator' field doesn't exist on Address model:
# MissingField: creator
```

**Tip**: Ensure your model has the correct foreign key field before using this mixin.

---

## Combining Mixins

You can combine multiple mixins for complex access control scenarios. **Order matters**: mixins are evaluated left-to-right.

### Example: Staff or Owner

```py
from trim import views

class AddressEditView(views.UserOwnedMixin, views.UpdateView):
    model = models.Address
    user_field = 'creator'
    user_allow_staff = True  # Staff can edit any address
    fields = ['street', 'city', 'state', 'zip_code']
```

### Example: Permission + Ownership

```py
class SecureEditView(views.Permissioned, views.UserOwnedMixin, views.UpdateView):
    model = models.Document
    permission_required = 'documents.change_document'
    user_field = 'author'
    user_allow_staff = False  # Even staff need to own the document
```

In this case, the user must have the `change_document` permission **AND** own the document.

---

## Best Practices

### 1. Choose the Right Mixin

- **`Permissioned`**: Use for role-based access (Django permissions)
- **`IsStaffMixin`**: Use for admin/staff-only views
- **`UserOwnedMixin`**: Use for user-specific resource protection

### 2. Mixin Order

Place authentication mixins **before** view classes:

```py
# ✅ Correct
class MyView(views.IsStaffMixin, views.UpdateView):
    pass

# ❌ Wrong - may not work as expected
class MyView(views.UpdateView, views.IsStaffMixin):
    pass
```

### 3. Test Your Access Control

Always test with different user types:
- Unauthenticated users
- Regular authenticated users
- Staff users
- Superusers

### 4. Custom Error Messages

Provide clear feedback when access is denied:

```py
class MyView(views.Permissioned, views.TemplateView):
    permission_required = 'myapp.special_access'
    permission_denied_message = "Please contact an administrator for access."
```

### 5. Use `user_allow_staff` Wisely

Setting `user_allow_staff=True` on `UserOwnedMixin` gives staff/admin full access. Only use this when appropriate for your security model.

---

## Related

- [Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Django Permissions](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization)
- [trim Views Overview](readme.md)
