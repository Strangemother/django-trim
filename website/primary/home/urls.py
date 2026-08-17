from trim import urls
from . import views

app_name = 'home'

urlpatterns = urls.paths_named(views,
    home=("HomeView", ""),
    fields=("ExampleSubView", "fields/"),
    fields_api=("FieldsApiView", "fields/api/"),
)
