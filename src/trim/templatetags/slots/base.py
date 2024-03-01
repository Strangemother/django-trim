from django.template import Context
from django import template
from django.template.base import token_kwargs

from loguru import logger

log = logger.debug


def inject_node(parser):
    T=parser.tokens[0].__class__
    tr = "{{ slotplot }}"
    parser.prepend_token( T(parser.tokens[0].token_type, tr))


def parse_until(parser, token, ends, delete_first=True):
    """`parser` is the iterative unit processing the nodes
    The `token` represents the current block, such as '<block token "wrap">'
    `ends` are a list of end-tokens to stop the parser

    """
    nodelist = parser.parse(ends)
    if delete_first:
        parser.delete_first_token()
    # inject_node(parser)
    splits = token.split_contents()[1:]
    extra = {}
    for i, word in enumerate(splits):
        if word == 'with':
            extra = token_kwargs(splits[i+1:], parser)
    return nodelist, splits, extra


class SlotList(object):
    def __init__(self, *a, **kw):
        log('  _def_ new SlotList', id(self))
        self.units =()

    def add(self, unit):
        # log(' -- SlotList.add', unit)
        self.units += (unit,)

    def set(self, iterable):
        self.units = tuple(iterable)

    def apply_lost(self, nodelist, context=None):
        """Apply the given nodelist to the 'lost' node, for
        the incoming render request.
        """
        log(f'{len(nodelist)} items')
        lost_slots = self.get_nodes('lost', context)
        for name, unit in lost_slots:
            log(f'Slot found: {unit}')

    def get_nodes(self, first_token, context=None):
        """Return the target node given the name, this
        could be None, "default" or _named_
        """
        res = ()

        for unit in self.units:
            names = unit.get_slot_names(context)
            if first_token in names:
                log(f'Found match! {first_token}')
                res += ((first_token, unit,),)

        return res # default_value # content = slotlist.

    def __len__(self):
        return len(self.units)

    def __repr__(self):
        return f'<{self.__class__.__name__} {len(self.units)} slots>'

