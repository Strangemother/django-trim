# `quickform` Tag

The `{% quickform "app:view" %}` applies an expected _form_ to the view, given the reversable name or url of an form view.

This allows you to create a standard formview, and address it within another page, utilising the full functionality of the target formview.

## Usage

Want to apply a _form_ to any page - such as a "notify me" form for a product page:

    {% load trim %}

    <form method='post' action='{% url "products:stock-notify-form" %}''>
        {% quickform "products:stock-notify-form" %}
        {% csrf_token %}
    </form>

We can make it cleaner later, but first let's build the flow. First we need a form and form view.

The form is a standard django form (with some `trim` sugar):

_forms.py_

```py
from django import forms
from trim.forms import fields

class StockNotifyForm(forms.Form):
    product_id = fields.hidden(fields.chars)
    email = fields.email()
```

The view is also a standard `FormView`. For convenience we've imported it from `trim.views`:

_view.py_

```py
from trim import views
from product import forms

class StockNotifyFormView(views.FormView):
    form_class = forms.StockNotifyForm
    success_url = reverse_lazy('products:stocknotify-success')
    template_name = 'products/generic-form-page.html'

    def form_valid(self, form):
        """Store a record against the email or user,
        return a response.
        """
        ...
```

As this is a _real view_ with acceptors so we can process the form as we need.

Next, the URL. In this case we're using `trim.urls.paths_dict` for readability:

_urls.py_

```py
from trim import urls as trims, names
from products import views

app_name = 'products'

urlpatterns = [
    ...
]

# Our new addition using the dict format
urlpatterns += shorts.paths_dict(views, dict(
        StockNotifyFormView=('stock-notify-form', 'stock/notify/',),
    )
)
```

### Implement

Phew - we've just built a ready to go form view; how is that useful for `{% quickform %}`?

At this point you can put the `StockNotifyForm` on any other page - using the url pattern as the target:

    {% load trim %}
    <form>
        {% quickform "products:stock-notify-form" %}
        {% csrf_token %}
    </form>


But wait! `quickform` returns an unbound form - allowing the normal djangoy routines...

    {% quickform "products:stock-notify-form" as stock_form %}
    {% include "baskets/sub/site_include.html" with form=stock_form %}


### Initial Data

The tag accepts arbitrary keyword arguments as `form.initial` data:

    {% load trim %}

    {% quickform "products:stock-notify-form" product_id=object.product_id email=user.email as stock_form %}
    {% include "baskets/sub/site_include.html" with form=stock_form %}

This applies the `product_id` and `email` as initial data.

Alternatively you may provide an object as all data through the `initial` keyword argument:

    {% quickform "products:stock-notify-form" initial=object as stock_form %}
    {% include "baskets/sub/site_include.html" with form=stock_form %}


### Action URL

The form will post-back to its own formview, you can capture this as the `form.action_url`:

    {% load trim %}

    {% quickform "products:stock-notify-form" as form %}
    <form method='post' action='{{ form.action_url }}'>
        <ul>
            {{ form.as_ul }}
        </ul>
        {% csrf_token %}
    </form>

You can override the _given_ post url by supplying the `action_url` keyword argument:

    {% quickform "products:stock-notify-form" action_url='/foo/bar/' as form %}

This works nicely with the `initial` keyword argument if you need those words as fields:

    {% quickform "products:stock-notify-form" action_url='/foo/bar/' initial=object as form %}
