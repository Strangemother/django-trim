
from django import template
from .slots.wrap_node import do_wrap


register = template.Library()


register.tag(name="wrap")(do_wrap)