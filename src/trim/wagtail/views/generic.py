from django.db import models
from wagtail.admin.panels import (FieldPanel, ObjectList, TabbedInterface,
                                  TitleFieldPanel)
from wagtail.api import APIField
from wagtail.models import Page

# from trim.wagtail import blocks as wbl
from trim.wagtail.streamfield import \
    prepared_streamfield  # FieldPanel,; APIField,; # as_fieldpanel_list,; # as_api_fields,

# from wagtail import blocks




# class BlogPage(Page):
#     # field definitions omitted

#     content_panels = [
#         TitleFieldPanel('title', classname="title"),
#         FieldPanel('date'),
#         FieldPanel('body'),
#     ]


class StructuredPage(Page):
    author = models.CharField(max_length=255)
    # date = models.DateField("Post date")
    body = prepared_streamfield("default")

    styles_panels = [
        # FieldPanel('advert'),
        FieldPanel("author"),
        # InlinePanel('related_links', heading="Related links", label="Related link"),
    ]

    # content_panels = Page.content_panels + as_fieldpanel_list(
    #         'body',
    #         # 'date',
    #         # 'author',
    #     )
    content_panels = Page.content_panels + [
        # TitleFieldPanel('title', classname="title"),
        # FieldPanel('date'),
        FieldPanel("body"),
    ]

    api_fields = [
        # APIField('date'),
        APIField("body"),
        # APIField('author'),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(styles_panels, heading="Styles"),
            ObjectList(Page.promote_panels, heading="Promote"),
        ]
    )

    class Meta:
        abstract = True
