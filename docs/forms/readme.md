# Forms

> Reduce typing on forms! Use the `fields` to quickly flesh out your form fields.

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

## Quick Forms

> Implement a prepared form on any page using the existing view and URLS. [read more in templatetags/quickforms](./templates/tags/quickforms.md)

Two quickform methods exist for your choosing. The _standard_ method return the real Form instance, the _instant form_ creates a finished HTML form.

```html
{% load quickforms %}

<form>
{% quickform "app:formview-name" %}
</form>

{% quickform.form "app:formview-name" %}
```

### Demo

You should have a _view_ and it should be ready for a standard `FormView`. The `quickform` templatetag extracts the `form_class` and produces a finished form.

The view and URL for the target form isn't special. Here we can use trim parts to cutdown on boilerplate

_views.py_
```py
from trim import views
from . import forms


class SearchFormView(views.FormView):
    form_class = forms.SearchForm
    template_name = 'product_search/form.html'
    ...
```

_forms.py_
```py
from django import forms
from trim.forms import fields
from . import models


class SearchForm(forms.Form):
    # basket_id = forms.CharField()
    query = fields.chars(max_length=255)

    class Meta:
        fields = ('query',)
```

_urls.py_
```py
from trim import urls as turls
from . import views

app_name = 'product_search'

urlpatterns = turls.paths_dict(views, dict(
        SearchFormView=('searchform', ''),
    )
)
```

This isn't new and the interesting part is the `{% quickform %}`.

To target the above we access the url `product_search:searchform`, of which will return a prepared `forms.SearchForm`:

_other_view.py_
```jinja2
{% load quickforms %}
<div class=myform>
{% quickform.form "product_search:searchform" %}
</div>
```

This produces a ready form:

```html
<div class=myform>
    <form method="post" action="/product_search/" data="">
        <ul>
            <li>
                <label for="id_query">Query:</label>
                <input type="text" name="query" maxlength="255" required="" id="id_query">
            </li>
        </ul>
        <input type="hidden" name="csrfmiddlewaretoken" value="8GVupx...tjwkcxD">
        <button type="submit">Submit</button>
    </form>
</div>
```
