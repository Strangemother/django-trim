# Views

Trim is designed to short-cut your imports. To use a common-set of django and `trim` views:

```py
from trim import views


class EditIndexView(views.Permissioned, views.TemplateView):
    permission_required = 'pages.change_MyModel'
```

+ [Serialized views](./seralized.md): JSON mostly
+ [Authed views](./seralized.md): Permissioned views and ownership mixins
    + [Permissioned](./seralized.md#Permissioned)
    + [IsStaffMixin](./seralized.md#IsStaffMixin)
    + [UserOwnedMixin](./seralized.md#UserOwnedMixin)

