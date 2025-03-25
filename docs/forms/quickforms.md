# Quick Forms

Plug your existing `FormView` form into any page. The form submission is sent to the correct page.

_Template examples:_

```jinja
{% load quickforms %}

<!-- Acts like a `form` -->
<form action='/myform/'>{% quickform "app:formview-name" %}</form>

<!-- Put a prepared form in the view -->
{% quickform.form "app:formview-name" %}

<!-- Put a prepared form in the view - from a form object -->
{% quickform.form form %}
```


**Where is the _form_?**

That's the clever part. The _form_ is your standard (already wired) `FormView`, with a name: `"app:formview-name"` and a url `/myform/`.

The `{% quickform %}` uses the formclass within the working view.

## Why

_Quick Forms_ offers a seamless approach to embedding **prepared forms on any page** by leveraging existing views and URLs. For more in-depth information, see the [templatetags/quickforms documentation](../templates/tags/quickforms.md).

**Assumptions:**

1. **Safer**: Post to an form page, using the validation and a success page within.
2. **Easier**: Reuse the same form across multiple pages without view context alterations
3. **Faster**: Immediately put any form on any page

**Examples**

+ **Contact Forms**: Create a single "Contact" `FormView` page with its own validation, processing (perhaps firing emails), Then flourish every page on your entire website, using the same contact form and validation.
+ **Vote Forms (same form pre-populated)**: Reuse the same form without submission woes. Apply init data in the tag for multiple forms on a page.
+ **Clever switchy**: Include your chosen form with a string, for switching of forms without the overhead.


## Getting Started

_Quick forms_ utilizes your existing Django FormViews to display a form on any chosen page. The `{% quickform app:viewname %}` tag retrieves and uses the form from the specified view. When the form is submitted, the data is posted directly to that view.

1. Build a standard `FormView`. e.g: view `contact:contact-us-form`
2. Use the form on another page. e.g `{% quickform.form "contact:contact-us-form" %}`

> This feature enables you to construct a standard form-view incorporating your business logic and deploy it anywhere in your application, bypassing the usual complexities associated with integrating forms in multiple places.

Quick Forms provide two distinct methods for ease of use:

+ The standard method `{% quickform %}`, which returns the actual Form instance.
+ The instant form method `{% quickform.form %}`, which generates a complete HTML form ready for use.

Below is an example of how to use quick-forms in your templates:

```jinja
{% load quickforms %}

<!-- Using the standard method -->
<form>
    {% quickform "app:formview-name" %}
</form>

<!-- Using the instant form method -->
{% quickform.form "app:formview-name" %}
```

## Example Usage

The `{% quickform "app:formview-name" %}` utilised an `FormView`. The `quickform` templatetag extracts the `form_class` and produces a finished form.

### Setup

The view, form, and URL (for the target formview) are not special. For the example you should already have:

1. A FormView
2. A URL to the FormView

Or to clarify you have a ready-to-go standard form of some type. For this example we create a basic `product_seach:searchform` on the POST URL `/search/`:

_views.py_
```py
from trim import views
from . import forms


class SearchFormView(views.FormView):
    form_class = forms.SearchForm
    template_name = 'product_search/form.html'

    def form_valid(self, form):
        # complex form handling ...
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

Here we use trim urls - exposing the url `/search/` and our name `product_seach:searchform`

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

### Implement

Now the interesting part: `{% quickform %}`. To target the above we access the url `product_search:searchform` of which will return a prepared `forms.SearchForm`:

```jinja
{% load quickforms %}

<div class=myform>
    {% quickform.form "product_search:searchform" %}
</div>
```

The result on our page includes a action url with a correct target, inside a finished form.

```jinja
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

Notice the `action` and `csrftoken` are prepared.

### Form URL Arguments

The target form page (such as `/product/search/`) may required path arguments in the url:

    # params:  "product_search:searchform" [shop slug] [subtype slug]
    # pattern: "product_search:searchform" "<str:shop_slug>/<str:subtype_slug>/"
    # url:     /product/search/tillys-bakery/muffins

```jinja
<!-- Arguments apply to the form endpoint -->
{% quickform.form "product_search:searchform" shop.slug "muffins" %}
```

```jinja
<form method="post" action="/product/search/tillys-bakery/muffins"> ... </form>
```

### Initial data

Prepoluate a form with keyword parameters, matching the field names within the form


```jinja
{% load quickforms %}

<div class=myform>
    {% quickform.form "product_search:searchform" query='four weddings' %}
</div>
```
