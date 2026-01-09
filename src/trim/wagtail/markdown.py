from wagtail.core.blocks import StreamBlock

from wagtailmarkdown.blocks import MarkdownBlock as WM_MarkdownBlock
from trim.wagtail import blocks as t_blocks
from django.forms.widgets import CheckboxSelectMultiple
from django import forms


class Styles(t_blocks.StructBlock):

    styles = t_blocks.MultipleChoiceBlock(
        widget=CheckboxSelectMultiple,
        choices=(
            (
                "flipped",
                "Horizontal Flip",
            ),
            # ('b', 'b',),
        ),
    )

    def __init__(self, required=True, help_text=None, **kwargs):
        super().__init__(**kwargs)
        ss = self.declared_blocks["styles"]
        ch = kwargs.get("choices", (("egg", "Egg"),))
        ss.choices = ch

    class Meta:
        template = "blocks/styles.html"


from wagtail.core.blocks import StructValue


class LinkStructValue(StructValue):
    """
    https://docs.wagtail.org/en/v4.0.1/advanced_topics/customisation/streamfield_blocks.html#additional-methods-and-properties-on-structblock-values
    """

    def html(self):
        text = self.get("content")
        # page = self.get('page')
        return text or "No text for {self}"


class MarkdownBlock(t_blocks.StructBlock):
    content = StreamBlock(
        (
            (
                "text",
                WM_MarkdownBlock(icon="pilcrow"),
            ),
            (
                "document",
                t_blocks.document_chooser(icon="doc-full-inverse"),
            ),
        )
    )

    # text = WM_MarkdownBlock(icon="pilcrow")
    # document = t_blocks.document_chooser(icon="doc-full-inverse")
    css_styles = Styles()

    class Meta:
        template = "blocks/markdown-block.html"
        value_class = LinkStructValue
