from django.template.base import Template
from django.template.response import TemplateResponse

try:
    import markdown as markdown_orig
except ImportError:
    markdown_orig = None


__all__ = [
    "MissingImportError",
    "MarkdownToMarkdownTemplateResponse",
    "MarkdownTemplateResponse",
    "MarkdownDoubleTemplateResponse",
    "MarkdownReponseMixin",
]


class MissingImportError(ImportError):
    """The trim.markdown.MarkdownTemplateResponse required a markdown
    renderer. If missing (at execution time), raise this import error.
    """

    pass


class MarkdownTemplateResponse(TemplateResponse):
    """Expecting a .md template file - perform standard rendering, coverting
    to HTML and return the finished page.
    """

    @property
    def rendered_content(self):
        """Return the freshly rendered content for the template and context
        described by the TemplateResponse.

        This *does not* set the final content of the response. To set the
        response content, you must either call render(), or set the
        content explicitly using the value of this property.
        """
        # django.template.backends.django.Template
        template = self.resolve_template(self.template_name)
        context = self.resolve_context(self.context_data)

        source_text = template.template.source
        md = self.get_markdown_object(context)
        html = md.convert(source_text)

        meta = md.Meta
        context["metadata"] = meta

        old_inner = template.template
        inner = Template(html, old_inner.origin, old_inner.name, old_inner.engine)
        template.template = inner
        res = template.render(context, self._request)
        return res

    def get_markdown_object(self, context):
        # context['view']

        if "view" in context:
            if hasattr(context["view"], "get_markdown_object"):
                return context["view"].get_markdown_object()
        # meta into the context.
        # HTML is the raw
        # https://python-markdown.github.io/extensions/
        extensions = [
            "meta",
            "extra",
        ]

        if markdown_orig is None:
            raise MissingImportError("markdown module is not installed.")

        md = markdown_orig.Markdown(extensions=extensions)
        return md


class MarkdownToMarkdownTemplateResponse(MarkdownTemplateResponse):

    @property
    def rendered_content(self):
        """Return the freshly rendered content for the template and context
        described by the TemplateResponse.

        This *does not* set the final content of the response. To set the
        response content, you must either call render(), or set the
        content explicitly using the value of this property.
        """
        # django.template.backends.django.Template
        template = self.resolve_template(self.template_name)
        context = self.resolve_context(self.context_data)

        source_text = template.template.source
        old_inner = template.template
        inner = Template(
            source_text, old_inner.origin, old_inner.name, old_inner.engine
        )
        template.template = inner
        res = template.render(context, self._request)
        return res


class MarkdownDoubleTemplateResponse(MarkdownTemplateResponse):
    """USe the default template as the wrapper for the markdown -
    the markdown has its own render chain.
    Provide the markdown object to the context of the original template
    """

    @property
    def rendered_content(self):
        """Return the freshly rendered content for the template and context
        described by the TemplateResponse.

        This *does not* set the final content of the response. To set the
        response content, you must either call render(), or set the
        content explicitly using the value of this property.
        """
        # django.template.backends.django.Template
        context = self.resolve_context(self.context_data)

        view_template = self.resolve_template(self.template_name)
        view_source = view_template.template.source
        view_inner = view_template.template

        # Convert the view source (the template_name markdown file) to HTML
        md = self.get_markdown_object(context)
        markdown_html = md.convert(view_source)
        # The markdown template is considered incomplete view template
        md_inner = Template(
            markdown_html, view_inner.origin, view_inner.name, view_inner.engine
        )
        view_template.template = md_inner
        meta = md.Meta

        context["metadata"] = meta
        context["markdown"] = {
            # render the incomplete markdown HTML to finished HTML
            "html": view_template.render(context, self._request),
            "object": md,
            "meta": meta,
        }

        # grab the template name from the meta data within the markdown.
        layout_template = self.resolve_template(meta["template_name"])
        # The layout (the template_name from the meta of the original view markdown file)
        return layout_template.render(context, self._request)


class MarkdownReponseMixin(object):
    response_class = MarkdownTemplateResponse
    # response_class = MarkdownDoubleTemplateResponse
