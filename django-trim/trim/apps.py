from django.apps import AppConfig

from django.db.models.signals import pre_init

class ShortConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trim'

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals
        # Explicitly connect a signal handler.
        pre_init.connect(signals.model_pre_init)
