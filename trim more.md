
trim packages act like standard modules
The parent is a directory, installed as a standard module - by the trim packager.

The trim packager maintains its own record of changes,
normal migrations enact those changes
a trim package list is managed through db and file/folders, or a simple list.
    All three are allowed.


# user passes test

Extend the django class `UserPassesTest` to include ready-to-build subcomponents:

+ UserIsAdmin
+ UserIsStaff
+ UserInGroup

With prebuilt classes for deeper inspection

## UserIsField

A user should match a field within the target object

```py
class OtherView(UserIsField, TemplateView):
    user_test_field = 'publisher'
    # ...
```

