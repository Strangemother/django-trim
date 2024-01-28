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


## Results

The first question may be - where do the imports go?

The `trim.live_import` fundamentally _"actives"_ the module, ensuring it's imported before your Django app wakes up. Without this, you would need to `import coolapp` somewhere within the app.


An example of "waking up" all modules across all apps:

```py
    from trim.apps import live_import
    loaded = live_import('coolapp')
    # e.g. All 10 django apps are tested:
    # blog.coolapp
    # search.coolapp
    # accounts.coolapp      # Found!
    # ...
    # contacts.coolapp
    # stocks.coolapp
    # string_integration.coolapp
    # home.coolapp
```

`live_import` helps perform an _import_ on all modules named `coolapp` (or anything you prefer) within all apps within your Django site.

### Example

You can inspect the modules and utilise the content within, naturally integrating components will mount as per normal python modules.

For example we could provide tooling to capture admin links, and reference them from all custom apps. In our `admintools.py` we apply some `LINKS`. The `trim.live_import` can reference the links:

_admin_tools.py_
```py
from admin_tools import links

ADMIN_LINKS = (
    links.Link(
            label='Users',
            group='Authentication',
            hyperlink='#'
        ),
)
```

When required, we can import all the modules matching `root/*/admintools.py`, and discover the `ADMIN_LINKS`:

```py

class IndexView(views.TemplateView):
    template_name = 'admin_tools/index.html'

    def get_context_data(self, **kwargs):
        """Collect the admintools.py file from all sibiling apps
        and apply them the context.
        """
        # load root/*/admintools.py from every app
        loaded = live_import('admintools')
        links = ()
        for module in loaded:
            links += getattr(module, 'ADMIN_LINKS', ())
        kwargs['links'] = links
        return kwargs
```

In our template, we can iterate the links as expected:

```jinja
{% for link in links %}
    <a href="{{ link.hyperlink }}">{{ link.label }}</a>
{% endfor %}
```

