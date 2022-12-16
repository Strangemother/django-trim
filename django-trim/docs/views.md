# Views

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
