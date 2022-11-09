# Building a ListView

`trim` helps apply the django builtin `ListView` with less words. First and foremost we need a list view:


## The View

_views.py_

```py
from trim import views
from . import models

class MyModelListView(views.ListView, views.Permissioned):
    model = models.MyModel
    permission_required = ( 'stocks.view_stockingmethod')
```

## Template

If you're working with the theming library, the view is fairly quick:

_templates/app/mymodel_list.html_

```html
{% theme "list" %}
{% block title %}My Model List{% endblock %}
```

The "list" page has a special property, to assign a hyper link for each detail object:

```py
# Extended from above.
class MyModelListView(views.ListView, views.Permissioned):
    ...
    list_item_link = 'stocks:stockingmethod-detail'
```

## URL

We apply a URL in `urls.py`:

```py
from trim import urls as trims

from . import views

app_name = 'stocks'

urlpatterns = trims.paths_dict(views, dict(
        ...
        MyModelListView=('mymodel-list', 'items/'),
    )
)
```

---

That's done. A clean and secure `mymodel` list, implemented in like 10 lines of code.
