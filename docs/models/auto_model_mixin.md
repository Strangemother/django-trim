# Auto Model Mixin

As the name describes, the _automatic_ model mixin applies methods and non-prive attributes to a target model. Use this to apply functions aross apps, without polluting the _other_ apps with feature functions.

## Usage

For example, add an method to an expected model, without altering the target model manually:

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


_stock/models.py_
```py

from trim.models import AutoModelMixin
from . import models # stock.models

class StockMixin(AutoModelMixin):

    def in_stock(self, product):
        return models.StockCount.stock_count(product=product) > 0

    class Meta:
        model_name = 'baskets.Cart'
```

With the app you can use your `in_stock` method on the `Cart`

```py
>>> from baskets.models import Cart
>>> cart = Cart.objects.first()
>>> cart.in_stock(cart.items.first())
True
```


## How it Works

The `trim.apps` main App ready function hooks to all `init` models during runtime.
If a record exists within `trim.models.auto.classes` the hook function sets any public methods and attributes from the mixin classes onto the target model.

The methods are applied from first to last for discoveries within the class register. This is designed to be fairly _dumb_, to ensure the django models `mappedproxy` internal dictionary remains intact.
