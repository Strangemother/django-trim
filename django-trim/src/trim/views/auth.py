from django.contrib.auth.mixins import UserPassesTestMixin

def is_staff_or_admin(user):
     return user.is_superuser or user.is_staff


class IsStaffMixin(UserPassesTestMixin):
    """
    Allow if the user is staff or admin.
    """
    def test_func(self):
        uu = self.request.user
        active_staff = uu.is_active and is_staff_or_admin(uu)
        return active_staff


class MissingField(Exception):
    pass


class UserOwnedMixin(UserPassesTestMixin):
    """
    Ensure the user owning the inner model `get_object()` is the requesting user.

        from trim.views import UserOwnedMixin
        class AddressDetailView(UserOwnedMixin, shorts.DetailView):
            model = models.Address
            user_field = 'creator'
            user_allow_staff = True
            template_name = 'locality/address_detail.html'
    """
    user_field = 'user'
    user_allow_staff = False

    def test_func(self):
        uu = self.request.user
        request_pk = uu.pk
        model_user = getattr(self.get_object(), self.user_field)

        try:
            owns = model_user.pk == request_pk
        except AttributeError as err:
            raise MissingField(self.user_field) from err

        is_admin = is_staff_or_admin(uu) if self.user_allow_staff else False
        active_staff = uu.is_active and (owns or is_admin)

        return active_staff
