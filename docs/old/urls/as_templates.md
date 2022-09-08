# short.urls.as_templates

Implement a set of views for a list of templates:

```py
from shorts import urls as shorts

## defaults
urlpatterns = [
    #...
]

## Appending
urlpatterns += shorts.as_templates(
    geoms=('mockup/', 'mockup/crystal-geometries.html'),
    crystal1=('mockup/1/', 'mockup/crystal-1.html'),
    home=('mockup/home/', 'mockup/home.html'),
)
```

In this case each path presents the HTML through the django templating library. This is exactly the same as implementing a `TemplateView` for each view.

