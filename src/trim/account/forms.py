from django import forms

from trim.forms import fields


class EmailChangeToken(forms.Form):
    token = fields.str()
