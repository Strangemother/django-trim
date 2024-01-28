# Toggle Link

> Create a link to toggle a class on a target Using JS


## Usage

Include this JS Asset in your HTML code:

```jinja
{% static "js/toggle-links.js" %}
```

Apply HTML assignments:

```html
<a data-target='foo-bar'>Click to toggle</a>

<div data-name='foo-bar'>
    toggled content.
</div>
```


The data-attributes:

    1. add `data-name` to a target
    2. add `data-target` to the clickable

The css class "toggle-show" "toggle-hidden" are switched per click.

## Groups

Optional add "data-group" to the clickable, for an _untoggle_ of all relatives.

## CSS

Use CSS to Toggle the visibility of the panel:

```js
.toggle-hidden {
    display: none;
}

a.toggle-link {
    text-decoration: none;
}

a.toggle-link.toggle-selected {
    text-decoration: underline;
}
```