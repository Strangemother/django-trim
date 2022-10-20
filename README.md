# Django Trim

Django trim helps boilerplate work for very fast prototyping and dev jumpstarts. With `trim` minimal boilerplate code parts, build conventional urls, views, models without the hassle.

> Use trim for boilerplate, PoC, or just pure laziness, to quickly write common django components.

I am for the Trim philosophy "convenient and thoughtless" - where a function or method should be quick to type, until I'm ready to replace them with the django builtins.

## Setup


Download:

    pip install django-trim


### Install:

Note this Apply the app `trim` to your `INSTALLED_APPS` within your `settings.py`:

    INSTALLED_APPS = [
        # ...
        'trim',
        # ...
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]


You're ready to go.


#### Optional Integration

Later-on you may need to apply an entry to your `context_processors`.

Within the your settings `TEMPLATES` entity, add `trim.context.appname` to the `OPTIONS.context_processors`:

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # ...
                    "trim.context.appname",
                ],
            },
        },
    ]


And that's it.


