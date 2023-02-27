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
