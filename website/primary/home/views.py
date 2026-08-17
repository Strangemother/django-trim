from trim.views import TemplateView


class HomeView(TemplateView):
    """Render the Django Trim homepage."""

    template_name = "home/home.html"


class ExampleSubView(TemplateView):
    """Render the model fields component guide."""

    template_name = "home/sub-view.html"


class FieldsApiView(TemplateView):
    """Render the functional fields API reference."""

    template_name = "home/fields-api.html"