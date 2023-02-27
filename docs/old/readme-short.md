# Django Short Shorts

> short shortcuts to standard implementation.

Django Short Shorts reduces the amount of text, imports and general congantive overload of microtasks when plugging together a django app in it's initial stages.

Drop in a few shortcuts to quickly infer (and plug-in) required parts for your apps. For example, we can generate a `CreateView`, `UpdateView`, `ListView` and `DeleteView` for all our models, with one line:

_views.py_:

```py
from short import views as shorts
shorts.crud_classes()
```

## Naming Convention

The library is called `short`, and each module with `short` replicates a standard django setup. For example, an app models: `todo.models` would be `short.models`.

In your module, consider calling the imported `short` unit as `shorts` (plural):

```py
# urls.py
from short import urls as shorts
shorts.paths_dict(...)

# views.py
from short import views as shorts
shorts.crud_classes()

# models.py
from short import models as shorts
shorts.grab_models('todo')
```

Although not the standard pythonic way it highlights the utility _is_ django-short-shorts and not the standard `django` or _your own_ `views`/`models`/etc.

> The purpose of Django Short Shorts is replace it. Eventually you'll implment true code to override the `shorts`, hence **we don't want _your_ `short.shorts` to get in the way of real code...**.

## Where are the `shorts`?

"Django Short Shorts" provides the parent `short` lib. All modules within `short` are have a standard name convention. When implementing the `shorts` (plural), you'll implement a `short` part as your usable module:

```py
from short import views as shorts
```

Hence you have your "short shorts". Notably this naming convention was chosen to ensure the end-user implements `shorts` (plural) - leading to less ambigiation.

## Why.

I write a lot of django code, and I'm constantly implementing the core basics, or applying a _"place holder"_ component until I need a fancy replacement. I've become constantly bored with writing _yet another quick list view_ and considered an application to help me boilerplate my work _as I'm developing_, but implement clear, short, standard methodology until I upgrade to a finished view.
Futhermore the boilerplate tool could infer urls, admin, models etc - plugging the gaps until I implement a long-term replacement.

I originally started an app called 'django boilerplate' (or something similar) to perform this task, however it acted as a transpiler and phyically wrote clean code into the python file. However this quickly became unweildly.

This second version was born from a bunch of tiny shortcuts through many projects; finally solving the issue. As such 99% of the functionality is passive, reading the runtime and producing classes, paths, upon django wakeup and injecting into the module.
