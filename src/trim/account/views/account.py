from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from trim import views as shorts

from .. import models


class PasswordChangeView(LoginRequiredMixin, shorts.FormView):
    model = shorts.get_user_model()
    form_class = PasswordChangeForm
    success_url = reverse_lazy("account:profile")

    template_name = "account/user_password_change.html"

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        if self.request.method == "POST":
            kwargs["data"] = self.request.POST
        return kwargs


class ProfilePasswordUpdateView(PasswordChangeView):
    # model = CustomUser
    template_name = "account/password_update_form.html"


def logout_view(request):
    logout(request)


class ProfileLogout(LogoutView):
    template_name = "account/logged-out.html"


class ProfileLogin(LoginView):
    template_name = "account/login.html"


class ProfileInactiveAccount(shorts.TemplateView):
    template_name = "account/inactive.html"


from django.contrib.auth import views as auth_views


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "account/forgotpasswordrecord_form.html"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        # If the email address is a registered user, send the email.
        U = shorts.get_user_model()
        email_field_name = U.get_email_field_name()
        # exists = U.objects.filter(email__iexact=email).exists()
        active_users = U._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )

        models.ForgotPasswordRecord.objects.create(email_address=email)

        for u in active_users:
            hup = u.has_usable_password()
            s = f"PasswordResetView::Requested email exists? has_usable_password: {hup}"
            print(s, u, email)

        return super().form_valid(form)


# class ProfileForgotPasswordView(shorts.CreateView):
#     model = models.ForgotPasswordRecord
#     fields = ('email_address',)
#     success_url = reverse_lazy('account:forgot_success')

#     def form_valid(self, form):
#         email = form.cleaned_data['email_address']
#         # If the email address is a registered user, send the email.
#         U = shorts.get_user_model()
#         exists = U.objects.filter(email__iexact=email).exists()
#         print('Requested email exists?', email, exists)
#         if exists:
#             self.send_reset_email(email)
#         return super().form_valid(form)

#     def send_reset_email(self, email_address):
#         # password reset here.
#         print('send email!')


class ProfileForgotPasswordSuccessView(shorts.TemplateView):
    template_name = "account/password-reset-success-view.html"
