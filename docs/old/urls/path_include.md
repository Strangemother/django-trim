# Path Include

Perform a standard `include` with less lines:

before:

```py
from products.views import IndexView
from django.urls import path, include

urlpatterns += [
    path("", IndexView.as_view()),
    path("account/", include('account.urls')),
    path("products/", include('products.urls')),
    path("baskets/", include('baskets.urls')),
    ]
```

after:

```py
from products.views import IndexView

from django.urls import path #, include
from short.urls import path_includes

urlpatterns += [
    path("", IndexView.as_view()),
] + path_includes(
      'account',
      'products',
      'baskets',
    )
```

Use the _single caller_ variant:

before:

```py
from products.views import IndexView
from django.urls import path, include

urlpatterns += [
    path("", IndexView.as_view()),
    path("account/", include('account.urls')),
    path("products/", include('products.urls')),
    path("baskets/", include('baskets.urls')),
    ]
```

after:

```py
from products.views import IndexView

from django.urls import path #, include
from short.urls import path_include

urlpatterns += [
    path("", IndexView.as_view()),
] + path_include('account/')
  + path_include('products/')
  + path_include('baskets/')
```
