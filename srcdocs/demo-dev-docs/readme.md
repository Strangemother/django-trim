---
title: Home
tags:
    - eggs
    - butter
---


> EXAMPLE

This demo-dev-docs serves as a test and example for the trim docs tools.
IT's essentially the example `srcdocs` a developer can build

It contains a range of research and existing tags

---


Fundmamentally this is a django website (Or like... an app) - but renders _pre_ markdown to markdown.

If the output has a frame (a wrapper of sorts) - then the output is browser compatible.


---


# Pre Markdown Doc

The pre-markdown doc renders markdown. You may include special syntax to DRY your docs.

{% siblings %}

{% insert "./getting-started/how-does-it-work.md" %}{% endinsert %}

## Examples

This file is markdown. But you can include fancy extras, applied to the content
before its converted to markdown.

### Siblings

Include a file neighbour list using `{% verbatim %}{% siblings %}{% endverbatim %}`:

{% siblings "examples/" %}

{% insert "./source-code-sub.md" %}content{% endinsert %}