# Models

Reduce typing on models! Import ready-to-use fields for your models.
All fields shadow the existing django field.

Here's a fast example:

_models.py_

```py
from django.db import models
from trim.models import fields

class ContactMessage(models.Model):
    user = fields.user_fk(nil=True)
    sender = fields.email(nil=True)
    cc_myself = fields.bool_false()
    subject = fields.chars(max_length=255, nil=True)
    message = fields.text(nil=False)
    created, updated = fields.dt_cu_pair()
```

All fields a shadowed with a functional caller, making them extremely predicable and short to type.

|     |     |     |
| --- | --- | --- |
|     |     |     |
|     |     |     |
