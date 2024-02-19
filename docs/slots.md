# Wraps and slots

A fragment

```html
    <div class="content">
        <div class="left">
            {{ wrap.content }}
        </div>
        <div class="right">
            not accessible
        </div>
    </div>
```

A wrap

    {% wrap "fragment.html" %}
            <p>content</p>
    {% endwrap %}

The result

    <div class="content">
        <div class="left">
            <p>content</p>
        </div>
        <div class="right">
            not accessible
        </div>
    </div>

## slots

A fragment

    <div class="content">
        <div class="left">
            {% slot "left" default %}placeholder{% endslot %}
        </div>
        <div class="right">
            {% slot "right" %}is accessible now{% endslot %}
        </div>
    </div>

Usage

    {% wrap "fragment.html" %}
        {% slot "left" %}
            <p>content</p>
        {% endslot %}
        {% slot "right" %}
            <p>more content</p>
        {% endslot %}
    {% endwrap %}

or

    {% wrap "fragment.html" %}
        {% slot %}
            <p>content</p>
        {% endslot %}
        {% slot "right" %}
            <p>more content</p>
        {% endslot %}
    {% endwrap %}

### Defaults

No slots automatically uses the default.

    {% wrap "fragment.html" %}
        <p>content</p>
    {% endwrap %}

Is the same as:

    {% wrap "fragment.html" %}
        {% slot "left" %}
            <p>content</p>
        {% endslot %}
    {% endwrap %}

Or even

    {% wrap "fragment.html" %}
        {% slot %}
            <p>content</p>
        {% endslot %}
    {% endwrap %}

But is always:

    {% wrap "fragment.html" %}
        <p>content</p>
    {% endwrap %}

---

+ Anything outside a slot definition is applied to the default slot

    {% wrap "fragment.html" %}

        {% slot "right" %}<p>right content</p>{% endslot %}
        <p>will become left</p>

    {% endwrap %}

+ Content outside a slot when the default slot is defined, is lost

    {% wrap "fragment.html" %}

        {% slot "right" %}<p>right content</p>{% endslot %}
        {% slot default %}<p>left content</p>{% endslot %}
        <p>will not be rendered</p>

    {% endwrap %}

+ Apply a _lost_ slot to capture anything unexpected

    frangement:

        {% wrap "fragment.html" %}
            {% slot %}
                <p>content</p>
            {% endslot %}
            {% slot "right" %}
                <p>more content</p>
            {% endslot %}

            {% slot lost %}
                <p>more content</p>
            {% endslot %}
        {% endwrap %}

    wrap:

        {% wrap "fragment.html" %}
            {% slot "right" %}<p>right content</p>{% endslot %}
            {% slot default %}<p>left content</p>{% endslot %}
            <p>rendered in "lost"</p>
        {% endwrap %}


===

## Development Notes

2024-02-18 21:05:37.039 | DEBUG    | trim.templatetags.trim:render:147 - DefineSlotNode, self.tokens=['extras']
[18/Feb/2024 21:05:37] "GET / HTTP/1.1" 200 16924


      do_wrap:64 -    _def_ do wrap
      __init__:72 -   _def_ new SlotList
      __init__:173 -  _cre_ SlotNode, ['"home-a"'] () {}
      do_slot:126 -   _dis_ "slot" discovered parent (wrap)
      __init__:173 -  _cre_ SlotNode, ['extras'] () {}
      do_slot:126 -   _dis_ "slot" discovered parent (wrap)
      __init__:85 -   _cre_ __init__ wrap

    . render:93 -     _ren_ Wrap node rendering template with:  <SlotList 2 slots>
      __init__:142 -  _cre_ DefineSlotNode, ['default'] () {}
      __init__:142 -  _cre_ DefineSlotNode, ['extras'] () {}
    * render:178 -    _ren_ SlotNode, ['"home-a"']
      render:178 -    _ren_ SlotNode, ['extras']
      render:147 -    _ren_ DefineSlotNode, ['default']
      render:147 -    _ren_ DefineSlotNode, ['extras']

When cached: .. \*

    render:93 -     _ren_ Wrap node rendering template with:  <SlotList 2 slots>
    render:178 -    _ren_ SlotNode, ['"home-a"']
    render:178 -    _ren_ SlotNode, ['extras']
    render:147 -    _ren_ DefineSlotNode, ['default']
    render:147 -    _ren_ DefineSlotNode, ['extras']


---

# Rules


A slot with no name is a `default` slot

```jinja
{% wrap 'foo.html' %}
    {% slot %}
        an unnamed slot is a "default slot"
    {% endslot %}
{% endwrap %}
```

---

## lost slots

Content outside of any slot is considered "lost".
Lost content will go to the `lost`, then `default` definition,
if each is not defined in sequence.


```jinja
{% wrap 'foo.html' %}
    This is lost content
{% endwrap %}
```

Definition

```jinja
{% slot.define "lost" %}
    replacable lost content slot
{% endslot %}
```

---

## default keyword vs "default" string

The `default` keyword should be an none-string allowing the
user to define another `"default"`


```jinja
{% slot default %}
    The default keyword is not a string.
{% endslot %}
```
```jinja
{% slot "default" %}
    A string locates the string name "default", not the key
    `default`
{% endslot %}
```

---

## lost keyword

"Lost" content has the same style of definition as `default`

+ it's a keyword type
+ It accepts all fallout data
+ Is optional
+ Can be a multi slot


```jinja
{% slot.define default lost %}
    This slot is both the default and lost
{% endslot %}
```

All content heads there:

```jinja
{% wrap "foo.html" %}

    This lost content is push to the lost slot.

    {% slot default %}
        Default content is pushed to the lost slot.
    {% endslot %}

{% endwrap %}
```

Note: I'm not sure how node order is applied here...

---

## slot names (mutiple)

A slot can apply many names, with fallback positions

```jinja
{% slot "primary-place" "extras" default %}
    <div class='color-green'>
    (wrap) for slot default
    </div>
{% endslot %}
```

A slot.definition can be a multi-slot


```jinja
{% slot.definition "extras" default lost %}
    a slot for "extras", default and lost content.
{% endslot %}
```