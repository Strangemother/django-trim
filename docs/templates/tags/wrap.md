# `wrap` Tag

The `{% wrap %}` template tag allows you to wrap some content with another common template:

```html
{% load trim %}

{% wrap "fragments/other.html" with custom="attributes" %}
    ...
{% endwrap %}
```

## Example

For this example the `wrap_form.html` accepts some some HTML in place of a _form_:

```html
{% wrap "stocks/wrap_form.html" with button_text="Next"  action="/foo/bar" %}
    <ul>
    {% for row in form %}
        <li>{{ row }}</li>
    {% endfor %}
    </ul>
{% endwrap %}
```

The template `stocks/wrap_forms.html` should refer to the `wrap.content` and any other variables from the `with` or parent contexts.

```
<form method="post"
  enctype="multipart/form-data"
  {% if action %}action="{{action}}"{% endif %}>

    {{ wrap.content }}
    <input class='btn'
        type="submit"
        value="{% firstof button_text 'Confirm' %}">
    {% csrf_token %}
</form>
```

It's similar to an `include` tag with some extra body.
