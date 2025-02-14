
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

from django.template.loader_tags import (
        TemplateSyntaxError,
    )


def parse_tag(parser, token):
    """REturn bits, the _with_ context,
    """

    bits = token.split_contents()

    res_bits = []
    options = {}
    tag_name, *remaining_bits = bits
    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError(
                "The %r option was specified more than once." % option
            )
        value = None
        if option == "with":
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError(
                    '"with" in %r tag needs at least one keyword argument.' % bits[0]
                )
            options[option] = value
        else:
            # raise TemplateSyntaxError(
            #     "Unknown argument for %r tag: %r." % (bits[0], option)
            # )
            res_bits.append(option)

    namemap = options.get("with", {})

    return res_bits, namemap, options