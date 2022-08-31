from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel


def image(*a, **kw):
    return ImageChooserPanel(*a, **kw)


def streamfield(*a, **kw):
    return StreamFieldPanel(*a, **kw)


def field(*a, **kw):
    return FieldPanel(*a, **kw)


def inline(*a, **kw):
    return InlinePanel(*a, **kw)


def snippet(*a, **kw):
    return SnippetChooserPanel(*a, **kw)
