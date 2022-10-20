
from django.db.models import Model
from .models.auto import hook_init_model_mixins


def str_printer(self, alts=None):
    """Acting as a __str__ replacement. Provide a list of format strings
    as `alts`, with a natural default to '_trim_string'.
    If a function exists matching the string format [get]_trim_string, the function is called.
    """
    apply_label = getattr(self, '_trim_props_label', True)
    self_prop_str = '{self.%(prop)s}'
    default_prop_format = f'%(prop)s="{self_prop_str}"' if apply_label else self_prop_str
    prop_format = getattr(self, '_trim_props_format', default_prop_format)
    alts = (alts or ()) + ('_trim_string',)
    format_str = None

    # Grab the first (best) string format - use a get method if it exists.
    #   self: _trim_string_repr, _trim_string, ...
    for s in alts:

        if hasattr(self, f'get{s}'):
            # self.get_trim_string()
            format_str = getattr(self, f'get{s}')()
            break

        if hasattr(self, s):
            format_str = getattr(self, s)
            break

    if format_str is None:
        # _trim_string or other alt props are not applied.
        if hasattr(self, '_trim_props'):
            props = self._trim_props
            if isinstance(props, (tuple, list)) is False:
                props = (props, )
                # If only one string, then reduce the printout "field=X",
                # to just "X"
                prop_format = self_prop_str

            format_str = ', '.join(prop_format % {'prop':x} for x in props)

    return format_str.format(self=self)


def repr_printer(self):
    cl = self.__class__.__name__
    alts = ('_trim_string_repr',)
    return f"<{cl}({self.pk}) '{str_printer(self, alts)}'>"


def model_pre_init(sender, args, kwargs, **kw):
    hook_init_model_mixins(sender)

    if hasattr(sender, '_trim_string') or hasattr(sender, '_trim_props'):
        # print('model_pre_init', sender, kw)
        if sender.__str__ == Model.__str__:
            sender.__str__ = str_printer

        if sender.__repr__ == Model.__repr__:
            sender.__repr__ = repr_printer

        # sender.__repr__ == Model.__repr__
