# CSS / JS Tags

The `{% link.css %}` and `{% link.js %}` tags generate HTML elements for including static CSS and JavaScript files.

**Syntax:**
```jinja2
{% link.css "path/to/file.css" %}
{% link.js "path/to/file.js" %}
```

**Example:**
```jinja2
{% link.css "css/myapp/styles.css" %}
{% link.js "js/myapp/script.js" %}
```

**Output:**
```html
<link rel="stylesheet" href="/static/css/myapp/styles.css">
<script type="text/javascript" src="/static/js/myapp/script.js"></script>
```

## Contents

- [Usage](#usage)
- [CSS Files](#css-files)
- [JavaScript Files](#javascript-files)
- [Comparison](#comparison)

## Usage

Load the tag in your template:

```jinja2
{% load link %}
```

Include a CSS file:

```jinja2
{% link.css "css/myapp/styles.css" %}
```

Include a JavaScript file:

```jinja2
{% link.js "js/myapp/script.js" %}
```

## CSS Files

The `{% link.css %}` tag generates a standard stylesheet link element:

```jinja2
{% link.css "css/forms/admin.css" %}
```

Output:
```html
<link rel="stylesheet" href="/static/css/forms/admin.css">
```

## JavaScript Files

The `{% link.js %}` tag generates a standard script element:

```jinja2
{% link.js "js/vendors/library.min.js" %}
```

Output:
```html
<script type="text/javascript" src="/static/js/vendors/library.min.js"></script>
```

## Comparison

These tags simplify the standard Django static file inclusion pattern:

**Traditional Django:**
```jinja2
{% load static %}
<link rel="stylesheet" href="{% static 'css/myapp/styles.css' %}">
<script type="text/javascript" src="{% static 'js/myapp/script.js' %}"></script>
```

**With Trim:**
```jinja2
{% load link %}
{% link.css "css/myapp/styles.css" %}
{% link.js "js/myapp/script.js" %}
```

Both tags use Django's `static` template tag internally, ensuring compatibility with your `STATIC_URL` configuration.
