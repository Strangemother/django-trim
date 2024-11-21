from django import forms
from trim.forms import fields

class AllFieldsForm(forms.Form):
    boolean = fields.boolean()
    boolean_false = fields.boolean_false()
    boolean_true = fields.boolean_true()
    chars = fields.chars()
    hidden_chars = fields.hidden_chars()
    password = fields.password()
    text = fields.text()
    choice = fields.choice()
    date = fields.date()
    datetime = fields.datetime()
    decimal = fields.decimal()
    duration = fields.duration()
    email = fields.email()
    file = fields.file()
    files = fields.files()
    file_path = fields.file_path()
    float = fields.float()
    generic_ip_address = fields.generic_ip_address()
    image = fields.image()
    integer = fields.integer()
    json = fields.json()
    multiple_choice = fields.multiple_choice()
    null_boolean = fields.null_boolean()
    regex = fields.regex()
    slug = fields.slug()
    time = fields.time()
    typed_choice = fields.typed_choice()
    typed_multiple_choice = fields.typed_multiple_choice()
    url = fields.url()
    uuid = fields.uuid()
    combo = fields.combo(fields=[fields.chars(), fields.email()])
    multi_value = fields.multi_value()
    split_datetime = fields.split_datetime()
    modelchoice = fields.modelchoice()
    hidden = fields.hidden()