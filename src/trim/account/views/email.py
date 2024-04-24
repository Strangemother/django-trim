from django.http import Http404

from .profile import ProfileUpdateView
from trim import views
from .. import models, forms

try:
    from mailroom import mail
    has_mail = True
except ImportError:
    print('mailroom app is not installed.')
    has_mail = False

from trim.urls import absolute_reverse

# class VerifiedEmailUpdateView(trim.):
class VerifiedEmailUpdateView(ProfileUpdateView):
    """Upon save generate a token and send an email
    When the user verifys, set the user primary to the new record.

    on update create change record
    send email to primary, and secondary
    Upon secondary accept, change the primary email.

    The flow is tokenized.,
    """
    success_url = views.reverse_lazy('account:profile')
    model = models.AccountEmail
    # model = views.get_user_model()
    fields = ( 'email_address', )

    def get_initial(self):
        return {
            'user': self.request.user,
            'email_address':self.request.user.email,
        }

    def form_valid(self, form):
        """If the form is valid, dont save the associated model."""
        self.object = form.save()
        self.send_email()
        return super().form_valid(form)

    def send_email(self):
        user_emails = (self.request.user.email)
        url = absolute_reverse(self.request, 'account:verify_email_token')
        tokened_url = absolute_reverse(self.request, 'account:verify_email_token', self.object.uuid_token)
        if has_mail:
            mail.template_send('verify_email_change', user_emails,
                user=self.request.user,
                accountemail=self.object,
                url=url,
                tokened_url=tokened_url,
                )
        # new_email = self.object.email_address
        # mail.template_send('confirm_email_ownership', new_email,
        #     user=self.request.user,
        #     accountemail=self.object,
        #     url=url)

    def get_object(self, queryset=None):
        if queryset is None:
            return self.new_model()
        try:
            return super().get_object(queryset)
        except (AttributeError, models.AccountEmail.DoesNotExist, Http404):
            return self.new_model()

    def new_model(self):
        m, c = self.model.objects.get_or_create(
            user=self.request.user,
            verified=None,
            )
        return m


class VerifyEmailTokenView(views.FormView):
    """A user may enter a GET form withthe token in the header.
    """
    success_url = views.reverse_lazy('account:profile')
    model = models.AccountEmail
    form_class = forms.EmailChangeToken
    template_name = 'account/form.html'
    query_pk_and_slug = True
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid_token'

    def get_initial(self):
        r = self.initial.copy()
        r['token'] = self.kwargs.get('uuid')
        return r

    def get(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """Test the form token against the verfied user and form."""
        data = form.cleaned_data
        token = data['token']
        user = self.request.user
        try:
            ae = self.model.objects.get(uuid_token=token)
        except self.model.DoesNotExist:
            # inject error here.
            print('Cannot find model of', token)
            return self.form_invalid(form)

        if ae.user.id != user.id:
            # inject error here.
            return self.form_invalid(form)

        ae.verified = now()
        user.email = ae.email_address
        user.save()
        ae.save()

        return super().form_valid(form)

from django.utils.timezone import now
