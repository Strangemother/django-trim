# Fields

All `trim.models.fields` shadow the standard Django field. They are designed to be completely interchangable.

```py
from trim.models import fields


class StockChange(models.Model):
    """A Stock change occurs for:

    + a document upload (stock list file)
    + A user purchase
    + Human change.

    A record is created detailing the instigator.
    """

    # user # who made the change
    # reason = document | purchase | user (Admin)
    stockcount = fields.fk(StockCount)
    from_count = fields.int(0)
    to_count = fields.int(1)
    created, updated = fields.dt_cu_pair()
    (
        associated,
        associated_content_type,
        associated_object_id
    ) = fields.any(prefix='associated')

    @property
    def count(self):
        return self.to_count

    def get_delta(self):
        return self.to_count - self.from_count
```

## Django Fields

```py
from trim.models import fields

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


# Date Time
date(*a, **kw)
datetime(*a, **kw)
blank_dt(*a, **kw)
dt_created(*a, **kw)
dt_updated(*a, **kw)
# A special pair
created, updated = dt_cu_pair(*a, **kw)
# delta
duration(*a, **kw)
time(*a, **kw)

# FK and M2M
fk(other, *a, on_delete=None, **kw)
user_fk(*a,**kw)
self_fk(*a, **kw)
o2o(other, *a, on_delete=None, **kw)
user_o2o(*a, **kw)
m2m(other, *a, **kw)
self_m2m(other, *a, **kw)

# ContentTypes
contenttype_fk(content_type=None, *a, **kw)
generic_fk(content_type_field='content_type', id_field='object_id', **kw)
unit, unit_content_type, unit_object_id = fields.any(prefix='unit')

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
```


## Function Aliases

Django `trim` is designed to be _ready-to-go_ and specifically designed to remove the language barrier to "correct" method names.

All `trim.models.fields` have a _flipped_ name as an alias to the original function:

```py
from trim.models import fields

class MyModel(models.Model):
    user = fields.user_fk()
    owner = fields.fk_user()
```

This allows you to assume your preferred flavour, without _learning_ a special `trim` language.

    | Field | Alternatives | ... |
    | --- | --- | --- |
    | float | float_ |
    | auto_small | small_auto |
    | auto_big | big_auto |
    | int_small | small_int |
    | int_big | big_int |
    | int_pos | pos_int |
    | int_small_pos | pos_small_int |
    | int_big_pos | pos_big_int |
    | int_ | integer |
    | int | integer |
    | --- | --- | --- |
    | str | string | chars |
    | --- | --- | --- |
    | boolean_null | bool_null | null_bool |
    | boolean_true | bool_true | true_bool |
    | boolean_false | bool_false | false_bool |
    | bool | boolean |
    | --- | --- | --- |
    | dt_blank | blank_dt |
    | dt | datetime |
    | created | dt_created |
    | updated | dt_updated |
    | --- | --- | --- |
    | any_model | any |
    | o2o_user | user_o2o |
    | fk_user | user_fk |
    | fk_self | self_fk |
    | m2m_self | self_m2m |
