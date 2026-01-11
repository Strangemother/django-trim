# Links

The `{% link %}` tag generates anchor elements with automatic URL resolution.

Provide a named URL pattern and optional parameters, and it will create a complete `<a>` tag.

```jinja2
{% load link %}

{% link "blog:post-detail" post.slug "Contact Us" class='large-btn' %}

<!-- Renders to: -->
<a href="/blog/posts/my-first-post/" class="large-btn">Contact Us</a>
```

## Syntax

```jinja2
{% link "url_name" [arg1] [arg2] ... [text] [attr1=value1] [attr2=value2] ... %}
```

## Contents

- [Usage](#usage)
- [URL Arguments](#url-arguments)
- [Link Text](#link-text)
- [HTML Attributes](#html-attributes)
- [Examples](#examples)

> [!TIP]
> Checkout [css js tag](css-js-tag.md) links for `{% link.js %}` and `{% link.css %}` tags

## Usage

Load the tag in your template:

```jinja2
{% load link %}
```

Simple link without parameters:

```jinja2
{% link "home" %}

Output:

<a href="/">home</a>
```

Link with custom text:

```jinja2
{% link "about" "About Us" %}

Output:

<a href="/about/">About Us</a>
```

## URL Arguments

Pass URL parameters the same way as the `{% url %}` tag:

```jinja2
{% link "blog:post-detail" post.pk %}
```

Multiple parameters:

```jinja2
{% link "shop:product" category.slug product.slug %}
```

The last string argument is used as the link text:

```jinja2
{% link "blog:post-detail" post.pk "Read Article" %}
```

Output:
```html
<a href="/blog/posts/42/">Read Article</a>
```

## Link Text

If no text argument is provided, the last URL parameter is used as the display text:

```jinja2
{% link "user:profile" user.username %}
```

Output:
```html
<a href="/users/john_doe/">john_doe</a>
```

### Using Model Objects

Pass a model instance as the last argument to use its `__str__` representation:

```python
class Product(models.Model):
    name = fields.chars(150)
    price = fields.decimal(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
```

```jinja2
{% link "shop:product" product.id product %}
```

Output:
```html
<a href="/shop/products/42/">Wireless Mouse - $29.99</a>
```

## Styling with Attributes

Add any HTML attributes directly to the tag—no special syntax required. This is perfect for CSS frameworks, JavaScript bindings, or accessibility features.

### CSS Classes

```jinja2
{% link "blog:create" "New Post" class="btn btn-primary" %}
<!-- Output: <a href="/blog/posts/new/" class="btn btn-primary">New Post</a> -->

{% link "user:logout" "Sign Out" class="nav-link text-danger" %}
<!-- Output: <a href="/accounts/logout/" class="nav-link text-danger">Sign Out</a> -->
```

### Target and Relationship Attributes

```jinja2
{% link "help:documentation" "Docs" target="_blank" rel="noopener" %}
<!-HTML Attributes

Add any HTML attributes directly to the tag. No special syntax required.

### CSS Classes

```jinja2
{% link "blog:create" "New Post" class="btn btn-primary" %}
```

Output:
```html
<a href="/blog/posts/new/" class="btn btn-primary">New Post</a>
```

### Common Attributes

```jinja2
{% link "help:docs" "Documentation" target="_blank" rel="noopener" %}
```

```jinja2
{% link "shop:cart" "Add to Cart" 
   class="btn"
   data-product-id=product.id
   aria-label="Add to cart" %}
```

Output:
```html
<a href="/help/docs/" target="_blank" rel="noopener">Documentation</a>
```

```html
<a href="/shop/cart/" 
   class="btn"
   data-product-id="42"
   aria-label="Add to cart">Add to Cart</a{% endif %}
</nav>
```

### Data Table with Actions
Examples

### Navigation Menu

```jinja2
<nav>
  {% link "home" "Home" class="nav-item" %}
  {% link "blog:list" "Blog" class="nav-item" %}
  
  {% if user.is_authenticated %}
    {% link "user:profile" user.username "My Account" class="nav-item" %}
    {% link "user:logout" "Logout" class="nav-item" %}
  {% endif %}
</nav>
```

### Data Table

```jinja2
<table>
  {% for product in products %}
  <tr>
    <td>{% link "shop:product" product.id product.name %}</td>
    <td>{% link "shop:edit" product.id "Edit" class="btn-sm" %}</td>
  </tr>
  {% endfor %}
</table>
```

### List Loop

```jinja2
{% for post in posts %}
  {% link "blog:post-detail" post.slug post.title class="post-link" %}
{% endfor %}
```

## Implementation

The `{% link %}` tag uses Django's `reverse()` function for URL resolution and renders through the `trim/link.html` template. This provides full compatibility with Django's URL system and allows customization by overriding the template