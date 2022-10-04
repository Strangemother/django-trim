# URLs

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

