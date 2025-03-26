# Django Trim

> Django Trim shortcuts all the boilerplate for some of those daily django parts. Reduce the amount of written text and trim your code for easier reading, faster prototyping, and less typing.

Django Trim reduces the amount of text, imports and general congantive overload of microtasks when plugging together a django app in it's initial stages.

+ Less typed text, same functionality
+ clear, predicable functional naming
+ Leverage conventions for faster prototyping
+ 100% compatible with existing django components.

## Trim

+ [Models](./models)
    + [Auto Model Mixin](./models/auto_model_mixin.md): Bridge models across apps automatically
    + [Fields](./models/fields.md): Functional model field names
    + [Live Models](./models/live.md): Utilise any model, with one import
+ [Views](./views)
    + [Authed Views](./views/authed-views.md): Fast mixing for user authentication
    + [Markdown](./markdown.md): Markdown template views, and responses classes
+ [Forms](./forms)
    + [Quick Forms](./forms/quickforms.md): Apply your prepared form on any view
    + [Hidden Widget](./widgets/hidden.md): easily apply _hidden_ to form fields
+ [URLs](./urls): less typing for includes and patterns
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
        + [markdown](./markdown.md): Template tags for rendering Markdown in the view
+ Apps
    + [Live Import](./apps.md): Live import special named files across all apps at _boot-time_
+ Execute
    + [`read_one_stream_command`](./execute.md): Read tricky byte pipes with one-bit stream reader (not django specific)