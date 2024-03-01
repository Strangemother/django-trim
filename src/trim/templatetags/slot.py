from django.template import Context
from django import template
from django.template.base import token_kwargs
from . import quickforms
# from .slots.base import inject_node
from .slots.slot_node import parse_until, do_define_slot, do_slot

from loguru import logger
log = logger.debug

register = template.Library()


register.tag(name="slot.define")(do_define_slot)
register.tag(name="slot")(do_slot)
