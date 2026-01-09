from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path

from trim import urls as t_urls

from . import views

app_name = "account"

urlpatterns = t_urls.paths_named(
    views,
    profile=(
        "ProfileView",
        (
            "",
            "profile/",
        ),
    ),
    edit=(
        "ProfileUpdateView",
        "profile/edit/",
    ),
    edit_username=(
        "ProfileUsernameUpdateView",
        "profile/edit/username/",
    ),
    edit_password=(
        "ProfilePasswordUpdateView",
        "profile/edit/user-information/",
    ),
    edit_email=(
        "ProfileEmailUpdateView",
        "profile/edit/email/now/",
    ),
    edit_email_verified=(
        "VerifiedEmailUpdateView",
        "profile/edit/email/",
    ),
    # home=('ProfileView', '',),
    logout=(
        "ProfileLogout",
        "logout/",
    ),
    login=(
        "ProfileLogin",
        "login/",
    ),
    new=(
        "ProfileNewAccount",
        "welcome/",
    ),
    inactive=(
        "ProfileInactiveAccount",
        "inactive/",
    ),
    forgot_success=(
        "ProfileForgotPasswordSuccessView",
        "forgot/sent/",
    ),
    invite=(
        "EmailInviteCreateView",
        "invite/",
    ),
    invites=(
        "EmailInviteListView",
        "invites/",
    ),
)


urlpatterns += [
    path(
        "forgot/",
        views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "profile/edit/email/verify/",
        views.VerifyEmailTokenView.as_view(),
        name="verify_email_token",
    ),
    path(
        "profile/edit/email/verify/<str:uuid>/",
        views.VerifyEmailTokenView.as_view(),
        name="verify_email_token",
    ),
]
