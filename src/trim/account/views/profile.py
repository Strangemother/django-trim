from django.http import Http404
# from django.utils.translation import ugettext_lazy  as _
from django.utils.translation import gettext as _

from trim import views


class ProfileNewAccount(views.TemplateView):
    template_name = "account/new-profile.html"


class ProfileView(views.TemplateView):
    template_name = "account/profile.html"


class ProfileUpdateView(views.UpdateView):
    success_url = views.reverse_lazy("account:profile")
    template_name = "account/profile_form.html"
    model = views.get_user_model()
    fields = (
        "first_name",
        "last_name",
        # 'username',
    )

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.
        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        queryset = queryset.filter(pk=self.request.user.pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist as err:
            d = {"verbose_name": queryset.model._meta.verbose_name}
            msg = _("No %(verbose_name)s found matching the query") % d
            raise Http404(msg) from err
        return obj


class ProfileUsernameUpdateView(ProfileUpdateView):
    fields = ("username",)


class ProfileEmailUpdateView(ProfileUpdateView):
    fields = ("email",)
