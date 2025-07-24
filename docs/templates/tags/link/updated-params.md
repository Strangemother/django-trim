# `updated_params` Tag

> [!TIP]
> I (the developer) didn't create this myself. I read this blog by Gonçalo Valério: https://blog.ovalerio.net/archives/1512

Updated Params grabs the `GET` Parameters from a URL, and updates the _dictionary_ of params to include your additional parameters.

```jinja
{% load updated_params %}
{% updated_params page=2 something='else' %}
```

It's useful when you need to preserve GET request params through requests, but also apply a change:

    https://example.ovalerio.net?{% updated_params page=2 something='else' %}


## Example

A quick example of the _next page_ pagination link, preserving existing GET params through the request:

```jinja
{% load updated_params %}
{% if page_obj.has_next %}
    <a href="?{% updated_params page=page_obj.next_page_number %}">next</a>
    <a href="?{% updated_params page=page_obj.paginator.num_pages %}">last &raquo;</a>
{% endif %}
```