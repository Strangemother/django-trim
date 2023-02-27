# Short String

Easy integrate `__str__` and `__repr__` with the `_short_string` trick:

**Before** (default):

```py
>>> p = models.Product.objects.first()
<Product: Product object (3)>
>>> print(p)
Product object (3)
```

**add shorts** upgrade:

```py
class Product(models.Model):
    # ... all previous fields
    _short_string = '"{self.name}" x{self.count}'

    def get_short_string(self):
        s = '"{self.name}"' if self.count == 1 else self._short_string
        return s.format(self=self)
```

**After:**

```py
>>> p = models.Product.objects.first()
<Product(3) '"example name" x4'>
>>> print(p)
"example name" x4
```
