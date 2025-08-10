# trim-docs

A method to convert "partial" or pre-markdown into fully formatted markdown.

**TL:DR;**

I want to be able to write markdown files, with django addons, press save and push to github.
This is because I want automated _TOCs_, thumbnailing, file references and custom rendering bits (that are DRY) 

This same content should be useful for django (normal pages), Hugo, github pages, the _docs/_ directory. All of them render slightly differently, so a _frame_ is needed to wrap the content for any destination.

This should be easy to use:

```python
INSTALLED_APPS = [
    ...
    'trimdocs',
]

TRIM_DOCS = {
    'srcdocs': 'srcdocs',
}
```

When compiling:

```bash
# minimal example
python manage.py trimdoc compile . 
python manage.py trimdoc compile --dest docs/
# or with output format
python manage.py trimdoc compile --dest hugo/src/ --frame hugo 
python manage.py trimdoc compile --dest .pages/ --frame github-pages 
```

## Reasoning

When working with markdown I'd like to use jinja templating - such as includes and _image_ tags.
In addition I wanted to be able to compile the markdown, or review it in the browser during dev. 
There's no reason why Django can't do that. And with the bonus of using the same stack as the project.

### Easy to Use

This should be a fire-and-forget solution to convert markdown files into fully formatted markdown. The developer can work in a _srcdocs_ directory, and the output will be in a _docs_ directory.

Fundamentally if the developer wants to ignore the tool, they're writing pure markdown. 
Personally I want to be able to write markdown, and then use django templating to perform hard parts (e.g. image include with thumbnailing), but I still want _just markdown_.

---

The output can be markdown (default), browser viewable HTML, or compiled into an alternative format.
The destination is key, such as github docs, Hugo docs, or github pages etc.

For this the doc tool should allow _rendering_ markdown, with a _frame_ for the output. 
This frame can be changed per compilation. 


## Usage

The tool can be used as a command line utility or as a Django app.

+ PY name: `django-trim[docs]`
+ Django app: `trimdocs`
+ Command line utility: `trim-docs`, maybe also `trimdocs`
+ Django command: `python manage.py trimdocs compile`

### Command Line

```bash
trim-docs --srcdocs srcdocs --destdocs docs --destformat markdown
```

Notes on the command line usage:

This needs django, therefore a _headless_ option may be required. I feel piping to the manage.py command is the best way to do this.


## Key Features

Things I want to be able to do with this tool:

+ Links: Easier to link to other markdown files, images, or external resources.
+ Includes: Ability to include other markdown files or templates within the main markdown file.
+ Image Tags: Support for image tags that can be processed and rendered correctly.
+ Frame: Ability to wrap the rendered markdown in a frame, which can include headers, footers, and other HTML structures.
+ Render: Convert markdown files into fully formatted markdown or HTML files.

### Core Functionality

+ Markdown to Markdown 
+ Markdown, with a "frame" (for browser or HTML flats)
+ Compile feature for flat result
+ Command line interface (django command)
+ Django app for easy integration

Then:

+ Plugin system for extending functionality
+ Configuration through Django settings or command line arguments

Plugins through:

+ Django template tags and filters
+ Functional procedures (e.g., parsing files, extracting methods)
+ Overridable views for custom processing

## Builtin Features

+ `TOC` tag: Generates a Table of Contents for the markdown file - or another directory
+ `Image` tag: Processes image tags to include images with optional thumbnailing
+ `Include` tag: Allows including other markdown files or templates within the main markdown file
+ `Link` tag: Simplifies linking to other markdown files, images, or external resources
+ `Frame` tag: Wraps the rendered markdown in a specified frame, which can include headers, footers, and other HTML structures
+ `Render` tag: Converts markdown files into fully formatted markdown or HTML files

---

Finally, versioning is important. However I haven't quite solved that yet. I feel it'll mostly involve a unique _output_ when generating the result, this is managed by the user. The django view can have a UI variable, allowing the user to select a version (pointing the source to a altertive directory).

### Building Plugins

I want to be able to build plugins that can extend the functionality of this tool.
A Plugin will mostly be django template tags and filters. But there's no reason why have can have functional procedures, such as _parse a file and get all the methods_.

For this the Django _view_ of a file should be overloadable. I think the django app (`trim_docs`) should have a default view that can be overridden by plugins.

## Configuration

The configuration for the tool can be done through a settings file or command line arguments. Key configurations include. 

Django settings seems a great place to put the configuration, as it allows for easy overrides and extensions. These settings can be overridden on the cli, and some in the markdown file itself (e.g. the frame).

### Frame

The frame is a template that wraps the rendered markdown content. It can be specified in the configuration or passed as an argument to the render function. The frame can include headers, footers, and any other HTML structure needed for the output.


### Example Usage
To render a markdown file with a specific frame, you can use the following command:

```bash
trim-docs --srcdocs srcdocs --destdocs docs --destformat html --frame default
``` 

This will take the markdown file from the `srcdocs` directory, process it, and save the output in the `docs` directory using the specified frame.


### Output

The output will be a fully formatted markdown file or HTML file, depending on the specified format.
The processed files will be ready for use in documentation, websites, or any other platform that supports markdown or HTML.


---

## Notes on Implementation

+ It seems prudent to ignore anything with a leading underscore, such as `_file.md` or `_dir/`.
    + But can be referenced in the markdown.
    + Can be exposed in the meta data with `expose:true` in the front matter.
        + Exposure should always be explicit. So every parent should have `expose: true`. 
+ Links are relative to the source directory, so they can be used in the markdown files.
    + e.g. `[Link](./file.md)` will link to `srcdocs/file.md`.
+ Will naturally read the `docs/` directory 
+ The tool should be able to handle nested directories, so `srcdocs/dir/file.md` will be processed correctly.
+ Automated `_contents.md` generation 
    + This will be a file that contains the Table of Contents for the directory.
    + It can be generated automatically or manually.
+ `_index.md` can override default `readme.md` 
+ An _internal_ endpoint can be with our without the `.md` extension.
+ A file or directory can be bound to a django view:

    ```markdown
    ---
    view: trimdocs.views.MarkdownView
    ---
    ```
+ global indicies file: `_incidies.md`
    + This file can be used to generate a global index for the documentation.
    + It can include links to all the files in the `srcdocs` directory.
    + It can be generated automatically or manually.

Notes on a readme

A readme file is special. A directory expectes a `readme.md` file. If it doesn't exist, it will look for `_index.md` or `_contents.md`.

+ readme.md 
+ _index.md

If they dont exist, a readme will be generated with the contents of the directory.




## View Tagging

A markdown file can be tagged with a view, which allows for custom processing of the file.
However, sometimes a view is needed, of which isn't a markdown file such as an index or contents file. 




## Future Enhancements

My primary wish is to be able to have _one_ `docs/` I edit, and the tool can reparse the result.
I feel it can be done with clever import referencing in the final markdown.

For example, if I had a file with the following

```markdown
Some content

{% TOC . %}

Let's get started ... 
```

This should generate the file, But also allow me to edit the file, and the TOC will be updated automatically.

To perform this without severe magic, we can pepper the result with a `<!-- trim-docs: toc -->` comment, which can be used to identify the TOC location.

Output (Also `docs/myfile.md`):

```markdown
Some content

<!-- trimdocs: <$ TOC . $> as 0x2093f3 -->
- [Let's get started](#lets-get-started)
<!-- endtrimdocs: 0x2093f3 -->

Let's get started ... 
```

This way, the tool can detect the TOC location, and resuse the command within the comment. The placeholders within `<$ TOC . $>` can be anything - but I feel `{% .. %}` is stressful for accidental parsing.

### How will it work?

I think two ways:

1. A regex parser, to undo the changes before parsing. 
2. A django template node designed for this custom language. 
    + Capturing the comment, parsing the partial, then returning the rendered result.
    + And replace the existing. 
3. The _key_ is a unique identifier, but also a hash of the content. This way, if the content changes, the identifier will change, and the tool can detect it.

The tool can also detect the `<!-- trim-docs: ... -->` comment, and replace it with the rendered result.
Therefore a user can opt for the partials instead. 

something like this:

```markdown
Some content

<!-- trimdocs TOC . -->

Let's get started ... 
```

