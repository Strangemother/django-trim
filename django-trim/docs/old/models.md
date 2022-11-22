## Short String

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

## Fields

```py
from short import shorts

# Stringy
url(*a, **kw)
text(*a, **kw)
chars(first_var=None, *a, **kw)
email(*a, **kw)

# Special Stringy
binary(*a, bytes=2_097_152, **kw)
slug(*a, **kw)
ip_addr(*a, **kw)
json(*a, **kw)

# Boolean
null_bool(*a, **kw)
true_bool(*a, **kw)
false_bool(*a, **kw)
boolean(*a, **kw)

auto(*a, **kw)
# UUID
uuid_null(*a, **kw)
pk_uuid(*a, **kw)
uuid(*a, **kw)


# Date Time Duration
date(*a, **kw)
datetime(*a, **kw)
blank_dt(*a, **kw)
dt_created(*a, **kw)
dt_updated(*a, **kw)
duration(*a, **kw)
time(*a, **kw)

# FK and M2M
fk(other, *a, on_delete=None, **kw)
user_fk(*a,**kw)
m2m(other, *a, **kw)
o2o(other, *a, on_delete=None, **kw)
user_o2o(*a, **kw)

# Numbers
integer(*a, **kw)
float_(*a, **kw)
pos_small_int(*a, **kw)
small_auto(*a, **kw)
small_int(*a, **kw)
big_auto(*a, **kw)
big_int(*a, **kw)
pos_big_int(*a, **kw)
pos_int(*a, **kw)
decimal(*a, digits=19, places=10, **kw)

# Files
file(*a, **kw)
image(*a, **kw)
filepath(*a, **kw)

auto_small = small_auto
auto_big = big_auto
int_small = small_int
int_big = big_int
int_pos = pos_int
int_small_pos = pos_small_int
int_big_pos = pos_big_int
dt_blank = blank_dt
o2o_user = user_o2o
fk_user = user_fk
```
