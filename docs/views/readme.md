# Views

Trim is designed to short-cut your imports. To use a common-set of django and `trim` views:

```py
from trim import views


class EditIndexView(views.Permissioned, views.TemplateView):
    permission_required = 'pages.change_MyModel'
```

+ [Serialized views](./serialized.md): JSON mostly
+ [Authed views](./authed-views.md): Permissioned views and ownership mixins
    + [Permissioned](./serialized.md#Permissioned)
    + [IsStaffMixin](./serialized.md#IsStaffMixin)
    + [UserOwnedMixin](./serialized.md#UserOwnedMixin)

