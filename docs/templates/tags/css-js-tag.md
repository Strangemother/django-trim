# CSS / JS Tags

Generate a standard include of CSS and JavaScript files to a view with `{% css ... %}` and  `{% js ... %}`

## Usage

Basic usage is quick:

```jinja2
{% load link %}
{% css "forms/admin.css" %}
{% js "vendors/foo.min.js" %}

{% link.css "forms/admin.css" %}
{% link.js "vendors/foo.min.js" %}
```

## link.js

Insert a standard `<script type="text/javascript" src="..."></script>` tag into your HTML. The link given is the `static` url of your target file.

```jinja2
{% load link %}
{% link.js "js/myapp/myfile.js" %}
```

```jinja2
# Becomes
<script type="text/javascript" src="/static/js/myapp/myfile.js"></script>
```

This is identical to the standard method, but saves a memory cells:

```jinja2
# AKA {% link.js "js/myapp/myfile.js" %}

{% load static %}
<script type="text/javascript" src="{% static "js/myapp/myfile.js" %}"></script>
```

## link.css

Insert a standard `<link href="..."></link>` tag into your HTML. The link given is the `static` url of your target file.

```jinja2
{% load link %}
{% link.css "css/myapp/myfile.css" %}
```

```jinja2
# Becomes
<link type="text/javalink" href="/static/css/myapp/myfile.css"></link>
```

This is identical to the standard method, but saves a memory cells:

```jinja2
# AKA {% link.css "css/myapp/myfile.css" %}

{% load static %}
<link type="text/javalink" href="{% static "css/myapp/myfile.css" %}"></link>
```
