# Live Models

> The `trim.live` models is a simple shortcut to your installed django application models without the need to import. Gather any model using standard dotted notation `trim.live.myapp.ModelName`

```py
from trim import live

MyModel = live.myapp.ModelName
```

The "live" models tool provides a fast access method to all the existing installed models using a single concat string resolving to the model.

**Why**

+ **Just works**: Access all your models without pre-loading.
+ **It's Lazy**: Trouble-free Bypassing of early import issues.
+ **Tiny**: One import. All models. No Magic.


## Example

```py
from trim import live

# model cart.Cart
cart = live.carts.Cart.objects.create(demo=True)

# model checkout.Checkout
checkout = live.checkout.Checkout(cart=cart)
checkout.save()
```

---


The `trim.live` object can replace a standard import or the `app.get_model` function.


<table>
<thead><tr>
  <th align="left">Before</th>
  <th align="left">After</th>
</tr></thead>
<tbody><tr valign="top"><td>

Example standard import methods:

```py
from django.apps import apps

from checkout.models import Checkout
from carts.models import Cart

ModelName = apps.get_model('myapp.ModelName')
cart = Cart.objects.create(demo=True)

checkout = Checkout(cart=cart)
checkout.save()
```

</td><td>

The `trim.live` can do exactly same, with one import:

```py
from trim import live

ModelName = live.myapp.ModelName
cart = live.carts.Cart.objects.create(demo=True)

checkout = live.checkout.Checkout(cart=cart)
checkout.save()
```

</td></tbody></table>



## Another Example

In this example we use an example `ShippingAccount` model. The `trim.live` returns the expected class model, allowing normal operations:

<table>
<thead><tr>
  <th align="left">Before</th>
  <th align="left">After</th>
</tr></thead>
<tbody><tr valign="top"><td>

```py
from django.apps import apps

ShippingAccount = apps.get_model('baskets.ShippingAccount')
cart_owner = self.get_object().cart.owner
user_addresses = ShippingAccount.objects.filter(owner=cart_owner, deleted=False)
```

</td><td>

After:

```py
from trim import live

owner = self.get_object().cart.owner
user_addresses = live.baskets.ShippingAccount.objects.filter(
        owner=owner, deleted=False
    )
```

</td></tbody></table>

