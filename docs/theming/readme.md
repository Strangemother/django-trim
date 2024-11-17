# Theming

> Trim themes allows you to pre-load template paths as simple words in a central file, allowing you to leverage your own managed theme pack or just simplify your template extends

The "theming" or a plain or `trim.theme` app provides a new layer of abstraction on-top of the standard django templating, to centralise the a _theme_ of files for your website:

```py
# themes.py
from trim.theming import install

SITE_THEMES = {
    'detail': '/foo/name.html',
    'other': '/foo/name.html',
}

SCOPE = install(SITE_THEMES)
```

```jinja
<!-- model detail view.html -->
{% theme "detail" %}
{% block content %}
    {{ object}}
{% endblock %}
```

The `theme` template tag acts just like the `{% extends "filename.html" %}`, except you can provide uniquly created _theme_ named files from your `theming.py` definition.

It allows you to write a dictionary definitions of the target theme, then use it across all your files. You can use this to simplify your own templating imports, or provide a _ready to go_ box of themes for an end-user.

## Installation

Apply `trim.theming` to your `INSTALLED_APPS`:

```py
INSTALLED_APPS = [
    'trim.theming',
    ...
]
```

`settings.py` configurations are optional, we recommend the packaged `theming.py` autoloading method, as this easier to transport if you're supplying packages to the wild.


Insert `'trim.theming.builtins'` to your 'builtins' list for the template renderer:

```py

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        ...

        "OPTIONS": {

            # Add to TEMPLATES.OPTIONS.builtins
            'builtins': [
                ...
                'trim.theming.builtins',
            ],
            "context_processors": [ ... ],
        },
    },
]
```

### Settings.py

The theming library utilises a dictionary as a mappings for target templates.

#### `THEMING_OPTIONS`

The _options_ assign the `root` and core `version` of your installed fileset. By default the `root` looks for a `theme/` directory. If we changed this to `foo/` the library would attempt to discover `*/templates/foo/*.html`.

```py
## Baked 'settings' for the theming unit. These vars stay bound outside
# the options of the template usage. In some cases (such as `version`) the
# option may be overridden - but generally these should be static during
# runtime.
THEMING_OPTIONS = {
    'root': 'theme',
    'version': '',
}
```

#### `THEMING_MAP`

We can install an optional _mapping_ of _name_ to _filename_ for our theme. Each key becomes an importable name:

```py
## The name -> file map exposed through the {% theme %} and {{ theme }}
# template tags. This is mapped into the _forced_ theming options, ensuring
# the templates may call _into_ one directory. By default this is the given
# "theme"
THEMING_MAP = {
    'detail.double': 'detail-double-header.html',
    'detail.default': 'detail.html',
}
```

Example:

```html
{% theme "detail" %}
{% theme "detail" "default" %}
{% theme "detail" "double" %}
```

## `theming.py`

In addition to the `settings` integration `trim.theming` accepts a `theming.py` at the root of any application. This is automatically loaded and allows the app to install additional theme template mappings

An example file setup:

    books
        models.py
        ...
        theming.py
    locations
        models.py
        ...
        theming.py
    mysite
        settings.py
        urls.py

    manage.py

The two files `books/theming.py` and `locations/theming.py` are automatically loaded.

### Installing a "pack"

Install your additional or _redirects_ within your `app/themes.py`

```py
from trim.theming import install

SITE_THEMES = {
    'detail': '/foo/name.html',
    'egg': '/foo/name.html',
}

SCOPE = install(SITE_THEMES)
```

They become the extends:

```html
{% theme "detail" %}
```

```html
{% theme "egg" %}
```

## Templates

The `theming` library utilises your custom themes. You can build your own, or copy the `trim` defaults from the `theming/templates/theme/*` directory

Create your `templates/theme/`. Defaults include:

+ page: `templates/theme/page.html`
+ form-page: `templates/theme/page.html`
+ detail: `templates/theme/page.html`
+ list: `templates/theme/page.html`

All theme templates extends `page: "theme/page.html"` - This extends the site-wide `"base.html"`

### Changing Default Templates

You may wish to _redirect_ the default template name to your own template. This is useful if you want to change a global name, such as `"detail"` to your new replacement

```py
from trim.theming improt name_default_redirect
name_default_redirect('detail', 'double', 'detail-double-header.html',)
```

Before:

```html
{% theme "detail" %} # theme/detail.html
```

After:

```html
{% theme "detail" %} # theme/detail-double-header.html
{% theme "detail" "double" %} # theme/detail-double-header.html
{% theme "detail.double" %} # theme/detail-double-header.html

{% theme "detail" "default" %} # theme/detail.html
{% theme "detail.default" %} # theme/detail.html
```

The `detail.default` is still accessible, and reverts to the settings within `trim.theming.config.THEMING_MAPS_DEFAULT`.

#### Example

Install a _default redirect_, allowing the import of the "detail" and it invisibly resolves "detail.double" with the addition "details.default" created automatically.

    name_default_redirect('detail', 'double', 'detail-double-header.html',)

### "rooting" and Absolute template paths

The themes package is designed to focus on one _root_ directory. By default this is `themes` and all templates should exist within this one directory:

_settings.py_

```py
THEMES_OPTIONS = {
    "root": 'themes',
}

THEMES_MAP = {
    'detail': 'detail.html',
    'list': 'list.html',
    'page': 'page.html',
}
```

directory stucture:

    baseapp/
        templates/
            themes/
                detail.html
                list.html
                page.html
                ...
        models.py
        views.py
        ...
    other/
        models.py
        ...
        templates/
            themes/
                detail.html

As the `other` app is installed _after_ `baseapp`, the `other/templates/themes/detail.html` overrides `baseapp`.  However we can change this within the themes setup, to target any app.

#### Absolute Root

Apply a forward-slash `/` at the start of the filename - infering an "absolute" template name, and ignore the `root` directory name:

_settings.py_

```py
THEMES_OPTIONS = { "root": 'beta', }
```

Here the entry for `{% theme "egg" %}` will resolve an absolute template path:

_themes.py_

```py
from trim.theming import install, name_default_redirect

SITE_THEMES = {
    'detail': 'new-detail.html',   # */templates/beta/new-detail.html
    'list':   'new-list.html'  ,   # */templates/beta/new-list.html

    'egg': '/foo/name.html',       # */templates/foo/name.html
}

SCOPE = install(SITE_THEMES)
```
