# `wrap` Tag

The `{% wrap %}` template tag allows you to wrap some content with another common template. Check out [slots](./wrap-slots.md) for defined placeholders.


<table>
<thead><tr>
  <th align="left">Implement</th>
  <th align="left">Template</th>
</tr></thead>
<tbody>
<tr valign="top">
<td>

At the place of include use the `{% wrap %}{% endslot %}` tag to _use_ the wrap template `homepage.html`

```jinja
{% load wrap %}

{% wrap "fragments/other.html" %}
    My View content
{% endwrap %}
```

</td>
<td>

Create a _wrap template_ with any HTML, and apply the `{{ wrap.content }}` in the best place for content injection `fragments/other.html`:

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
</tr>
<tr>

</tr>
</tbody></table>



# Usage

`{% wrap ... %}` acts very similar to `{% include ... %}` with an additional `wrap` context.

```jinja
{% load wrap %}

{% wrap "fragments/other.html" with custom="attributes" %}
    ...
{% endwrap %}
```

We can apply any content within a slot, such as conditions and other include statement. The HTML is rendered within the context of the parent (before it's inserted into the wrap template), therefore we consider `wrap.content` as the "finished" result.


---

Create a fragment of which utilises the `{{ wrap.content }}`:

```jinja2
<!-- fragments/other.html -->
<div class="complex-content">
    <div class='text-content'>
        {{ wrap.content }}
    </div>
    <!-- Some very complex HTML -->
    <div class='right-content'></div>
</div>
```

We can use it within another template, adding some content to the wrap:

```jinja2
<!-- homepage.html -->
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
