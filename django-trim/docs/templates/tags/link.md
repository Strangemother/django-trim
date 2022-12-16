# Links

A very common task during development is _making hyperlinks_. Therefore links is part of the common tags.

Generate a hyperlink to a view with `{% link viewname arguments text %}`

## Usage

Basic usage is quick:

```jinja2
{% load link %}
{% link "appname:viewname" %}
```

Producing a finished `<a>` ref:

```jinja2
<!-- {% link "baskets:shippingaccount-detail" object.pk "more info" %} -->
<a href="/baskets/shipping-accounts/item/7/">more info</a>
```

### Arguments

Provide url expected arguments. This acts similar to the `url` tag:

```jinja2
<!-- {% link "shipping:company" request.user.business_name 
shipping.company "My Company Shipping" %} -->
<a href="/shipping/companies/acme/fedeks/">My Company Shipping</a>
```

The last argument is always used as text. 

```jinja2
<!-- {% link "shipping:company" request.user.business_name 
shipping.company %} -->
<a href="/shipping/companies/acme/fedeks/">fedeks</a>
```

## Text Label

You may provide all your link argument inline. The last argument item is the link _text_.

For example you have a model with a renderable string:

```python
class Meal(models.Model):
    name = fields.chars(100)
    user = fields.user_fk()

    def __str__(self):
        str_parts = ( self.name.title(),
                      self.__class__.__name__,
                      self.user,
                    )
        return f'{0} {1} for {3}'.format(*str_parts)
```

We can use the `__str__` string as expected by supplying the object as the last arg:

```jinja2
<!-- {% link "meals:user-choice-detail" request.user
object.name object %} -->
<a href="/meals/derek_malone/pizza/">Pizza Meal for Derek</a>
```

Under the hook `link` utilised the standard `reverse` and a template `trim/link.html`

### Attributes

A `link` accepts any attributes and applys them to the `<a>` ref - such as `class` or any other HTML attribute.

note: You do not use `with` syntax

```jinja2
<!-- {% link "shipping:company" request.user.business_name 
shipping.company "My Company Shipping" class='button large' target='_blank' %} -->

<a href="/shipping/companies/acme/fedeks/" 
   target='_blank'
   class='button large'>My Company Shipping</a>
```

With this you can essentially build any hyperlink you need - such as external `noreferrer` and other html attributes. 
