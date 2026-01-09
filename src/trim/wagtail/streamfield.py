from django.db import models

from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField

from trim.wagtail import blocks as wbl


FIELDS_CACHE = {"pre": ()}


def pre_install_global_block(name, class_):
    FIELDS_CACHE["pre"] += ((name, class_),)


def get_fields():
    FIELDS = {
        "default": [
            ("heading", HeadingBlock()),
            ("paragraph", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ]
        + list(FIELDS_CACHE["pre"])
    }

    return FIELDS


class TabbedStructBlock(blocks.StructBlock):
    polyclasses = wbl.text(required=False, default="default", group="secondary")
    # dev_note = wbl.text(required=False, default='default', group='styles')

    def render_form_template(self):
        res = super().render_form_template()
        # context = self.get_form_context(
        #     self.get_default(), prefix="__PREFIX__", errors=None
        # )
        # return mark_safe(render_to_string(self.meta.form_template, context))
        return res

    class Meta:
        template = "blocks/default-content-block.html"
        form_template = "block_forms/tabbed-struct-block.html"
        # form_template = 'blocks/default-content-block.html'


class RichTextBlock(TabbedStructBlock):
    # polyclasses = blocks.CharBlock()
    # photo = ImageChooserBlock(required=False)
    content = wbl.richtext()
    # content = blocks.RichTextBlock()

    class Meta:
        icon = "text"
        form_classname = "richtext-block struct-block"
        # template = 'blocks/default-content-block.html'


class HeadingBlock(TabbedStructBlock):
    content = wbl.text()

    class Meta:
        icon = "text"
        form_classname = "title"
        template = "blocks/heading-block.html"


def as_fieldpanel_list(*items):
    """
    content_panels = Page.content_panels + [
        # FieldPanel('author'),
        # FieldPanel('date'),
        FieldPanel('body'),
    ]
    """
    res = ()
    for item in items:
        res += (FieldPanel(item),)
    return list(res)


def as_api_fields(*items):
    """
    # Export fields over the API
    api_fields = [
        # APIField('date'),
        APIField('body'),
        # APIField('author'),
    ]
    """
    res = ()
    for item in items:
        res += (APIField(item),)
    return list(res)


def prepared_streamfield(group="default", **kw):
    items = get_fields().get(group)
    return StreamField(items, **kw)
