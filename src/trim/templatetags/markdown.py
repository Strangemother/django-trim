from django import template
from django.urls import resolve, reverse
from django.conf import settings


try:
    import markdown as markdown_orig
except ImportError:
    markdown_orig = None


register = template.Library()

# @register.simple_tag(takes_context=True, name='file_content')
# def file_content(context, view_name, *url_args, **kwargs):

@register.inclusion_tag('trim/templatetags/markdown_file_content.html', takes_context=True,
                        name='markdown.file')
def src_code_content_template(context, filename, *args, **kwargs):
    """Load and process a markdown file.
    """
    info = get_file_contents(filename, settings.POLYPOINT_DOCS_DIR)
    if info['exists']:
        content = info['content']
        md = get_markdown_object()
        info['html'] = md.convert(content)
        info['metadata'] = md.Meta

    return {
        'lang_class': 'language-javascript',
        'markdown_object': info,
    }


def get_markdown_object():
    # context['view']

    # meta into the context.
    # HTML is the raw
    # https://python-markdown.github.io/extensions/
    extensions=[
        'meta',
        'extra',
    ]

    if markdown_orig is None:
        raise MissingImportError('markdown module is not installed.')

    md = markdown_orig.Markdown(extensions=extensions)
    return md


def get_file_contents(path, parent=None):
    parent = parent or settings.POLYPOINT_DEMO_DIR
    target = parent / path
    print('target', target)
    exists = target.exists()
    content = None
    if exists:
        content = target.read_text()
    return {
        'filepath': target,
        'exists': exists,
        'content': content,
    }