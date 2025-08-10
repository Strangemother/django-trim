# It's Just Markdown!

Markdown is great so there's no point trying to replace it. This doc tool presents _just markdown_, and can render generally any markdown file.


## ... With Extras

This tool may be considered a _pre markdown_ step. Allowing the inclusion of complex addons - using another beautiful syntax, mustache templating.

> It's just markdown with a sprinkling of pre-step extras.


## Why not produce "addon X"?

I absolutely love markdown and use it for a lot of doc writing. However as a web developer this assigns some limitations I'm not used-to. Attempting to "DRY" markdown with extent addons still mandated an extended backend or _pre-markdown compilation_, so I can push the docs to a cloud provider or some other app.

These apps include:

+ Hugo
+ Github / Bitbucket
+ Markdown Editor, VSCode, Sublime,
+ Anything in a directory

As each one _compiles_ markdown in a different manner, the only solution is a _pre-step_ I can manipulate myself...


### Enter Django

As I'm a python dev; I love Django and thus by creating a template response of which reads _a target directory_ I immediately render markdown - with **all the benifits** of the django eco-system.

Using a simple web app renderer, django allows an unparalleled level of abstraction. The syntax can be easily switch to jinja - but I opted for nice clean standard `{% verbatim %}{% template tags %}{% endverbatim %}`

And voila! Auto DRY. Plus all of djangos backend!


## Caveats and Limitations

As we can see the bonuses are great. A pre-step compiler, a potential builtin editor and it'll work on any HTML or MD.

The only minor irritation is reduction of textually applying template includes: `{% verbatim %}{%  %}{% endverbatim %}` in markdown breaks the extern renderer.

As a solution we use Django standard `{% templatetag openblock %} verbatim %}{% templatetag openblock %}  %}{% templatetag openblock %} endverbatim %}` syntax. But this isn't as easy as just throwing `{% verbatim %}{%  %}{% endverbatim %}`  into the md file.

The same issue with `{% verbatim %}{{ mustache }}{% endverbatim %}` templating.