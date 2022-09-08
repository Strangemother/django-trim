# Django Trim

> Django Trim shortcuts all the boilerplate for some of those daily django parts. Reduce the amount of written text and trim your code for easier reading, faster prototyping, and less typing.

Django Trim reduces the amount of text, imports and general congantive overload of microtasks when plugging together a django app in it's initial stages.

+ Less typed text, same functionality
+ clear, predicable functional naming
+ Leverage conventions for faster prototyping
+ 100% compatible with existing django components.

## Trim Examples

Some quick examples to quickly trim your code.

### Models

Reduce typing on models! Import ready-to-use fields for your models. All
fields shadow the existing django field:

_models.py_
```py
from django.db import models
from trim.models import fields

class ContactMessage(models.Model):
    user = fields.user_fk(nil=True)
    sender = fields.email(nil=True)
    cc_myself = fields.bool_false()
    subject = fields.chars(max_length=255, nil=True)
    message = fields.text(nil=False)
    created, updated = fields.dt_cu_pair()
```

### Forms

Reduce typing on forms! Use the fields to quickly flesh out your form fields.
All django fields are interchangable. Some are convenience tools such as the `trim.forms.fields.text()` TextArea input field:

_forms.py_
```py
from django import forms
from trim.forms import fields

class ContactForm(forms.Form):
    sender = fields.email(required=False) # EmailField
    cc_myself = fields.bool_false() # A boolean field if `False` prepared
    subject = fields.chars(max_length=255, required=False) # CharField
    message = fields.text(required=True) # A ready-to-go CharField with a TextArea widget
```


Drop in a few shortcuts to quickly infer (and plug-in) required parts for your apps. For example, we can generate a `CreateView`, `UpdateView`, `ListView` and `DeleteView` for all our models, with one line:


### Views

Reduce Typing on views is more interesting. Generate a _Create_, _Read_, _Update_, _Delete_ set of views for a model:

_views.py_
```py
from django.shortcuts import render

from trim import views
from . import models, forms

views.crud(models.ContactMessage)

# or DANGEROUSLY do **all** discovered models.
views.crud_classes()
```

This writes the views as you would by hand, allowing real inheritence and imports. The `views.crud` produces five Class Based Views. Looking something similar to this:

_views.py (meta class result)_
```py
from trim import views
from . import models

class ContactMessageListView(views.ListView):
    model = models.ContactMessage


class ContactMessageCreateView(views.CreateView):
    model = models.ContactMessage
    fields = '__all__'


class ContactMessageUpdateView(views.UpdateView):
    model = models.ContactMessage
    fields = '__all__'


class ContactMessageDeleteView(views.DeleteView):
    model = models.ContactMessage
    success_url = reverse_lazy('products:list')


class ContactMessageDetailView(views.DetailView):
    model = models.ContactMessage
```

The same appled for other view-packs; such as `history`.

> There is no magic. Django Trim generates **real** class instances using meta classing (It's as if you wrote the code by hand!)

Apply along with your existing views, to mix and match your complexity requirements:

```py
from django.shortcuts import render

from trim import views
from . import models, forms

views.history(models.ContactMessage, __name__, date_field='created')

class ContactFormSuccessView(views.TemplateView):
    template_name = 'contact/success.html'

class ContactMessageListView(views.IsStaffMixin, views.ListView):
    # MUST BE STAFF TO ACCESS
    model = models.ContactMessage

# django trim is aware of already existing classes
# through the naming convention and will omit ContactMessageListView (above)
views.crud(models.ContactMessage)

class ContactMessageDetailView(views.IsStaffMixin, views.DetailView):
    """Override the trim generated detail view to apply an 'IsStaffMixin'
    """
    model = models.ContactMessage

```

### Admin

Instantly and automatically generate admin views for incoming models.

```py
from django.contrib import admin
from trim import admin as t_admin

from . import models

t_admin.register_models(models)
```

Or use the model detection functions to use the standard admin site register function:

_admin.py_
```py
from django.contrib import admin
from trim.models import grab_models
from . import models
# Register all discovered models, ignoring any indirect imports
admin.site.register(grab_models(models, ignore=['User']))
```

### URLs

Help the readability of your `urls.py`:

```py

from trim import t_urls
from trim.models import grab_models

from . import views

app_name = 'contact'

urlpatterns = t_urls.paths_named(views,
    success=('ContactFormSuccessView', 'thanks/',),
    # reference trim generated views.
    sheet=('ContactMessageListView', 'sheet/',),
    detail=('ContactMessageDetailView', 'sheet/<str:pk>/',),
)
```

Perform Full includes through single entries, each expand to the conventional include:

```py
from trim.urls import path_includes as includes

urlpatterns += includes(
        'account', # path('account/', include('accounts'))
        'products',
        'contact',
    )
```

Maybe just a `TemplateView` or four:

_urls.py (extended from above)_
```py
urlpatterns += t_urls.as_templates(
    geoms=('mockup/', 'mockup/crystal-geometries.html'),
    crystal1=('mockup/1/', 'mockup/crystal-1.html'),
    home=('mockup/home/', 'mockup/home.html'),
    v1_article=('mockup/article/', 'mockup/v1-article.html'),
    advert_cell=('advert/1/', 'small_adverts.html')
)

urlpatterns += [
    t_urls.template_view('mockup/2', 'mockup/crystal-geometries.html')
]
```

