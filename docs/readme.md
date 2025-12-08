# Django Trim

> Django Trim shortcuts all the boilerplate for some of those daily django parts. Reduce the amount of written text and trim your code for easier reading, faster prototyping, and less typing.

Django Trim reduces the amount of text, imports and general congantive overload of microtasks when plugging together a django app in it's initial stages.

+ Less typed text, same functionality
+ clear, predicable functional naming
+ Leverage conventions for faster prototyping
+ 100% compatible with existing django components.

## Quick Start

+ [Recipes](./recipes) - Step-by-step guides for building common features
    + [Building a Contact Form](./recipes/basic-page.md) - Complete guide for beginners
    + [Building a ListView](./recipes/listview.md) - Display data in tables

## Trim

+ [Models](./models)
    + [Auto Model Mixin](./models/auto_model_mixin.md): Bridge models across apps automatically
    + [Fields](./models/fields.md): Functional model field names
    + [Live Models](./models/live.md): Utilise any model, with one import
+ [Views](./views)
    + [Authed Views](./views/authed-views.md): Fast mixing for user authentication
    + [Markdown](./markdown.md): Markdown template views, and responses classes
+ [Forms](./forms)
    + [Form Fields](./forms/fields-auto.md): Complete reference of all form field shortcuts
    + [Quick Forms](./forms/quickforms.md): Apply your prepared form on any view
    + [Hidden Widget](./widgets/hidden.md): easily apply _hidden_ to form fields
+ [URLs](./urls): less typing for includes and patterns
    + [Functions](./urls/functions.md): Comprehensive reference of all URL helper functions
    + [Overview](./urls/readme.md): Getting started with trim URLs
+ [Admin](./admin.md): Register all models in your django admin with one function call.
+ [Templates](./templates)
    + [Theming](./theming/readme.md): Centralise template import names with your own theming package
    + [Tags](./templates/tags)
        + [link](./templates/tags/link/readme.md): Generate `<a>` hyperlinks in the view using view names.
            + [css|js link](./templates/tags/css-js-tag.md): Generate standard _script_ and _stylesheet_ imports using view names.
        + [wrap](./templates/tags/wrap.md): Build HTML fragments (like `{% include %}`), with additional body content
            + [slots](./templates/tags/wrap-slots.md): Extend `{% wrap %}` with _slot_ for multiple body definitions.
        + [quickform](./templates/tags/quickform.md): Use a single view tag to import a ready-to-go `FormView` form.
        + [strings](./templates/tags/strings.md): Utilities for string management within a template.
        + [updated_params](./templates/tags/updated_params.md): Update URL query parameters while preserving existing ones.
        + [functional](./templates/tags/functional.md): Dynamically call any Python function by its fully qualified name.
        + [datetime](./templates/tags/datetime.md): Calculate and display time differences in human-readable format.
        + [markdown](./markdown.md): Template tags for rendering Markdown in the view
+ Apps
    + [Live Import](./apps.md): Live import special named files across all apps at _boot-time_
+ Execute
    + [`read_one_stream_command`](./execute.md): Read tricky byte pipes with one-bit stream reader (not django specific)