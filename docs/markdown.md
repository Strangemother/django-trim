# Markdown

Django Trim offers a few tools to help with Markdown rendering

+ [Template Response](#template-response): Return a django templated markdown formatted response from your view, rendered as finished HTML
+ [Template Tags](#template-tags): Use Markdown directly within a HTML template
  +  [`markdown`](#markdown)
  +  [`markdown.file`](#markdown-file)

## Example

A Markdown View:

```py
from trim import views
from trim.markdown.response import MarkdownTemplateResponse

class MarkdownReponseMixin(views.TemplateView):
    response_class = MarkdownTemplateResponse
    template_name = "contact/index.md"
```

Collect a markdown file:

```jinja
{% load markdown %}

<div>
    {% markdown.file "readme.md" %}
</div>
```


Use Markdown within the view:

```jinja
{% load markdown %}

<div>
    {% markdown %}
    # Markdown Block.

    Write markdown content within the template directly.
    {% endmarkdown %}
</div>
```

## Usage

### Template Response

Expecting a .md template file - perform standard rendering, coverting to HTML and return the finished page.


```py
from trim import views
from trim.markdown.response import MarkdownTemplateResponse

class MarkdownReponseMixin(views.TemplateView):
    response_class = MarkdownTemplateResponse
    template_name = "contact/index.md"
```


### Template Tags

To use tags within the template, ensure to load `markdown`:

```jinja
{% load markdown %}
```

This import provides a few markdown template tags.


#### `markdown`

Populate a template `markdown` node with content to render as markdown:

```jinja
{% load markdown %}
<body>
    <div>
        {% markdown %}
        # Markdown Block.

        Write markdown content within the template directly, rendered with the same server tools:

        + Intendation check
        + generic markdown renderer

        ... And other stuff.
        {% endmarkdown %}
    </div>
</body>
```

Indentation is de-indented when parsed.


#### `markdown.file`

It's pretty common to have a markdown _file_ - such as a `docs/readme.md`.


```jinja
{% load markdown %}

<h1>Readme</h1>
<div class="readme">
    {% markdown.file "docs" "readme.md" %}
</div>
```

This is designed to be flexible but slightly more secure than exposing full-paths. The tag accepts _two_ arguments `{% markdown.file target_directory relative_filepath %}`.

##### Setup

The target directories are stored within your settings file. Create an dictionary named `TRIM_MARKDOWN_DIRS` and apply applicable paths:

_settings/base.py_
```py
# The root directory containing the site, relative to the README.md
SITE_DIR = (Path(__file__).parent / '../').resolve().absolute()

# ...
DEMO_DIR = SITE_DIR / 'site_demos'
DOCS_DIR = SITE_DIR / 'docs'
EXAMPLES_DIR = SITE_DIR / 'examples'

# a pack of locations we can use for {% markdown.file filepath %}
TRIM_MARKDOWN_DIRS = {
    'site_demos': DEMO_DIR,
    'docs': DOCS_DIR,
    'examples': EXAMPLES_DIR,
}
```

##### Apply

The keys applied within the `TRIM_MARKDOWN_DIRS` dictionary may be referenced within the tag:

```jinja
{% load markdown %}

<div class="first">
    {% markdown.file "docs" "readme.md" %}
</div>

<div class="second">
    {% markdown.file "examples" "readme.md" %}
</div>
```

If the given file does not exist in target directory (e.g. `readme.md`) - no content is rendered.
