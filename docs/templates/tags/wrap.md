# `wrap` Tag

The `{% wrap %}` template tag allows you to wrap some content with another common template. Check out [slots](./wrap-slots.md) for defined placeholders.


<table>
<thead><tr>
  <th align="left">

  Template `fragments/other.html`

  </th>
  <th align="left">

  Usage `homepage.html`

  </th>
</tr></thead>
<tbody>
<tr valign="top">
<td>

```jinja2
<div class="complex-content">
    <div class='text-content'>
        {{ wrap.content }}
    </div>
    <!-- Some very complex HTML -->
    <div class='right-content'></div>
</div>
```

</td>
<td>


```jinja
{% load wrap %}

{% wrap "fragments/other.html" with custom="attributes" %}
    My View content
{% endwrap %}
```

</td>
</tr>
<tr>
<td colspan="2">

```jinja2
<div class="complex-content">
    <div class='text-content'>
        My View content
    </div>
    <!-- Some very complex HTML -->
    <div class='right-content'></div>
</div>
```

</td>
</tr>
</tbody></table>

---

```jinja
{% load wrap %}

{% wrap "fragments/other.html" with custom="attributes" %}
    ...
{% endwrap %}
```

> `{% wrap ... %}` acts very similar to `{% include ... %}` with an additional `wrap` context.

## Usage

Create a fragment of which utilises the `{{ wrap.content }}`:

_fragments/other.html_
```jinja2
<div class="complex-content">
    <div class='text-content'>
        {{ wrap.content }}
    </div>
    <!-- Some very complex HTML -->
    <div class='right-content'></div>
</div>
```

We can can use it within another template, adding some content to the wrap:

_homepage.html_
```jinja2
{% load wrap %}

{% wrap "fragments/other.html" %}
    <h1>Welcome</h1>
    <p>The quick brown fox has complex content.</p>
{% endwrap %}
```

## Complex Content

The content within the `wrap` is _rendered inline_ using the _current_ context. The variable available in the fragment `wrap.content` is considered "rendered" when used.


```jinja2
{% load wrap %}

{% wrap "fragments/other.html" %}
    <!-- Content can be complex -->
    {% include "homepage/intro-text.html" %}
{% endwrap %}
```


## Attributes and Conditionals

The `wrap` tag accepts _with_ statement keyword arguments.

```jinja2
{% load wrap %}

<!-- make a complex thing. -->
{% quickform "products:stock-notify-form" as stock_form %}

<!-- provide as an argument -->
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

# Example

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
