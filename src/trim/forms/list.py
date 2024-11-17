from django import forms
from trim.forms import fields

class ListForm(forms.Form):

    count = fields.integer(required=False)
    order_by = fields.chars(required=False)
    direction = fields.chars(required=False)

