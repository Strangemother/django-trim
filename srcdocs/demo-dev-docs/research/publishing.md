# Publishing

All content is generally viewable within the browswer, but by nature of the tool a range of publishing methods are available.

1. `serve` the site in a browser for local editor and viewing.
2. `publish md` is a defaulted _save to output_ routing
3. `publish [html]` produce a html site of the content.

However the product is mostly designed to help you write your `md` files, so it's a translator...


## Serve Locally

Serving the tool locally runs a webserver configured to read a doc directory. This can be used to navigate the markdown files and view the _compiled_ result.

Within this interface some save buttons exist to help view-users press go.


## Command Line Publish

Generally the tool can be a `compile` command, reading a pre markdown directory and compiling to a markdown directory.

    tool publish md
    tool compile [output-dir]

Alternatively the `publish html` command produces a rendered version of the markdown as flat html files. This includes any general _site wrapper_.

---

## General Watch Tool

Refreshing the local vew presents the re-compiled pages