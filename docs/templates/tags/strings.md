# Strings

The `strings` template tag provides a few functions for working with text strings within the template directly.

+ [str_merge](#str_merge)

## Usage

Within your template use the load `{% load strings %}` command

```jinja
{% load strings %}
{% str_merge "road" "house" "!" %} <!-- roadhouse! -->
```

# `str_merge`

Merge many strings into a single string and use as a variable:

Our example context data:

```py
from trim import views


class ExampleFileView(views.TemplateView):
    template_name = 'example/template.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, part_name="foo-example")
```

Within our template `example/template.html`:

```jinja
{% str_merge "./imports/" part_name ".html" as include_name %}
{% include include_name %}

{% str_merge "../theatre/" part_name ".js" as script_name %}
<script src={{script_name}}></script>
```
