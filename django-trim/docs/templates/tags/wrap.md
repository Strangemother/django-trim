# `wrap` Tag

The `{% wrap %}` template tag allows you to wrap some content with another common template:

```jin
{% load trim %}

{% wrap "fragments/other.html" with custom="attributes" %}
    ...
{% endwrap %}
```

## Usage

The `wrap` tag accepts _with_ statement keyword arguments.

```jinja2
{% load trim %}

{% quickform "products:stock-notify-form" as stock_form %}
{% wrap "fragments/form.html" with form=stock_form %}{% endwrap %}
```

You can test for empty content using standard template tags.

```jinja2
<ul class="crud-form {% if wrap.content %}has-wrap-content{% else %}no-wrap-content{% endif %}">
    {% if wrap.content %}
        {{ wrap.content }}
    {% else %}
        {{ form.as_ul }}
    {% endif %}
</ul>
```

## Example

For this example the `wrap_form.html` accepts some some HTML in place of a _form_:

```jinja2
{% wrap "stocks/wrap_form.html" with button_text="Next"  action="/foo/bar" %}
    <ul>
    {% for row in form %}
        <li>{{ row }}</li>
    {% endfor %}
    </ul>
{% endwrap %}
```

The template `stocks/wrap_forms.html` should refer to the `wrap.content` and any other variables from the `with` or parent contexts.

```jinja2
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
