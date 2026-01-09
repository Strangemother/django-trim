from django.conf import settings

## Baked 'settings' for the theming unit. These vars stay bound outside
# the options of the template usage. In some cases (such as `version`) the
# option may be overridden - but generally these should be static during
# runtime.
THEMING_OPTIONS = {
    "root": "theme",
    "version": "",
}

THEMING_MAP_DEFAULTS = {
    "form": "form.html",
    "page": "page.html",
    "list": "list.html",
    "detail": "detail.html",
}

## The name -> file map exposed through the {% theme %} and {{ theme }}
# template tags. This is mapped into the _forced_ theming options, ensuring
# the templates may call _into_ one directory. By default this is the given
# "theme"
THEMING_MAP = getattr(
    settings,
    "THEMING_MAP",
    {
        # 'detail.double': 'detail-double-header.html',
        # 'detail.default': 'detail.html',
    },
)

from collections import ChainMap

LIVE_MAPS = {"ready_map": ChainMap(THEMING_MAP, THEMING_MAP_DEFAULTS)}


def set_ready_map(data):
    LIVE_MAPS["ready_map"] = data


def get_theme_map():
    return LIVE_MAPS["ready_map"]


def name_redirect(origin, target):
    THEMING_MAP.setdefault(origin, get_theme_map()[target])


def name_default_redirect(
    origin,
    target,
    target_template,
    default_template=None,
    default_word="default",
    sep=".",
):
    """Build a redirection of a default template name, to a special template
    name, "detail" -> "detail.other", with the _other_ as the new primary.

        name_default_redirect('detail', 'other', 'detail-other.html',)

    Producing a THEME entry:

        'detail.other' = 'detail-other.html'
        'detail.default' = 'detail.html'

    Functionally this is similar to:

        THEMING_MAP = {
            'detail.double': 'detail-double-header.html',
            'detail.default': 'detail.html',
        }
        THEMING_MAP.setdefault('detail', THEMING_MAP['detail.double'])

    """
    # Create the 'detail.default' entry
    default_key = sep.join([origin, default_word])
    default_template = default_template or get_theme_map().get(origin)
    THEMING_MAP.setdefault(default_key, default_template)

    # Create the _new_ entry
    new_key = sep.join([origin, target])
    THEMING_MAP.setdefault(new_key, target_template)

    # Add the redirect "detail" => "detail.double"
    return name_redirect(origin, new_key)


## Install a _default redirect_, allowing the import of the "detail"
# and it invisibly resolves "detail.double" with the addition "details.default"
# created automatically.
# name_default_redirect('detail', 'double', 'detail-double-header.html',)

## for base variants its nice to set
# the default to an inner key.
# The inner key may be prone to change, but the outer key (detail)
# should stay stable to the template.
# THEMING_MAP.setdefault('detail', THEMING_MAP['detail.double'])

UNDEF = {}


def theme_option(key, var=UNDEF, default=None):
    if var in (None, UNDEF):
        OPTS = getattr(settings, "THEMING_OPTIONS", None) or THEMING_OPTIONS
        return OPTS.get(key, default)
    return var


def install(*maps, **kw):
    """Install a theme pack from the user `theming.py` loadout."""
    ready_map = get_theme_map()
    scope = ready_map.new_child()
    for md in maps:
        scope.update(md)
    set_ready_map(scope)
    # print('trim.theming.config.install', ready_map)
    return scope
