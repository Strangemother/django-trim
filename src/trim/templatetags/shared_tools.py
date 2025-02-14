
from django.template.base import token_kwargs


def parse_until(parser, token, ends):
    """Gather all information within the context of the parser until the `ends`
    are met:


        @register.tag(name="markdown")
        def do_slot(parser, token):
            nodelist, splits, extra = parse_until(parser, token, ('endmarkdown',))
            return MarkdownContentNode(nodelist, splits, **extra)

    """
    nodelist = parser.parse(ends)
    parser.delete_first_token()
    # rather than delete, change;
    # inject_node(parser)
    splits = token.split_contents()[1:]
    extra = {}
    for i, word in enumerate(splits):
        if word == 'with':
            extra = token_kwargs(splits[i+1:], parser)
    return nodelist, splits, extra