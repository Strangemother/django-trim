# Development Scripts

This directory contains scripts for maintaining and generating project documentation.

## Documentation Generation

### `gen_docs_standalone.py`

**Purpose:** Automatically generates the `docs/models/fields-auto.md` file by introspecting the `trim.models.fields.django` module.

### `gen_forms_fields_docs.py`

**Purpose:** Automatically generates the `docs/forms/fields-auto.md` file by introspecting the `trim.forms.fields` module.

**Usage:**

```bash
# From the django-trim root directory
python dev/gen_docs_standalone.py
```

**What it does:**

1. Scans all functions in `trim.models.fields.django`
2. Executes each field function to determine the Django field type it creates
3. Extracts docstrings and function aliases
4. Generates markdown tables with:
   - Alphabetical listing of all fields
   - Grouped by field type (e.g., all `IntegerField` variants together)
   - Table of contents

**Output:**
- File: `docs/models/fields-auto.md`
- Generated from template: `docs/models/fields-auto-template.md`

**When to run:**

- After adding new field helper functions to `trim.models.fields.django`
- After updating field docstrings
- When field function names or aliases change

**Requirements:**

- Django must be installed (automatically configured in the script)
- The script creates a minimal in-memory Django configuration

**Example output:**

```
🔧 Generating fields documentation...
   Source: trim.models.fields.django
   Output: /workspaces/django-trim/docs/models/fields-auto.md

📝 Processing fields:
   ✓ auto                 -> AutoField
   ✓ chars                -> CharField
   ✓ fk                   -> ForeignKey
   ...

✅ Processed 80 field functions
   📄 Written: /workspaces/django-trim/docs/models/fields-auto.md
   📊 Lines: 552

✨ Documentation generated successfully!
```

### Template File

The generator uses `docs/models/fields-auto-template.md` as a template. The template contains:

- Header and usage examples (static content)
- Three placeholders that get filled:
  - `%(table)s` - Alphabetical table of all fields
  - `%(typed_toc)s` - Table of contents for typed sections
  - `%(typed_tables)s` - Tables grouped by field type

**To modify the generated docs:**
1. Edit `docs/models/fields-auto-template.md` for structural/introductory changes
2. Edit field docstrings in `src/trim/models/fields/django.py` for field descriptions
3. Re-run `gen_docs_standalone.py`

---

## Form Fields Documentation

### `gen_forms_fields_docs.py`

**Usage:**

```bash
# From the django-trim root directory
python dev/gen_forms_fields_docs.py
```

**What it does:**

1. Scans all functions in `trim.forms.fields`
2. Analyzes source code to determine Django field types
3. Extracts docstrings
4. Generates comprehensive markdown documentation with:
   - Alphabetical listing of all form fields
   - Grouped by Django field type
   - Table of field aliases
   - Usage examples

**Output:**
- File: `docs/forms/fields-auto.md`
- Generated from template: `docs/forms/fields-auto-template.md`

**When to run:**

- After adding new form field helper functions
- After updating field docstrings
- When field aliases change

**Note:** Unlike the model fields generator, this doesn't require Django to be set up since it analyzes the source code directly rather than executing the functions.

---

## Original Script

### `gen_docs.py`

**Status:** Legacy script (requires external Django project)

This is the original version that requires a full Django project at `../../workspace/simple/simple`. It's kept for reference but `gen_docs_standalone.py` is recommended as it doesn't require external dependencies.

---

## Adding New Documentation Generators

If you want to create similar generators for other modules:

1. Copy `gen_docs_standalone.py` as a template
2. Modify the module path and extraction logic
3. Create a template file in `docs/`
4. Update this README with usage instructions

**Template structure:**

```python
# 1. Setup paths and minimal Django config
# 2. Import and introspect the target module
# 3. Extract relevant information (classes, functions, etc.)
# 4. Format as markdown tables
# 5. Use template file with %(placeholder)s syntax
# 6. Write output
```

---

## Troubleshooting

### Django not found

```bash
# Install Django in the virtual environment
pip install django
```

### Module import errors

Make sure you're running from the django-trim root directory:

```bash
cd /path/to/django-trim
python dev/gen_docs_standalone.py
```

### Template not found

Ensure `docs/models/fields-auto-template.md` exists. This file defines the structure of the generated documentation.

---

## Related Documentation

- Generated fields docs: `docs/models/fields-auto.md`
- Template file: `docs/models/fields-auto-template.md`
- Source module: `src/trim/models/fields/django.py`
- Documentation inventory: `DOCUMENTATION_INVENTORY.md`
