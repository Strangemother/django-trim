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


from django import apps
import importlib

def live_import(module_name):
    """Perform late imports of the target module name within each app
    to ensure any _lazy_ are collected.

    For example, import *.coolapp module for every installed app:

        class ProjectConfig(AppConfig):
            default_auto_field = 'django.db.models.BigAutoField'
            name = 'project'

            def ready(self):
                live_import('coolapp')

    This allows the import of modules for an installed app without mandatory imports
    within the target app.
    """

    _apps = apps.registry.apps

    for conf in _apps.get_app_configs():
        name = conf.label
        # print(' -- App', name)
        # name == 'admin'
        # __name__ == 'django.contrib.admin'
        package_name = conf.module.__name__
        n = f'{package_name}.{module_name}'
        try:
            # print('  Looking for', n)
            vv = importlib.import_module(n)
            print(' -! Imported', vv)
        except ModuleNotFoundError as err:
            if err.name != n:
                # module name mismatch, the failed import is not the
                # one we requested.
                raise err

