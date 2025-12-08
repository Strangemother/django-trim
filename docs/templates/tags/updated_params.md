# `{% updated_params %}` Template Tag

Update URL query parameters while preserving existing ones from the current request.

## Overview

The `updated_params` tag is useful for building pagination, filtering, and sorting links that preserve the current query string parameters while updating specific ones. This is particularly helpful in list views where you want to maintain filter selections across page changes or vice versa.

## Usage

```django
{% load updated_params %}

<!-- Basic usage: update or add a parameter -->
<a href="?{% updated_params page=2 %}">Next Page</a>

<!-- Update multiple parameters -->
<a href="?{% updated_params page=3 sort='name' %}">Page 3 sorted by name</a>

<!-- Preserve existing filters while changing page -->
<a href="?{% updated_params page=object_list.next_page_number %}">Next</a>
```

## How It Works

The tag:
1. Copies all current GET parameters from `request.GET`
2. Updates them with the new parameters you provide
3. Returns a URL-encoded query string

This means existing parameters are preserved unless explicitly overridden.

## Examples

### Pagination with Filters

```django
{% load updated_params %}

<!-- Current URL: /products/?category=electronics&brand=sony&page=1 -->

<!-- Next page link preserves category and brand -->
<a href="?{% updated_params page=2 %}">
    Next Page
</a>
<!-- Results in: /products/?category=electronics&brand=sony&page=2 -->
```

### Sorting with Pagination

```django
{% load updated_params %}

<!-- Current URL: /products/?page=3&category=books -->

<!-- Change sort, keep page and category -->
<a href="?{% updated_params sort='price' order='asc' %}">
    Sort by Price
</a>
<!-- Results in: /products/?page=3&category=books&sort=price&order=asc -->
```

### Filter Links

```django
{% load updated_params %}

<div class="filters">
    <h3>Category:</h3>
    <a href="?{% updated_params category='electronics' page=1 %}">Electronics</a>
    <a href="?{% updated_params category='books' page=1 %}">Books</a>
    <a href="?{% updated_params category='clothing' page=1 %}">Clothing</a>
</div>
```

### Complete Pagination Example

```django
{% load updated_params %}

<div class="pagination">
    {% if page_obj.has_previous %}
        <a href="?{% updated_params page=1 %}">&laquo; First</a>
        <a href="?{% updated_params page=page_obj.previous_page_number %}">Previous</a>
    {% endif %}
    
    <span class="current">
        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
    </span>
    
    {% if page_obj.has_next %}
        <a href="?{% updated_params page=page_obj.next_page_number %}">Next</a>
        <a href="?{% updated_params page=page_obj.paginator.num_pages %}">Last &raquo;</a>
    {% endif %}
</div>
```

## Reference Implementation

Source: [Credit to O. Valerio](https://blog.ovalerio.net/archives/1512)

The tag is defined in `trim.templatetags.updated_params`:

```python
@register.simple_tag(takes_context=True)
def updated_params(context, **kwargs):
    """Update URL query parameters while preserving existing ones.
    
    Copies all GET parameters from the current request and updates them
    with the provided keyword arguments, returning a URL-encoded query string.
    
    Args:
        context: Django template context (automatically provided)
        **kwargs: Query parameters to add or update
    
    Returns:
        str: URL-encoded query string
    
    Example:
        {% load updated_params %}
        <a href="?{% updated_params page=2 sort='name' %}">Next</a>
    """
    res = context['request'].GET.copy()
    res.update(kwargs)
    return res.urlencode()
```

## Benefits

- **Preserves Context**: Keeps existing query parameters intact
- **Clean URLs**: Automatically URL-encodes the output
- **Flexible**: Works with any number of parameters
- **Simple**: No need to manually track and pass all parameters

## Common Use Cases

1. **Pagination** - Change page while keeping filters
2. **Sorting** - Change sort order while keeping search and filters
3. **Filtering** - Add/change filters while keeping pagination
4. **Search** - Update search terms while preserving other parameters

## Related

- [`{% link %}` tag](./link/readme.md) - Generate links from Django view names
- [ListView documentation](../../views/list-views.md) - List views with pagination
