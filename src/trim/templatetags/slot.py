from django import template
from django.template import Context
from django.template.base import token_kwargs
from loguru import logger

from . import quickforms
# from .slots.base import inject_node
from .slots.slot_node import do_define_slot, do_slot, parse_until

log = logger.debug

register = template.Library()


register.tag(name="slot.define")(do_define_slot)
register.tag(name="slot")(do_slot)
