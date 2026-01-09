from django.contrib import admin

from trim import admin as tadmin

from . import models

# @tadmin.register(models.AccountEmail)
# class AccountEmail(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'email_address',
#         'verified',
#         'created',
#         'updated',
#         )


tadmin.register_models(models, ignore=__name__)
