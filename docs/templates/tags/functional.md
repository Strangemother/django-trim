# `{% functional %}` Template Tag

Dynamically call any Python function by its fully qualified name directly from your Django templates.

## Overview

The `functional` tag provides a powerful way to execute Python functions from within templates without needing to create custom template tags or filters. It uses `pydoc.locate` to find and execute functions, allowing you to access the full Python standard library and your custom modules.

## ⚠️ Security Warning

**Use with extreme caution in production environments.** This tag can execute arbitrary code and poses significant security risks if the function name comes from untrusted sources. Only use with controlled, whitelisted function names in production.

## Usage

```django
{% load functional %}

<!-- Basic function call -->
{% functional 'module.function_name' arg1 arg2 kwarg1=value1 %}
```

## How It Works

1. Uses `pydoc.locate()` to find the function by its fully qualified name
2. If found and callable, executes it with the provided arguments
3. Returns the result (or empty string if not found)
4. If the object is not callable (e.g., a constant), returns its string representation

## Examples

### Math Operations

```django
{% load functional %}

<!-- Calculate square root -->
{% functional 'math.sqrt' 16 %}
<!-- Output: 4.0 -->

<!-- Calculate power -->
{% functional 'math.pow' 2 10 %}
<!-- Output: 1024.0 -->

<!-- Get mathematical constants -->
{% functional 'math.pi' %}
<!-- Output: 3.141592653589793 -->

<!-- Calculate factorial -->
{% functional 'math.factorial' 5 %}
<!-- Output: 120 -->
```

### String Operations

```django
{% load functional %}

<!-- Convert to uppercase -->
{% functional 'str.upper' 'hello world' %}
<!-- Output: HELLO WORLD -->

<!-- Join strings -->
{% functional 'str.join' ', ' items_list %}
<!-- Output: item1, item2, item3 -->

<!-- String replacement -->
{% functional 'str.replace' 'hello world' 'world' 'Django' %}
<!-- Output: hello Django -->
```

### Date and Time

```django
{% load functional %}

<!-- Get current datetime -->
{% functional 'datetime.datetime.now' %}
<!-- Output: 2025-12-08 10:30:45.123456 -->

<!-- Format date -->
<p>Current time: {% functional 'datetime.datetime.now' %}</p>

<!-- Calculate timedelta -->
{% functional 'datetime.timedelta' days=7 %}
<!-- Output: 7 days, 0:00:00 -->
```

### File Path Operations

```django
{% load functional %}

<!-- Join paths -->
{% functional 'os.path.join' '/home/user' 'documents' 'file.txt' %}
<!-- Output: /home/user/documents/file.txt -->

<!-- Get basename -->
{% functional 'os.path.basename' '/path/to/file.txt' %}
<!-- Output: file.txt -->

<!-- Get file extension -->
{% functional 'os.path.splitext' 'document.pdf' %}
<!-- Output: ('document', '.pdf') -->
```

### Custom Application Functions

```django
{% load functional %}

<!-- Call custom utility functions -->
{% functional 'myapp.utils.format_currency' price currency='USD' %}
<!-- Output: $99.99 -->

{% functional 'myapp.helpers.calculate_discount' item.price discount_percent=15 %}
<!-- Output: 84.99 -->

<!-- Access custom business logic -->
{% functional 'inventory.models.Product.get_stock_level' product.id %}

<!-- Format custom data -->
{% functional 'myapp.formatters.format_phone' user.phone country_code='+1' %}
```

### Random Values (Development/Testing)

```django
{% load functional %}

<!-- Generate random number -->
{% functional 'random.randint' 1 100 %}

<!-- Choose random item -->
{% functional 'random.choice' color_list %}

<!-- Random float -->
{% functional 'random.random' %}
```

### Working with Collections

```django
{% load functional %}

<!-- Get length -->
{% functional 'len' my_list %}

<!-- Get max value -->
{% functional 'max' number_list %}

<!-- Get min value -->
{% functional 'min' number_list %}

<!-- Sum values -->
{% functional 'sum' price_list %}
```

## Accessing Constants and Attributes

The tag can also access module-level constants and attributes:

```django
{% load functional %}

<!-- Mathematical constants -->
π = {% functional 'math.pi' %}
e = {% functional 'math.e' %}
∞ = {% functional 'math.inf' %}

<!-- System information -->
{% functional 'sys.version' %}
{% functional 'sys.platform' %}
```

## Practical Use Cases

### 1. Price Formatting

```django
{% load functional %}

<div class="product">
    <h3>{{ product.name }}</h3>
    <p class="price">
        {% functional 'myapp.utils.format_price' product.price user.currency %}
    </p>
</div>
```

### 2. Complex Calculations

```django
{% load functional %}

<div class="statistics">
    <p>Average: {% functional 'statistics.mean' scores_list %}</p>
    <p>Median: {% functional 'statistics.median' scores_list %}</p>
    <p>Std Dev: {% functional 'statistics.stdev' scores_list %}</p>
</div>
```

### 3. Dynamic URL Building

```django
{% load functional %}

<!-- Join URL parts -->
<a href="{% functional 'urllib.parse.urljoin' base_url path %}">
    Link
</a>
```

### 4. Text Processing

```django
{% load functional %}

<!-- Truncate text -->
{% functional 'textwrap.shorten' long_description width=100 placeholder='...' %}

<!-- Wrap text -->
<pre>{% functional 'textwrap.fill' description width=80 %}</pre>
```

## Return Values

The tag handles different return types:

- **Callable functions**: Returns the function's result
- **Non-callable objects** (constants, variables): Returns string representation
- **Not found**: Returns empty string `''`

## Limitations

1. **Security Risk**: Can execute arbitrary code - use carefully
2. **Template Context**: Does not automatically have access to template context
3. **Complex Objects**: May not serialize well for display
4. **Import Errors**: Returns empty string if module/function not found

## Best Practices

### ✅ DO

```django
<!-- Use with known, safe functions -->
{% functional 'math.sqrt' value %}

<!-- Use with your own controlled modules -->
{% functional 'myapp.utils.safe_function' arg %}

<!-- Use for simple calculations -->
{% functional 'len' items %}
```

### ❌ DON'T

```django
<!-- Don't use with user input -->
{% functional user_provided_function_name %}  <!-- DANGEROUS! -->

<!-- Don't use for complex business logic - use views instead -->
{% functional 'complex.business.logic' %}  <!-- Should be in view -->

<!-- Don't use for database operations in templates -->
{% functional 'models.User.objects.create' %}  <!-- NEVER do this -->
```

## Alternative Approaches

Consider these alternatives before using `functional`:

1. **Custom Template Tags**: More secure and explicit
2. **Template Filters**: For value transformations
3. **View Context**: Calculate in view and pass to template
4. **Model Methods**: Add methods to your models
5. **Context Processors**: For globally available functions

## Reference Implementation

Source: `trim.templatetags.functional`

```python
@register.simple_tag(takes_context=False)
def functional(name, *args, **kwargs):
    """Dynamically call any Python function by its fully qualified name."""
    _callable = locate(name)
    if not _callable:
        return ''
    
    if not callable(_callable):
        return str(_callable)
    
    return _callable(*args, **kwargs)
```

## Security Considerations

To use this tag safely in production:

1. **Whitelist Functions**: Only allow specific function names
2. **Input Validation**: Never use user input for function names
3. **Audit Usage**: Review all uses of this tag in templates
4. **Consider Alternatives**: Use custom template tags when possible
5. **Environment Restrictions**: Disable or restrict in production settings

### Example: Whitelisted Wrapper

```python
# In your own templatetags file
ALLOWED_FUNCTIONS = {
    'math.sqrt',
    'math.floor',
    'len',
    'myapp.utils.format_price',
}

@register.simple_tag
def safe_functional(name, *args, **kwargs):
    if name not in ALLOWED_FUNCTIONS:
        return ''
    return functional(name, *args, **kwargs)
```

## Related

- [Custom Template Tags (Django Docs)](https://docs.djangoproject.com/en/stable/howto/custom-template-tags/)
- [Template Filters](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#built-in-filter-reference)
- [`{% updated_params %}` tag](./updated_params.md) - Update URL parameters
- [`{% link %}` tag](./link/readme.md) - Generate links from view names
