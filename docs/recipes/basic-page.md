# Building a Contact Form

A contact form is one of the first things you'll build in Django. Let's use `trim` to create a complete working form with minimal code. This guide covers the essentials: model, form, view, and URL.

> **Prerequisites:** You have Django and `django-trim` installed, with a basic Django project created. Add `'trim'` to your `INSTALLED_APPS`. 
> This guide assumes you're new, but familiar with the basics of Django projects.

If you're new to Django, Hello 👋! If you're experienced with Django, these tutorial may be slower than you prefer, and checking out our [guide for the experienced](./TODO.md), covering the additions rather than a getting-started tutorial.

For you new to Django, this tutorial will walk you through the steps to create a contact form using Django Trim. We'll cover everything from setting up the model to creating the view and URL routing. 

**Note** this is focused on using django-trim to make the process easier, rather than teaching explicit Django itself. If you want to learn Django itself, check out the [official Django tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/) (I'll do my best to keep this aligned with it, but it's not a replacement).

Okay on with making a contact form!

## The Three Core Steps

Every Django feature follows the a similar pattern. In this case we're going _model first_, because "CRUD" is still super common, and django makes that 420 easy.

We will make:

1. **Model** - Define your data structure
2. **View** - Handle the logic and display
3. **URL** - Wire it up so people can access it

It will:

- Display a form for users to fill out
- Validate and save the form data
- Store contact messages in the database
- Show a success page after submission

for free it will also:

- Integrate with Django Admin to view messages
- Super secure form handling with CSRF protection
- Minimal code (seriously!)

Let's build a contact form following this pattern.

---

<details>
<summary>🚀 <strong>Setup: Creating Your Contact App</strong></summary>

In all cases we're building within the `contact` app of your Django project.

To create the app if you haven't already:

```bash
python manage.py startapp contact
```

This is _an app_, designed to be plugged into your larger django project.

Then add it to your `INSTALLED_APPS` in `settings.py`:

```py
INSTALLED_APPS = [
    # ... your other apps
    'trim',
    'contact',
]
```

Now we can populate the important files within the `contact` app.

**Files we'll create/edit:**
```
contact/
├── models.py         # Step 1: Define ContactMessage model
├── forms.py          # Step 2: Create ContactForm (you'll create this file)
├── views.py          # Step 3: Create views for form and success page
├── urls.py           # Step 5: URL routing (you'll create this file)
├── admin.py          # Step 7: Register model in admin
└── templates/
    └── contact/
        ├── form.html     # Step 4: Form display template
        └── success.html  # Step 4: Success page template
```
</details>

---

## Step 1: Create the Model

Most things start with a model. Here's a contact message model using trim's field shortcuts:

_contact/models.py_

```py
from django.db import models
from trim.models import fields

class ContactMessage(models.Model):
    """Model to store contact form messages."""
    name = fields.chars(max_length=100)
    email = fields.email()
    subject = fields.chars(max_length=200, nil=True)
    message = fields.text()
    created = fields.dt_cu()
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
```

That's it. The `fields` shortcuts save typing while staying 100% compatible with Django's standard fields. `nil=True` is shorthand for `null=True, blank=True`.

<details>
<summary>🚀 <strong>What's happening here</strong></summary>

A "Model" in Django is a Python class that represents a database table. Each attribute of the class corresponds to a column in that table.

We don't really need to worry about that, as the ORM (Object-Relational Mapping) layer of Django handles all the database interactions for us.

We always interact with these python models in our code unless we're doing something low-level.

- `ContactMessage` is our model class, inheriting from `models.Model`.
- Each field (like `name`, `email`, etc.) is defined using `trim.models.fields` shortcuts for less typing.
- `created` uses `dt_cu()` which automatically sets the timestamp when a message is created.
- The `__str__` method defines how the object is represented as a string, useful for admin displays.
</details>

### Run Migrations

Create and apply the database changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Why?** Django needs to create the database table for your new model. `makemigrations` generates the SQL instructions, `migrate` runs them.

<details>
<summary>🔰 <strong>Beginner: What are Migrations?</strong></summary>

**Migrations** are Django's way of propagating changes you make to your models into your database.

**The process:**

1. **You change a model** (add a field, create a new model, etc.)
2. **`makemigrations`** - Django looks at your models and creates a migration file
   - This file contains Python code describing the changes
   - Located in `yourapp/migrations/`
   - Version controlled with your code
3. **`migrate`** - Django applies the migration to your database
   - Creates/modifies database tables
   - Updates the schema to match your models

**Why not write SQL directly?**
- Migrations are database-agnostic (works with PostgreSQL, MySQL, SQLite, etc.)
- Django tracks which migrations have been applied
- Easy to roll back changes if needed
- Team members can sync their databases easily

**Important:** Always run migrations after changing models, otherwise your code and database won't match!
</details>

---

## Step 2: Create the Form

First, let's create the form that will handle user input:

_contact/forms.py_

```py
from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
```

<details>
<summary>🔰 <strong>Beginner: What is a ModelForm?</strong></summary>

A `ModelForm` is a Django shortcut that automatically creates form fields based on your model. 

Instead of writing this:

```py
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200, required=False)
    message = forms.CharField(widget=forms.Textarea)
```

You write this:

```py
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
```

Django reads your model and creates matching form fields automatically. It also handles saving data directly to the database with `form.save()`.

**Benefits:**
- Less code to maintain
- Form fields always match your model
- Built-in validation based on model field types
- Easy database saving
</details>

---

## Step 3: Create the Views

Django's `FormView` handles everything: displaying the form, validating data, and processing submissions. With trim, it's even cleaner:

_contact/views.py_

```py
from django.urls import reverse_lazy
from trim import views
from .forms import ContactForm


class ContactFormView(views.FormView):
    template_name = 'contact/form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:success')
    
    def form_valid(self, form):
        # Save the contact message
        form.save()
        return super().form_valid(form)


class ContactSuccessView(views.TemplateView):
    template_name = 'contact/success.html'
```

<details>
<summary>🔰 <strong>Beginner: Understanding the Views</strong></summary>

**ContactFormView:**
- Inherits from `FormView` - a Django class that handles forms
- `template_name` - which HTML template to display
- `form_class` - which form to use (our ContactForm)
- `success_url` - where to redirect after successful submission
- `form_valid()` - custom method that runs when form data is valid

**ContactSuccessView:**
- Inherits from `TemplateView` - a simple view that just displays a template
- Shows a "thank you" message after form submission

**Why `reverse_lazy`?**
It delays looking up the URL until it's actually needed. This prevents issues when Django is still loading and the URL patterns aren't available yet.

**Why use a "FormView"?**

we _could_ use a standard function-based view, and then _check for POST, validate, save, redirect, etc... But it's a very common pattern, so Django provides `FormView` to handle all that boilerplate for us.

The FormView provides a convenient method `form_valid()` (and `form_invalid()` if needed) to hook into the form processing lifecycle.

> As developers, we shouldn't have to reinvent the wheel every time we need a form. Using `FormView` saves us time and keeps our code clean.

It saves **so much code** compared to writing it all manually! 👍

---

**What happens when someone submits the form?**
1. User fills out form and clicks submit
2. Django validates the data (checks email format, required fields, etc.)
3. If valid, `form_valid()` runs and saves to database
4. User gets redirected to the success page
5. If invalid, form redisplays with error messages
</details>

**Key points:**

- `ContactFormView` handles the form display and submission
- `form_valid()` is called when the form passes validation - we save the message here
- `ContactSuccessView` shows a "thanks" page after submission

---

## Step 4: Create the Templates

_templates/contact/form.html_

```html
{% load quickforms %}
<!DOCTYPE html>
<html>
<head>
    <title>Contact Us</title>
</head>
<body>
    <h1>Contact Us</h1>
    
    {% quickform.form %}
    
    <!-- Or for more control: -->
    <!--
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Send Message</button>
    </form>
    -->
</body>
</html>
```

_templates/contact/success.html_

```html
<!DOCTYPE html>
<html>
<head>
    <title>Thank You!</title>
</head>
<body>
    <h1>Message Sent!</h1>
    <p>Thanks for reaching out. We'll get back to you soon.</p>
    <p><a href="{% url 'contact:form' %}">Send another message</a></p>
</body>
</html>
```

<details>
<summary>🔰 <strong>Beginner: Understanding Templates</strong></summary>

**Templates** are HTML files with special Django tags that let you insert dynamic content.

**Key concepts in our templates:**

**`{% load quickforms %}`** - Loads the trim quickforms template tag library

**`{% quickform.form %}`** - A trim shortcut that renders:
- The complete HTML `<form>` tag with proper action and method
- All form fields with labels
- Error messages if validation fails
- CSRF token for security
- A submit button

**`{% url 'contact:form' %}`** - Generates the URL for the contact form page
- `contact` is the app namespace
- `form` is the URL name we defined in urls.py
- Django generates the actual path (like `/contact/`)

**Why use templates?**
They separate your HTML (presentation) from your Python code (logic), making both easier to maintain.

**Django form rendering options:**
- `{{ form.as_p }}` - Wraps each field in `<p>` tags
- `{{ form.as_table }}` - Renders as table rows
- `{{ form.as_ul }}` - Renders as list items
- Manual rendering - Loop through fields for complete control
</details>

**Note:** `{% quickform.form %}` is a trim shortcut that renders a complete, styled form with submit button and CSRF token. For more control, use the standard Django form rendering shown in the comment.

---

## Step 5: Add the URLs

Connect your views to URLs so people can access them. We'll use trim's cleaner URL syntax:

_contact/urls.py_

```py
from trim.urls import paths_named
from . import views

app_name = 'contact'

urlpatterns = paths_named(views,
    form=('ContactFormView', '',),
    success=('ContactSuccessView', 'success/',),
)
```

This generates URL patterns with names automatically - less typing, same result.

<details>
<summary>📋 <strong>Compare: Classic Django URLs</strong></summary>

Here's the same thing using standard Django URL patterns:

```py
from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactFormView.as_view(), name='form'),
    path('success/', views.ContactSuccessView.as_view(), name='success'),
]
```

**Differences:**
- **Standard Django**: More explicit, manually specify each component
- **Trim's `paths_named`**: Less repetition, names generated from keys
- **Result**: Identical functionality

Both approaches work perfectly - trim just saves you from typing the same names twice.
</details>

<details>
<summary>🔰 <strong>Beginner: Understanding URLs</strong></summary>

**URL patterns** connect web addresses to views.

**`app_name = 'contact'`** - Creates a namespace for your URLs
- Lets you use `{% url 'contact:form' %}` instead of just `{% url 'form' %}`
- Prevents naming conflicts if multiple apps have a 'form' URL

**Standard Django URL pattern:**
```py
path('', views.ContactFormView.as_view(), name='form')
```
- `''` - The URL path (empty means the root of /contact/)
- `views.ContactFormView.as_view()` - The view to run
- `name='form'` - A name to reference this URL

**Trim's `paths_named` shortcut:**
```py
paths_named(views,
    form=('ContactFormView', '',),
)
```
- Automatically generates `name='form'`
- Looks up `ContactFormView` from the views module
- Less repetition, same result

**URL structure:**
- `/contact/` → ContactFormView (shows the form)
- `/contact/success/` → ContactSuccessView (shows thank you message)
</details>

### Wire It Into Your Project

In your main project `urls.py`:

```py
from django.urls import path, include

urlpatterns = [
    # ... your other URLs
    path('contact/', include('contact.urls')),
]
```

---

## Step 6: Test It

Start the development server:

```bash
python manage.py runserver
```

Visit `http://localhost:8000/contact/` and submit a message. You should see the success page.

---

## Step 7: View Messages in Admin

Register your model in the admin to view submitted messages. We'll use trim's quick registration:

_contact/admin.py_

```py
from trim import admin as t_admin
from . import models

t_admin.register_models(models)
```

This registers all models in your module at once - perfect for getting started quickly.

<details>
<summary>📋 <strong>Compare: Classic Django Admin Registration</strong></summary>

Here's the standard Django approach for registering individual models:

```py
from django.contrib import admin
from .models import ContactMessage

admin.site.register(ContactMessage)
```

**Differences:**
- **Standard Django**: Register each model individually, more control per model
- **Trim's `register_models()`**: Registers all models in the module automatically
- **Result**: Both make models visible in admin

For simple cases, trim's approach is faster. For custom admin configurations (list displays, filters, etc.), use the standard approach with `admin.ModelAdmin` classes.
</details>

Visit `http://localhost:8000/admin/` (after creating a superuser with `python manage.py createsuperuser`) to see your submitted messages.

<details>
<summary>🔰 <strong>Beginner: Django Admin</strong></summary>

**Django Admin** is a built-in web interface for managing your database.

**Creating a superuser:**
```bash
python manage.py createsuperuser
```
This creates an admin account. You'll be asked for:
- Username
- Email (optional)
- Password

**Registering models:**
- `admin.site.register(ContactMessage)` - Makes the model appear in admin
- `t_admin.register_models(models)` - Trim shortcut that registers all models in the file

**Why use the admin?**
- View all submitted contact messages
- Edit or delete entries
- No need to build a custom interface for basic CRUD operations
- Great for internal tools and data management

**Accessing admin:**
Visit `/admin/`, log in with your superuser credentials, and you'll see all registered models.
</details>

---

## What You've Built

In about 50 lines of code, you've created:

✅ A database model for contact messages  
✅ A form that validates user input  
✅ A view that handles form submission  
✅ A success page  
✅ URLs to access everything  
✅ Admin integration to view submissions  

## Customizing Your Form

### Add Field Validation

```py
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if 'spam' in email.lower():
            raise forms.ValidationError("Please use a valid email.")
        return email
```

### Add Email Notifications

```py
from django.core.mail import send_mail

class ContactFormView(views.FormView):
    # ... existing code ...
    
    def form_valid(self, form):
        message = form.save()
        
        # Send notification email
        send_mail(
            subject=f"New contact: {message.subject}",
            message=message.message,
            from_email=message.email,
            recipient_list=['admin@example.com'],
        )
        
        return super().form_valid(form)
```

### Customize Fields with Trim

Use trim's form field shortcuts for cleaner code:

```py
from trim.forms import fields

class ContactForm(forms.Form):
    name = fields.chars(max_length=100)
    email = fields.email()
    subject = fields.chars(max_length=200, required=False)
    message = fields.text(rows=10)
    
    def save(self):
        return ContactMessage.objects.create(**self.cleaned_data)
```

See [Form Fields Reference](../forms/fields-auto.md) for all available shortcuts.

---

## Next Steps

Now that you have a working form, you might want to:

- **[Build a ListView](./listview.md)** - Display all contact messages in a table
- **[Add Authentication](../views/authed-views.md)** - Require login to view messages
- **[Use Quickforms](../forms/quickforms.md)** - Drop forms into any page with a template tag
- **[Add More Fields](../forms/fields-auto.md)** - Explore all form field shortcuts

---

## Key Takeaways

Hopefully this helps with understanding the mental model of Django views, with a bit of trim sugar to make it easier.

As a hot overview for beginners:

1. We required a **Model** to store data
2. We created a **Form** to handle user input and validation
3. We built **Views** to display the form and process submissions
4. We set up **URLs** to route requests to our views

It's like web-lego. The quick receipe for every view:

1. I need to store data → Make a Model  
2. I need user to fill it → Make a Form
3. I need to display the form → Make a View
4. I need to access it → Make a URL

And that's it! Everything else is just variations on that theme.

---

For us we used trim to reduce boilerplate, so in summary:

1. We created a model `ContactMessage`
2. We automated the form with _ModelForm_ `ContactForm`
3. We used _FormView_ `ContactFormView` to handle a form lifecycle
4. Some URLs to access the view.

Django's class-based views do the heavy lifting. Trim just makes them faster to write.
