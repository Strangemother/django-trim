# DateTime Template Tags

Calculate and display time differences in human-readable format.

## Overview

The datetime template tags provide convenient ways to calculate and display time differences between datetime objects. These tags are particularly useful for showing durations, elapsed time, or time remaining in a user-friendly format.

## Tags

### `{% timedelta %}`

Calculate the time difference between two datetime objects, returning a Python `timedelta` object.

### `{% human_timedelta %}`

Calculate the time difference and format it as a human-readable, localized string with automatic pluralization.

## Usage

```django
{% load datetime %}

<!-- Get timedelta object -->
{% timedelta end_time start_time %}

<!-- Get human-readable string -->
{% human_timedelta end_time start_time %}
```

## `{% timedelta %}` - Raw Duration

Returns a Python `timedelta` object for programmatic use.

### Basic Usage

```django
{% load datetime %}

<!-- Calculate duration -->
{% timedelta order.completed order.created %}
<!-- Output: datetime.timedelta(days=2, seconds=13512) -->

<!-- Store for later use -->
{% timedelta event.end event.start as duration %}
<p>Event lasted {{ duration }}</p>
```

### Using with Conditionals

```django
{% load datetime %}

{% timedelta cart.updated cart.created as cart_age %}
{% if cart_age.days > 7 %}
    <div class="alert">Your cart is over a week old!</div>
{% elif cart_age.days > 1 %}
    <div class="notice">Your cart is {{ cart_age.days }} days old</div>
{% endif %}
```

### Accessing Timedelta Properties

```django
{% load datetime %}

{% timedelta project.completed project.started as duration %}
<div class="project-stats">
    <p>Days: {{ duration.days }}</p>
    <p>Seconds: {{ duration.seconds }}</p>
    <p>Total seconds: {{ duration.total_seconds }}</p>
</div>
```

## `{% human_timedelta %}` - Human-Readable Duration

Formats time differences as readable text with automatic pluralization and localization.

### Basic Usage

```django
{% load datetime %}

<!-- Simple duration display -->
{% human_timedelta order.shipped order.created %}
<!-- Output: "2 days 3 hours 15 minutes" -->

<!-- With context -->
<p>Processing time: {% human_timedelta order.completed order.created %}</p>
<!-- Output: "Processing time: 1 day 6 hours 30 minutes" -->
```

### Common Patterns

#### Show Time Ago

```django
{% load datetime %}

<p>Last updated: {% human_timedelta now item.updated %} ago</p>
<!-- Output: "Last updated: 3 hours 22 minutes ago" -->

<p>Posted {% human_timedelta now post.created %} ago</p>
<!-- Output: "Posted 2 days 5 hours ago" -->
```

#### Order Processing Time

```django
{% load datetime %}

<div class="order-timeline">
    <div class="stage">
        <strong>Order Placed:</strong> {{ order.created }}
    </div>
    <div class="stage">
        <strong>Processing Time:</strong> 
        {% human_timedelta order.shipped order.created %}
    </div>
    <div class="stage">
        <strong>Delivery Time:</strong> 
        {% human_timedelta order.delivered order.shipped %}
    </div>
    <div class="total">
        <strong>Total Time:</strong> 
        {% human_timedelta order.delivered order.created %}
    </div>
</div>
```

#### Session Duration

```django
{% load datetime %}

<div class="session-info">
    <h3>User Session</h3>
    <p>Duration: {% human_timedelta session.end session.start %}</p>
    <p>Started: {{ session.start }}</p>
    <p>Ended: {{ session.end }}</p>
</div>
```

#### Project Timeline

```django
{% load datetime %}

<div class="project-card">
    <h4>{{ project.name }}</h4>
    <div class="timeline">
        {% if project.completed %}
            <span class="duration">
                Completed in {% human_timedelta project.completed project.started %}
            </span>
        {% else %}
            <span class="in-progress">
                In progress for {% human_timedelta now project.started %}
            </span>
        {% endif %}
    </div>
</div>
```

## Format Output

The `human_timedelta` tag produces output in the following format:

- **Years**: `"1 year"` or `"2 years"`
- **Days**: `"1 day"` or `"5 days"`
- **Hours**: `"1 hour"` or `"3 hours"`
- **Minutes**: `"1 minute"` or `"45 minutes"` (shown if duration >= 1 minute)
- **Seconds**: `"1 second"` or `"30 seconds"` (shown if duration < 1 minute)

### Examples of Output

```python
# 400 days, 2 hours, 2 minutes
"1 year 35 days 2 hours 2 minutes"

# 45 seconds
"45 seconds"

# 1 day, 2 hours, 30 minutes
"1 day 2 hours 30 minutes"

# 3 hours only
"3 hours"

# Just minutes
"15 minutes"
```

## Comparison with Django's Built-in Tags

### `timesince` Filter

Django's built-in `timesince` filter provides similar functionality:

```django
<!-- Django's timesince -->
{{ cart.created|timesince:cart.updated }}
<!-- Output: "2 days, 3 hours" (approximate) -->

<!-- Trim's human_timedelta -->
{% human_timedelta cart.updated cart.created %}
<!-- Output: "2 days 3 hours 15 minutes" (more precise) -->
```

**Differences:**
- `timesince`: More concise, shows only 2 levels (e.g., "2 days, 3 hours")
- `human_timedelta`: Shows all relevant time components for full precision

### `timeuntil` Filter

For future dates, use Django's `timeuntil`:

```django
<!-- Django's timeuntil -->
{{ event.start|timeuntil }}
<!-- Output: "2 days, 3 hours" (until future event) -->

<!-- Trim's alternative (if event.start is in future) -->
{% human_timedelta event.start now %}
<!-- Output: Shows duration (may be negative if comparing past to present) -->
```

## Localization

The `human_timedelta` tag uses Django's `ngettext` for proper pluralization and localization support. The output will automatically adjust based on your Django language settings:

```python
# English
"1 day 2 hours 3 minutes"

# Spanish (with proper translation files)
"1 día 2 horas 3 minutos"

# French
"1 jour 2 heures 3 minutes"
```

## Complete Examples

### Shopping Cart Age Indicator

```django
{% load datetime %}

{% timedelta now cart.created as age %}
<div class="cart-header">
    <h2>Your Shopping Cart</h2>
    <div class="cart-age">
        {% if age.days >= 30 %}
            <span class="warning">
                ⚠️ Items may have changed. Cart is {% human_timedelta now cart.created %} old.
            </span>
        {% elif age.days >= 7 %}
            <span class="notice">
                Cart created {% human_timedelta now cart.created %} ago
            </span>
        {% else %}
            <span class="fresh">
                Cart is fresh ({% human_timedelta now cart.created %} old)
            </span>
        {% endif %}
    </div>
</div>
```

### Task Completion Dashboard

```django
{% load datetime %}

<div class="tasks-dashboard">
    {% for task in completed_tasks %}
        <div class="task-card">
            <h3>{{ task.title }}</h3>
            <div class="task-meta">
                <span class="started">{{ task.started|date:"M d, Y" }}</span>
                <span class="duration">
                    <strong>Duration:</strong>
                    {% human_timedelta task.completed task.started %}
                </span>
                <span class="completed">{{ task.completed|date:"M d, Y" }}</span>
            </div>
            {% timedelta task.completed task.started as duration %}
            {% if duration.days > 7 %}
                <span class="badge long-task">Long Task</span>
            {% elif duration.days > 1 %}
                <span class="badge medium-task">Multi-Day</span>
            {% else %}
                <span class="badge quick-task">Quick Task</span>
            {% endif %}
        </div>
    {% endfor %}
</div>
```

### Event Countdown/Duration

```django
{% load datetime %}

<div class="event-timer">
    {% if event.start > now %}
        <!-- Event hasn't started -->
        <h3>Event Starts In:</h3>
        <p class="countdown">{% human_timedelta event.start now %}</p>
    {% elif event.end > now %}
        <!-- Event is ongoing -->
        <h3>Event In Progress</h3>
        <p>Running for: {% human_timedelta now event.start %}</p>
        <p>Ends in: {% human_timedelta event.end now %}</p>
    {% else %}
        <!-- Event has ended -->
        <h3>Event Completed</h3>
        <p>Duration: {% human_timedelta event.end event.start %}</p>
        <p>Ended: {% human_timedelta now event.end %} ago</p>
    {% endif %}
</div>
```

## Implementation Notes

### Year Calculation

Years are approximated as 365 days and do not account for leap years. For more precise year calculations, consider using `dateutil` or custom logic in your views.

### Precision

- `timedelta`: Returns exact Python `timedelta` object
- `human_timedelta`: Shows years, days, hours, and either minutes OR seconds (not both)

### Negative Durations

Both tags handle negative durations (when `early_time > late_time`), but the output may not be intuitive. Ensure proper argument order:

```django
<!-- Correct order: later time first, earlier time second -->
{% timedelta order.completed order.created %}  ✓

<!-- Incorrect order: will produce negative duration -->
{% timedelta order.created order.completed %}  ✗
```

## Reference Implementation

Source: `trim.templatetags.datetime`

```python
@register.simple_tag(takes_context=False, name='timedelta')
def timedelta_tag(late_time, early_time, *targs, **kwargs):
    """Calculate the time difference between two datetime objects."""
    td = (late_time - early_time)
    return td

@register.simple_tag(takes_context=False, name='human_timedelta')
def str_timedelta_tag(late_time, early_time, *targs, **kwargs):
    """Calculate time difference and format in human-readable text."""
    td = (late_time - early_time)
    return localize_timedelta(td)

def localize_timedelta(delta):
    """Convert timedelta to human-readable localized string."""
    # ... implementation with ngettext for pluralization
```

## Related

- [Django's timesince filter](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#timesince)
- [Django's timeuntil filter](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#timeuntil)
- [Python timedelta documentation](https://docs.python.org/3/library/datetime.html#timedelta-objects)
- [`{% functional %}` tag](./functional.md) - For calling datetime functions
- [Django i18n documentation](https://docs.djangoproject.com/en/stable/topics/i18n/)
