# Getting Started

The goal of this tool is _out of the way compilation_, where you write you "dev docs/" and this _compiles_ your pre-markdown to your markdown folder.

The output folder (your target) is your final location, e.g. your projects standard `docs/` folder

{% insert "./getting-started/how-does-it-work.md" %}{% endinsert %}

## Example

Your markdown file contains standard markdown plus any template vars:

{% verbatim %}
```md
### Content Example

Perhaps a bit of lorem: `{% lorem w random %}`
```
{% endverbatim %}

Of which results in:


### Content Example

Perhaps a bit of lorem: `{% lorem w random %}`

---

## Setup

The initial setup is easy - the tool is designed to be _out of the way_

1. Grab the package
2. Run it in your `md-1/` directory, with a target output directory (e.g `docs/`)

## Running

A few builtin flavours exist for running the tool:

+ current working dir: Run in the output directory
+ YAML Config: run the tool relative to a `.doc-config.yaml` file


### Current Working Directory

Run the app within the target directory - You can edit the neighouring files.

    - root/
        - myapp.js
        - bin/
        - docs/
            - readme.md
            - other.md

            * $ ./tool-admin serve # run-here...

like this:

```bash
/user/apps/root/docs/ $ tool-admin serve
```

### YAML File Pointer

A more stable routine is a `.doc-config.yaml` in the favourite place, such as the root of your project:


    - root/
        - myapp.js
        - bin/
        - docs/
            - readme.md
            - other.md
        - .doc-config.yaml
        * $ ./tool-admin serve # run-here using .doc-config.yaml



### Editing what `docs/`?

If preferred you can run `tool` within the target `docs` directory:

    - root/
        - myapp.js
        - bin/
        - docs/
            - .doc-config.yaml
            - readme.md
            - other.md
            * $ ./tool-admin serve # run-here...

This will work and you can choose an output directory. **However** It's more likely you will want your _output directory_ as your `docs/` folder, therefore consider a _pre-docs_ setup.

This ensures you edit files outside your _output directory_ (if the output dir is `docs/`):


    - root/
        - myapp.js
        - bin/
        - docs/
            - readme.md
            - other.md
        - docs-1/
            - .doc-config.yaml
            - readme.md
            - other.md
            * $ ./tool-admin serve


## Usage



## What does it Do?

+ Write markdown
+ Write complex addons and shared components
+ Use as a markdown editor, compiler, or publisher
+ Serve as a markdown, static site, or a django site
+ Write custom components
    + Tags, Includes, Views
+ And with an entire eco-system for free!


