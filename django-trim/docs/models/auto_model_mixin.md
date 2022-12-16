# Auto Model Mixin

As the name describes, the _automatic_ model mixin applies methods and non-private attributes to a target model. Use this to apply functions across apps without polluting the _other_ apps with feature functions.

## Usage

For example, add a method to an expected model, without altering the target model manually:

_otherapp/models.py_

```py
from trim.models import AutoModelMixin

class FooMonkeyMixin(AutoModelMixin):

    def wave(self, word):
        print(f"Hi - I'm a {self} waving {word}")

    class Meta:
        # The target app 'baskets' and its model 'Cart'
        model_name = 'otherapp.Person'
```

```py
>>> from otherapp.models import Person
>>> Person().wave('hello')
"Hi I'm <Person: Person object (None)> waving hello"
```

The `otherapp.Person` now has a `wave()` function. the `self` refers to the target model;`self == Person()`.

Therefore many apps may bind functions to a target model (`otherapp.Person`) without editing the target.

### The `model_name`

The target may be a string or a qualified model:

```py
from trim.models import AutoModelMixin
from trim.models import fields

class HyperlinkList(AutoModelMixin):

    def get_hyperlinks(self):
        return Hyperlink.get_user_models(self)

    class Meta:
        model_name = fields.get_user_model()
```

## Example

As an example, we have a `products.GenericProduct` of which has a _stock_ count.

_product/models.py_

```py
from trim.models import fields
from django.db import models

class GenericProduct(models.Model):
    ...
    product_id = fields.str(50)
```

We _could_ apply a bunch of stock count methods to this model, however this forces us to closely couple the `products` models to stock models.

To correct this, create a `StockAutoMixin` extending the `AutoModelMixin`.

_stock/models.py_

```py
from trim.models import AutoModelMixin
from . import models # stock.models

class StockAutoMixin(AutoModelMixin):

    def in_stock(self):
        return models.StockCount.stock_count(product=self) > 0

    class Meta:
        model_name = 'products.GenericProduct'
```

Within the app you can use your `in_stock` method on the `GenericProduct`

```py
>>> from products.models import GenericProduct
>>> product = GenericProduct.objects.first()
>>> product.in_stock()
True
```

## How it Works

The `trim.apps` main App ready function hooks to all `init` models during runtime.
If a record exists within `trim.models.auto.classes` the hook function sets any public methods and attributes from the mixin classes onto the target model.

The methods are applied from first to last for discoveries within the class register. This is designed to be fairly _dumb_, to ensure the django models `mappedproxy` internal dictionary remains intact.
