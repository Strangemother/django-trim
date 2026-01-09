from trim import views

from .. import dispatch, forms, models

# __all__ = ['EmailInviteCreateView']


class EmailInviteCreateView(views.CreateView):
    model = models.EmailInvite
    fields = (
        "email_address",
        # 'user',
    )

    def get_initial(self):
        return {"user": self.request.user}

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        dispatch.send_invite.send(sender=self.__class__, object=self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return views.reverse("account:profile")


class EmailInviteListView(views.ListView):
    model = models.EmailInvite

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
