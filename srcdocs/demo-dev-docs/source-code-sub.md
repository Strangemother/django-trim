### Source Code

Put your file somewhere (e.g. `./examples/foo.py`), and add a `{% verbatim %}{% sourcecode %}{% endverbatim %}` tag within the markdown file:
{% verbatim %}```jinja2
{% sourcecode "./examples/foo.py" title='without leaf function' %}
```{% endverbatim %}

Result:

{% sourcecode "./examples/foo.py" title='without leaf function' %}