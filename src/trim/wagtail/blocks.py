"""Wagtail 'blocks' in an easier form:

https://docs.wagtail.org/en/stable/reference/streamfield/blocks.html
"""

try:

    try:
        from wagtail.blocks import *
        from wagtail.fields import StreamField
    except ImportError as e:
        from wagtail.core.blocks import *
        from wagtail.core.fields import StreamField

    from wagtail.embeds.blocks import EmbedBlock
    from wagtail.snippets.blocks import SnippetChooserBlock
    from wagtail.images.blocks import ImageChooserBlock
    from wagtail.documents.blocks import DocumentChooserBlock
    from wagtail.admin.panels import FieldPanel
    from wagtail.api import APIField

    # StreamField
    PREPARED = True
except ImportError as e:
    PREPARED = False
    raise e

if PREPARED is True:
    streamfield = stream_field = StreamField


def field_panel(*a, **kw):
    return FieldPanel(*a, **kw)


def api_field(*a, **kw):
    return APIField(*a, **kw)


fieldpanel = field_panel
apifield = api_field


def chars(*a, **kw):
    return CharBlock(*a, **kw)


def integer(*a, **kw):
    return IntegerBlock(*a, **kw)


def decimal(*a, **kw):
    return DecimalBlock(*a, **kw)


def boolean(*a, **kw):
    return BooleanBlock(*a, **kw)


def datetime(*a, **kw):
    return DateTimeBlock(*a, **kw)


def text(*a, **kw):
    return TextBlock(*a, **kw)


def email(*a, **kw):
    return EmailBlock(*a, **kw)


def float_(*a, **kw):
    return FloatBlock(*a, **kw)


def regex(*a, **kw):
    return RegexBlock(*a, **kw)


def url(*a, **kw):
    return URLBlock(*a, **kw)


def date(*a, **kw):
    return DateBlock(*a, **kw)


def time(*a, **kw):
    return TimeBlock(*a, **kw)


def richtext(*a, **kw):
    return RichTextBlock(*a, **kw)


def rawhtml(*a, **kw):
    return RawHTMLBlock(*a, **kw)


def blockquote(*a, **kw):
    return BlockQuoteBlock(*a, **kw)


def choice(*a, **kw):
    return ChoiceBlock(*a, **kw)


def multiplechoice(*a, **kw):
    return MultipleChoiceBlock(*a, **kw)


def pagechooser(*a, **kw):
    return PageChooserBlock(*a, **kw)


def documentchooser(*a, **kw):
    return DocumentChooserBlock(*a, **kw)


def imagechooser(*a, **kw):
    return ImageChooserBlock(*a, **kw)


def snippetchooser(*a, **kw):
    return SnippetChooserBlock(*a, **kw)


def embed(*a, **kw):
    return EmbedBlock(*a, **kw)


def static(*a, **kw):
    return StaticBlock(*a, **kw)


def struct(*a, **kw):
    return StructBlock(*a, **kw)


def list_(*a, **kw):
    return ListBlock(*a, **kw)


def stream(*a, **kw):
    return StreamBlock(*a, **kw)


str = chars
float = float_
list = list_
dt = date_time = datetime
raw_html = rawhtml
rich_text = richtext
block_quote = blockquote
multiple_choice = multiplechoice
page_chooser = pagechooser
document_chooser = documentchooser
image_chooser = imagechooser
snippet_chooser = snippetchooser
stream_block = stream
