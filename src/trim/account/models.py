from django.db import models
from trim.models import fields
from trim import models as trims


class AccountEmail(models.Model):
    # A friendly name
    user = fields.fk_user(nil=True)
    name = fields.chars()
    email_address = fields.email()
    uuid_token = fields.str_uuid()
    # DT The user verified.
    verified = fields.datetime(nil=True)

    created = fields.dt_created()
    updated = fields.dt_updated()


class Account(models.Model):
    """Assign a user to the internal system of assets."""

    user = fields.o2o_user()

    verified = fields.datetime(nil=True)
    # identify alterntive email address as authenticated and purchases
    associated_emails = fields.m2m(AccountEmail)

    created = fields.dt_created()
    updated = fields.dt_updated()


class EmailInvite(models.Model):
    user = fields.fk_user()

    email_address = fields.email(help_text="The target user email address")
    uuid_token = fields.str_uuid()

    accepted = fields.datetime(nil=True)
    expires = fields.datetime(nil=True)

    created, updated = fields.dt_cu_pair()


class ForgotPasswordRecord(models.Model):
    email_address = fields.email()
    # has_usable_password = fields.bool()
    created, updated = fields.dt_cu_pair()
