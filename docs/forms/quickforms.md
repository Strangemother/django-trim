# Quick Forms

> Implement a prepared form on any page using the existing view and URLS. [read more in templatetags/quickforms](./templates/tags/quickforms.md)


_Quick forms_ utilise the your existing django FormView to present a form on a chosen page.
The `{% quickform app:viewname %}` tag uses the _form_ from the target view, and upon submission, the result is posted to the view.

This allows you to create a standard form-view (with your business logic) and use it _anywhere_ without the integration issues complex form integration.

_Quick Forms_ offers a seamless approach to embedding prepared forms on any page by leveraging existing views and URLs. For more in-depth information, see the [templatetags/quickforms documentation](./templates/tags/quickforms.md).

_Quick forms_ smartly utilize your existing Django FormView to display a form on any chosen page. The `{% quickform app:viewname %} ` tag **retrieves and uses the form from the specified view**. When the form is submitted, the data is posted directly to that view.

> This feature enables you to construct a standard form-view incorporating your business logic and deploy it anywhere in your application, bypassing the usual complexities associated with integrating forms in multiple places.

Quick Forms provide two distinct methods for ease of use:

+ The standard method, which returns the actual Form instance.
+ The instant form method, which generates a complete HTML form ready for use.


Below is an example of how to use Quick Forms in your templates:


```jinja
{% load quickforms %}

<!-- Using the standard method -->
<form>
    {% quickform "app:formview-name" %}
</form>

<!-- Using the instant form method -->
{% quickform.form "app:formview-name" %}
```

## Demo

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
