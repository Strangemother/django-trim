# trim.apps

## Live Import

> Build your own app live loading tool, to automatically integrate convention named files

The `trim.apps.live_import` function allows you to build autoloading modules for incoming django apps. Similar to djangos automatic loading of _models.py_ and other core components.

You may _capture_ the module during load-time and perform early interactions with the django app, before the site is live.

```py
from trim.apps import live_import
# load root/*/subfile.py from every app
live_import('subfile')
```

Importantly this should be called during the correct load phase to ensure live app hooking, such as an apps `app.py` ready call of your primary app:

```py
from django.apps import AppConfig
from trim.apps import live_import

class ProjectConfig(AppConfig):
    def ready(self):
        live_import('subfile')
```

## Usage

As an example we be a resource provider. Our integration requires the file `coolapp.py` to exist at the root of an application:

_directory layout_
    root/mysite/
      mysite/
        - settings.py
        - urls.py
        - wsgi.py
      fooapp/
        - views.py
        - models.py
        - coolapp.py
      otherapp/
        - views.py
        - models.py
        - coolapp.py
      - manage.py
      - requirements.txt

With our application prepped we can build an application to _load_ the `coolapp` files:

_directory layout_
    root/mysite/
      cooler/
        - app.py
        - views.py
        - models.py
      ...
      - manage.py

Within the `app.py` of the parent app (in this case `cooler`), perform late imports of the target module name within each app:

import \*.coolapp module for every installed app:

```py
from trim.apps import live_import

from django.apps import AppConfig

class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'

    def ready(self):
        ...
        live_import('coolapp')
```

This allows the import of modules for an installed app without mandatory imports within the target app. Any app without the target file `coolapp.py`, it will silently fail.
