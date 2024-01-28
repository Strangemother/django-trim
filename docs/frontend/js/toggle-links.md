# Toggle Link

> Create a link to toggle a class on a target Using JS

In many cases, _tabs_ and _panels_ may be simplified to toggling a class on the selected item. When our _clickable_ is activated, the `toggle-show` and `toggle-hidden` classs are cycled on the target.

Applying a _group_ will hide all targets when one clicker is clicked.

1. Install the static `js/toggle-links.js`
2. A `data-target="my-target"` to the clicker
3. Add `data-name='foo-bar'` to the target item
4. Click you `data-target` item
5. The `data-name` element class changes

## Usage

Include this JS Asset in your HTML code:

```jinja
{% static "js/toggle-links.js" %}
```

Apply HTML assignments:

1. add `data-name` to a target
2. add `data-target` to the clickable

The name `my-target` can be any unique name.

```html
<a data-target='foo-bar'>Click to toggle</a>

<div data-name='foo-bar'>
    toggled content.
</div>
```

And that's it! Click the `data-target` item and the `data-name` element class will change.

The css class "toggle-show" "toggle-hidden" are switched per click.

## Groups

> Optional add "data-group" to the clickable, for an _untoggle_ of all relatives.

1. Add `data-group='somename'` for every item in the group


```html
<a data-group="baz" data-target='foo-bar'>Click to toggle</a>
<a data-group="baz" data-target='another-foo'>Click to toggle</a>

<div data-name='foo-bar'>
    toggled content.
</div>

<div data-name='another-foo'>
    toggled content.
</div>
```


## CSS

Here's some CSS to toggle the visibility of a panel:

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