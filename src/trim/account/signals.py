from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

# @receiver(user_logged_in)
# def post_login(sender, user, request, **kwargs):
#     print('Post Login event', request.session.get('cart_id'))


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        models.Account.objects.create(user=instance)
