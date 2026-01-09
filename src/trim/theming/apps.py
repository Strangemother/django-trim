from django.apps import AppConfig
from trim.apps import live_import
from . import context

from django.conf import settings


class ThemingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trim.theming"

    def ready(self):
        context.build_default_themer()
        # Import /app/theming.py from all apps
        # print(' -- live importing theming')
        live_import("theming")
