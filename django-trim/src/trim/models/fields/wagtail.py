from wagtail.images import get_image_model_string
from wagtail.core.fields import StreamField

from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .django import fk
from .base import defaults

from .. import panels
from wagtail.snippets.models import register_snippet

register = register_snippet

def streamfield(*a, **kw):
    kw = defaults(a, kw, nil=True)
    return StreamField(*a, **kw)


def image_fk(*a, **kw):
    kw = defaults(a, kw, related_name='+')
    return fk(get_image_model_string(), *a, **kw)

image = image_fk
