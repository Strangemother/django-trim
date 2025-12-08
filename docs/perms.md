# Permissions

**Module:** `trim.perms`

Build Django permission strings using a fluent, chainable API. Perfect for generating multiple permission strings for model CRUD operations without repetitive typing.

## Quick Example

```py
from trim.perms import props

# Generate CRUD permissions for a model
perms = props.myapp.MyModel.crud
# Results in: myapp.add_mymodel, myapp.view_mymodel, 
#             myapp.change_mymodel, myapp.delete_mymodel

# Single permission
perm = props.stocks.StockCount + 'view'
# Results in: stocks.view_stockcount
```

## Usage

### Basic Permission String

Build permission strings using dot notation that mirrors Django's app and model structure:

```py
from trim.perms import props

# Single permission
view_perm = props.blog.Post + 'view'
# 'blog.view_post'

# Multiple permissions
perms = props.blog.Post + ['view', 'change']
# Creates permission set for 'view' and 'change'
```

### CRUD Shortcut

Use the `.crud` property to quickly generate all four standard Django permissions:

```py
from trim.perms import props

# Generate add, view, change, and delete permissions
perms = props.inventory.Product.crud

# Equivalent to:
# - inventory.add_product
# - inventory.view_product  
# - inventory.change_product
# - inventory.delete_product
```

### Custom Permission Sets

Build custom permission combinations:

```py
from trim.perms import props

# Read-only permissions
read_only = props.articles.Article + ['view']

# Editor permissions
editor = props.articles.Article + ['view', 'change']

# Full access
full_access = props.articles.Article.crud
```

## Classes

### `EasyPermissionString`

**Purpose:** Fluent API for building Django permission strings without manual concatenation.

**Features:**
- Dot notation for app and model names
- Chainable permission additions
- CRUD shortcut property
- Tuple generation for multiple permissions

#### Attributes

- `index` (int): Current position in the permission string structure
- `positions` (defaultdict): Maps positions to permission action sets
- `strs` (SlofTuple): Internal storage for permission components

#### Properties

##### `.crud`

Adds all four standard Django model permissions: `add`, `view`, `change`, `delete`.

```py
perms = props.app_name.ModelName.crud
# Generates 4 permissions automatically
```

#### Methods

##### `push(index, *items)`

Add permission components at a specific index position.

**Parameters:**
- `index` (int): Position in the permission structure
- `*items`: Permission actions or components to add

**Returns:** New `EasyPermissionString` instance (immutable chain)

```py
perms = props.myapp.MyModel.push(2, 'custom_action')
```

##### `as_tuple()`

Convert the permission builder to a tuple of permission strings.

```py
perms = props.blog.Post.crud
perms.as_tuple()
# Returns tuple of permission strings
```

##### `flat()`

Generate a dot-separated string representation.

**Returns:** String in format `'component1.component2.component3'`

```py
perm = props.blog.Post + 'view'
perm.flat()
# 'blog.post.view'
```

#### Operators

##### `+ str` or `+ list/tuple`

Add permission actions to the current permission string.

```py
# Single action
perm = props.blog.Post + 'view'

# Multiple actions
perms = props.blog.Post + ['view', 'change', 'delete']
```

---

### `SlofTuple`

**Purpose:** Enhanced tuple with "slice of" functionality for extracting elements at the same index from nested tuples.

Useful for working with structured permission data where you need to extract specific positions across multiple entries.

#### Methods

##### `slof(index)`

Extract the element at `index` from each tuple in the collection.

**Parameters:**
- `index` (int): Position to extract from each nested tuple

**Returns:** New `SlofTuple` containing extracted elements

**Example:**

```py
from trim.perms import SlofTuple

content = SlofTuple([('c', 'b'), ('g', 'r')])
result = content.slof(0)
# SlofTuple(('c', 'g'))

result = content.slof(1)  
# SlofTuple(('b', 'r'))
```

## Common Patterns

### View Permission Checks

```py
from django.contrib.auth.decorators import permission_required
from trim.perms import props

@permission_required(str(props.blog.Post + 'view'))
def post_detail(request, pk):
    # View implementation
    pass
```

### Class-Based View Permissions

```py
from django.contrib.auth.mixins import PermissionRequiredMixin
from trim.perms import props

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    permission_required = str(props.blog.Post + 'change')
```

### Multiple Permission Requirements

```py
from trim.perms import props

perms = props.inventory
admin_perms = [
    perms.Product.crud,
    perms.Category.crud,
    perms.Supplier + ['view', 'change']
]
```

### Dynamic Permission Generation

```py
from trim.perms import props

def get_model_permissions(app_name, model_name, actions):
    """Generate permission strings dynamically."""
    builder = getattr(getattr(props, app_name), model_name)
    return builder + actions

# Usage
perms = get_model_permissions('blog', 'Post', ['view', 'change'])
```

## Integration with Django

### Using with `@permission_required`

```py
from django.contrib.auth.decorators import permission_required
from trim.perms import props

# Convert to string for decorator
perm_string = str(props.articles.Article + 'change')

@permission_required(perm_string)
def edit_article(request, pk):
    # ...
    pass
```

### Using with PermissionRequiredMixin

```py
from django.contrib.auth.mixins import PermissionRequiredMixin
from trim import views
from trim.perms import props

class ArticleEditView(PermissionRequiredMixin, views.UpdateView):
    model = Article
    permission_required = str(props.articles.Article + 'change')
```

### Using with `has_perm()`

```py
from trim.perms import props

def check_user_permissions(user, app, model):
    view_perm = getattr(getattr(props, app), model) + 'view'
    return user.has_perm(str(view_perm))
```

## Notes

- Permission strings follow Django's convention: `app_label.action_modelname`
- Model names are automatically lowercased to match Django's permission format
- The API is immutable - each operation returns a new instance
- Use `str()` or `.flat()` to get the final permission string
- The `.crud` property is a convenient shortcut for standard model permissions

## Related

- [Views - Permissioned](./views/authed-views.md#Permissioned) - Using permissions with views
- [Django Permissions Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization)

---

*This module provides a more ergonomic way to build Django permission strings, reducing typos and improving code readability when working with multiple permissions.*
