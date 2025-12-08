---
applyTo: "**/*.py"
---

# Python Best Practices for `django-trim`

- **Follow exact [PEP8](https://peps.python.org/pep-0008/) style:**
  - Use 4 spaces per indentation level.
  - Limit lines to 79 characters.
  - Use blank lines to separate functions and classes.
  - Use clear, descriptive names for variables, functions, and classes.
  - Place imports at the top of the file, grouped by standard library, third-party, and local imports.
- **Clarity and Simplicity:**
  - Write code that is easy to read and understand.
  - Prefer explicit over implicit constructs.
  - Add docstrings to all public modules, functions, classes, and methods.
- **Jay's Preferences:**
  - Prefer small, single-purpose functions with clear return values.
  - Use early returns instead of nested `if/else` or switch/case logic.
  - Avoid deep nesting; refactor complex logic into helper functions.
  - Use list comprehensions and generator expressions for clarity when appropriate.
  - Avoid side effects in functions unless necessary.
- **General:**
  - Use type hints where possible.
  - Add comments to explain non-obvious code.
  - Write tests for all new features in `src/trim/tests.py` or related submodules.

# Example: Preferred Function Style
```python
def get_eggs_count(basket):
    """Return the number of eggs in a basket, or 0 if not set."""
    if not basket:
        return 0
    return getattr(basket, 'eggs', 0)
```

# Example: Early Return
```python
def is_valid_user(user):
    if user is None:
        return False
    if not user.is_active:
        return False
    return True
```

---

- Django class-based views should follow standard patterns.


# For more, see `src/trim/`, `docs/`, and code comments for usage patterns.

