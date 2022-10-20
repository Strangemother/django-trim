# Model conditions


> If model.X: Return modelY

Connective elements between models, as _conditions_ built independantly of the models.

```py
class Alpha:
    foo = 1

class Beta:
    foo = 2

class Charlie:
    bar = 3

class Condition:

    def test_next(self, model):
        if model[self.prop] == self.value:
            return Beta
        return Charlie

a = Alpha()
cond = Condition('Foo', 2)

b_or_c = cond.test_next(a)
```
