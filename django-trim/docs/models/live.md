# Live Models

> The `trim.live` models is a simple shortcut to your installed django application models without the need to import. Gather any model using standard dotted notation `trim.live.myapp.ModelName`

The "live" models tool provides a fast access method to all the existing installed models using a single concat string, resolving to the model.

## Example

```py
from trim import live

other = live.myapp.ModelName
cart = live.carts.Cart.objects.create(demo=True)

checkout = live.checkout.Checkout(cart=cart)
checkout.save()
```

---

Replace a standard model import, or the django get_model import:

Before:

```py
from django.apps import apps

from checkout.models import Checkout
from carts.models import Cart

other = apps.get_model('myapp.ModelName')
cart = Cart.objects.create(demo=True)

checkout = Checkout(cart=cart)
checkout.save()
```

After:

```py
from trim import live

other = live.myapp.ModelName
cart = live.carts.Cart.objects.create(demo=True)

checkout = live.checkout.Checkout(cart=cart)
checkout.save()
```

## Another Example

```py
from django.apps import apps

ShippingAccount = apps.get_model('baskets.ShippingAccount')
cart_owner = self.get_object().cart.owner
user_addresses = ShippingAccount.objects.filter(owner=cart_owner, deleted=False)
```

after:

```py
from trim import live

owner = self.get_object().cart.owner
user_addresses = live.baskets.ShippingAccount.objects.filter(
        owner=owner, deleted=False
    )
```
