from pathlib import Path
from django.template.base import TemplateSyntaxError
# from django.conf import settings
from . import config
## The range of template Theming classes for the {{ theme }} template tags.
# the 'default' theming is applied to the module `theming` instance.
themers = {}
theming = None

class NoThemingTemplateFound(Exception):
    pass


def find_template(mappings, name, root=None, version=None):
    map_filename = mappings.get(name)
    if map_filename is None:
        raise NoThemingTemplateFound(name)

    root = config.theme_option('root', root, './')
    version = config.theme_option('version', version, '')

    if map_filename.startswith('/'):
        # No rooting - the template name is literal
        # /templates/[map_filename]
        return str(Path('') / version / map_filename[1:])
    return str(Path(root) / version / map_filename)


class Theming(object):

    def __init__(self, theme_map=None, key=None):
        self.theme_map = theme_map or {}
        self.key = key

    def get_theme_map(self):
        if callable(self.theme_map):
            return self.theme_map()
        return self.theme_map

    def _resolve(self, name=None):
        try:
            return find_template(self.get_theme_map(), name)
        except NoThemingTemplateFound:
            raise TemplateSyntaxError(f'theming name "{name}" did not resolve')

    def _template_resolve(self, name=None):
        res = self._resolve(name=name)
        if res is None:
            raise TemplateSyntaxError(f'theming name "{name}" did not resolve')
        return res

    def resolve_theme_parent(self, bits, origin, context):
        key = '.'.join(bits)
        return self._template_resolve(name=key)

    def _loop_response(self, k):
        return self._resolve(k)

    def __getattr__(self, k):
        return self._loop_response(k)

    def __getitem__(self, k):
        return self._loop_response(k)

    def __str__(self):
        """Called by the template when applied to the view.
        """
        return self._template_resolve(name=self.key)


def build_default_themer():
    global theming
    theming = themers['default'] = Theming(config.get_theme_map)


def magic_strings(request):
    return {'theme': themers['default'] }

