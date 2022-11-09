# Custom 404's

Short shorts provides a quick method to integrate a custom 404 page per view using a mixin. Rather than having a single 404 for the entire website, build unique error pages for each view.

```py
from . import models

from short import views as shorts
from short.views.errors import Custom404

class ProductDetailView(Custom404, shorts.DetailView):
    model = models.Product
```

If a 404 error occurs when accessing this view, the custom 404 replaces the template response.

## Redirect

Alternatively we can request a _redirect_:

```py
# Same imports as the first example

class ProductDetailView(Custom404, shorts.DetailView):
    model = models.Product
    custom_404_redirect_url = 'products:filter'
```

If an 404 occurs the user is redirected with the same arguments given for the view:


```py
# What happends when resolving this URL
#
class Custom404(object):
    def get_custom_404_url(self, request, *args, **kwargs):
        """Return a resolved url. Use all the args and kwargs given to the
        owning view.
        """
        if self.custom_404_redirect_url is None:
            raise Missing404RedirectUrl("custom_404_redirect_url not supplied.")
        return reverse(self.custom_404_redirect_url, args=args, kwargs=kwargs)
```

## Template

Replace the template, returning a custom 404 page:


```py
# Same imports as the first example

class ProductDetailView(Custom404, shorts.DetailView):
    model = models.Product
    custom_404_template_name = 'products/product_detail_404.html'
```
