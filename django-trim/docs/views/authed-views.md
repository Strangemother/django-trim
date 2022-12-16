# Permissioned Views

Quickly integrate Admin, staff, and user permissioned views using `trim.Permissioned` and other mixins.

## Permissioned

`trim.views.Permissioned` is the `PermissionRequiredMixin`

```py
from trim import views

class EditIndexView(views.Permissioned, views.TemplateView):
    permission_required = 'pages.change_MyModel'
```

## IsStaffMixin

Apply a test to ensure the user is Staff or Admin

```py
from trim import views

class EditIndexView(views.IsStaffMixin, views.TemplateView):
    # only admin may enter
    pass
```

## UserOwnedMixin

Ensure the user owning the inner model `get_object()` is the requesting user.

```py
    from trim import views

    class AddressDetailView(views.UserOwnedMixin, views.DetailView):
        user_field = 'creator'
        user_allow_staff = True

        model = models.Address
        ...
```

In this example the `Address` model should have a `user` field, and the user must be the user making the request. By applying `user_allow_staff=True` - we also ensure admins can view this page.
