# `slot` Tag

Use the `{% slot [name] %}` tag to push content into the `{% slot.define [name] %}` within a `{% wrap %}`.



<table>
<thead><tr>
  <th align="left">Define</th>
  <th align="left">Use</th>
</tr></thead>
<tbody>
<tr valign="top">
<td>

Within the [wrap tag](./wrap.md), we can define placeholders with `{% slot.define name %}{% endslot %}`.

Within the
```jinja
<!-- filename `wraps/hero-header.html` -->
{% load slot %}

<div class='hero-header'>
    <header>
        {% slot.define "title" %}
            <h1>Spoons?</h1>
        {% endslot %}
    </header>
    {% slot.define default %}
        <p>Default slot content</p>
    {% endslot %}
</div>
```

</td>
<td>

When implementing the _wrap_, we can opt to use the slots:

```jinja2
<!-- filename `home.html` -->
{% load wrap %}

{% wrap "wraps/hero-header.html" %}
    {% slot "title" %}
        <h1>Sugar not Shugar?</h1>
    {% endslot %}
    {% slot %}
        <p>Alternative HTML</p>
    {% endslot %}
{% endwrap %}
```

</td>
</tr>
<tr>

</tr>
</tbody></table>


Take a look at [the wrap tag](./wrap.md) to implement slots

## Usage

A wrap accepts slots when applied. The slot name is the same as the target sibling `slot.define`. Within a slot we can apply any HTML:

```jinja2
<!-- filename `home.html` -->
{% load wrap %}

{% wrap "wraps/hero-header.html" %}
    {% slot "title" %}<h1>Sugar not Shugar?</h1>{% endslot %}
    {% slot %}<p>Alternative HTML</p>{% endslot %}
{% endwrap %}
```


A `{% slot.define %}` defines a position within a target `{% wrap %}` as a placeholder for user content. Multiple optional slots may be defined within the wrap template:


```jinja
<!-- filename `wraps/hero-header.html` -->
{% load slot %}

<div class='hero-header'>
    <header>
        {% slot.define "title" %} <!-- Define the "title" slot -->
            <h1>Spoons?</h1>
        {% endslot %}
    </header>

    <div class='split-50-50'>
        {% slot.define default %} <!-- The _default_ slot -->
            <p>Default slot content</p>
        {% endslot %}

        <div class="right-image"><img src="hero.png"></div>
    </div>
</div>
```

## Define Slots

Our wrap template is the target to import. Within this target we can add `{% slot.define named %}` definitions:

```jinja
<!-- filename `wraps/hero-header.html` -->
{% load slot %}

<div class='hero-header'>
    <header>
        {% slot.define "title" %}
            <h1>Spoons Can Run?</h1>
        {% endslot %}
    </header>
    <div class='split-50-50'>

        {% slot.define default %}
            <p>The question is <em>how</em>
               did the spoon run off with the fork?</p>
        {% endslot %}

        <div class="right-image"><img src="hero.png"></div>
    </div>
</div>
```

The `default` name is a keyword and not a string

    default != "default"

### Wrap Usage

When implementing this wrap we can use it as normal without `slot` tags:

```jinja2
<!-- filename `homepage.html` -->
{% load wrap %}

{% wrap "wraps/hero-header.html" %}
    <p>Replace the default content with alternative HTML</p>
{% endwrap %}
```

Or we can target our slots:

```jinja2
<!-- filename `homepage.html` -->
{% load wrap %}

{% wrap "wraps/hero-header.html" %}
    {% slot "title" %}<h1>Milk?</h1>{% endslot %}
    {% slot %}<p>Replace the default content with alternative HTML</p>{% endslot %}
{% endwrap %}
```

Notice within the wrap we use `slot` (not `slot.define`).

### Result

The output HTML collapses `slot` or `slot.define` placeholders:

```jinja
<!-- View Wrap; for the header -->
<div class='hero-header'>
    <header>
        <h1>Milk</h1>
    </header>
    <div class='split-50-50'>
        <!-- default content replaced -->
        <p>Replace the default content with alternative HTML</p>

        <div class="right-image">
            <img src="hero.png">
        </div>
    </div>
</div>
```


## Implement

Slots define areas within the _target_ wrap template, to override when importing.

+ We can implement as many slots as required
+ Slots can be _named_ or a `default`
+ Within the `wrap` we use the `slot` tag
+ Within the template we create `slot.define` areas

When implementing a slot, we _define_ its placement ready for override. This can be _named_ or _unnamed_. If unnamed it becomes the `default`.

### Default Slot Definition

The `default` slot defines the _general_ placeholder used when the wrap does not use any `slot` tags, or uses a `slot` tag without a name. Notice `default` (keyword) not `"default"` (string);

```jinja
<!-- Wrap Template `wraps/target.html` -->
{% load slot %}
<div>
    <!-- Define fields to override. -->
    {% slot.define default %}
        Default HTML Content
    {% endslot %}
    <p>Not slotted content.</p>
</div>
```

We can access this `default` slot without using any `{% slot %}` tags:

```jinja2
<!-- view template `homepage.html` -->
{% load wrap %}

{% wrap "wraps/target.html" %}
    <p>Replace the default content with alternative HTML, no slots needed.</p>
{% endwrap %}
```

Use `{% slot %}` when importing or calling the wrap template. Tags: `{% slot %}`, `{% slot default %}`, and  _no slots_, are treated as the same _default_ placeholder:

```jinja2
{% load wrap slot %}

{% wrap "wraps/target.html" %}
    {% slot %}
        <p>Replace the default content with alternative HTML,
        no slot names needed.</p>
    {% endslot %}
{% endwrap %}
```

### Named Slots

A wrap template can be more complex, applying multiple optional placeholders to override. For example we can build a product card with many overrides:

+ We can include standard django, such as `{{ object }}` access
+ `slot.define` can have multiple names
+ Slot names are `"strings"` (because they can be variables)

_wraps/product-card.html_
```jinja
{% load slot %}
<div class='product card'>
    <header>
        <h1>{% slot.define "title" %}{{ object.name }}{% endslot %}</h1>

        <div>{% slot.define "header" %}
            <!-- nothing by default -->
        {% endslot %}</div>
    </header>
    <div class='content flex-across'>
        <div>
        {% slot.define "content" default %} <!-- both "content" slot or the default -->
            {% if object.desc %}
                {{ object.desc }}
            {% else %}
                <p>Replace Me. Replace Me. Replace me with your typing sticks.</p>
            {% endif %}
        {% endslot %}
        </div>

        <div class="right-image">
            <img src="{{ object.image_src }}">
        </div>
    </div>
</div>
```

When implementing this wrap template, we can choose to override any (or no) slots:

```jinja2
<!-- homepage.html -->
{% load wrap slot %}

{% for item in products.all() %}
    <!-- A wrap acts like an include -->
    {% wrap "wraps/product-card.html" with object=item %}

        {% slot "header" %}
            <ul>
                <li>{{ object.primary_desc }}</li>
                <li>
                    <p>{{ object.info }}</p>
                </li>
            </ul>
        {% endslot %}

        {% slot "content" %}
            <p>Replace the default content with alternative HTML,
            no slot names needed.</p>
        {% endslot %}
    {% endwrap %}

{% endfor %}
```

