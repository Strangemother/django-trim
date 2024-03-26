# CSS / JS Tags

Generate a standard include of CSS and JavaScript files to a view with `{% css ... %}` and  `{% js ... %}`

## Usage

Basic usage is quick:

```jinja2
{% load link %}
{% css "forms/admin.css" %}
{% js "vendors/foo.min.js" %}
```
