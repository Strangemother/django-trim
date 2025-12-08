# Django-Trim Quick Reference

**Purpose:** Fast lookup for commonly-used components and their documentation status.

## Core Modules (Top Level)

| Module | Purpose | Documented | Doc File |
|--------|---------|------------|----------|
| `trim.admin` | Model registration helpers | ✅ | `docs/admin.md` |
| `trim.apps` | Django app configuration | ✅ | `docs/apps.md` |
| `trim.urls` | URL pattern shortcuts | ✅ | `docs/urls/readme.md` |
| `trim.views` | Class-based view helpers | ✅ | `docs/views/readme.md` |
| `trim.models` | Model field shortcuts | ✅ | `docs/models/readme.md` |
| `trim.forms` | Form utilities | ✅ | `docs/forms/readme.md` |
| `trim.cuts` | ❌ NEEDS DOCS | ❌ | `docs/stubs/trim_cuts.md` |
| `trim.oven` | ❌ NEEDS DOCS | ❌ | `docs/stubs/trim_oven.md` |
| `trim.perms` | Permission utilities | ❌ | `docs/stubs/trim_perms.md` |
| `trim.rand` | Random string generation | ❌ | `docs/stubs/trim_rand.md` |

## Models Package

### Fields (`trim.models.fields`)

**Status:** ✅ Well Documented

**Documentation:** `docs/models/fields.md`

**Common Shortcuts:**
- `fields.fk()` - Foreign key helper
- `fields.user_fk()` - User foreign key
- `fields.bool_false()` - Boolean field (default False)
- `fields.bool_true()` - Boolean field (default True)
- `fields.int()` - Integer field
- `fields.dt_cu_pair()` - Created/Updated datetime pair

### Live Model Access (`trim.models.live`)

**Status:** ✅ Documented

**Documentation:** `docs/models/live.md`

**Usage:**
```python
from trim import live
model = live.app_name.ModelName
```

### Auto Model Mixin (`trim.models.auto`)

**Status:** ✅ Documented

**Documentation:** `docs/models/auto_model_mixin.md`

## Views Package

### Base Views (`trim.views.base`)

**Status:** ⚠️ Partially Documented

**Documentation:** `docs/views/readme.md`

**Key Classes:**
- `ExtraContext` - ✅ Documented
- `HttpMethodsMixin` - ❌ Needs docs
- `MultipleObjectsMixin` - ❌ Needs docs

### List Views (`trim.views.list`)

**Status:** ✅ Documented

**Documentation:** `docs/views/list-views.md`

**Key Classes:**
- `ListView` - ✅ Documented
- `PaginationView` - ✅ Documented

### Authentication Views (`trim.views.auth`)

**Status:** ✅ Documented

**Documentation:** `docs/views/authed-views.md`

**Key Classes:**
- `Permissioned` - ✅ Documented
- `LoginRequired` - ✅ Documented
- `StaffRequired` - ✅ Documented

## Forms Package

### Quick Forms (`trim.forms`)

**Status:** ✅ Documented

**Documentation:** `docs/forms/quickforms.md`

**Template Tag:**
```django
{% load quickforms %}
{% quickform object %}
```

### Widgets (`trim.forms.widgets`)

**Status:** ❌ Mostly Undocumented

**Documentation Status:**
- 20+ widget functions need documentation
- See `DOCUMENTATION_INVENTORY.md` for full list

**Common Functions:**
- `checkbox()` - ❌ Needs docs
- `radios()` - ❌ Needs docs
- `select_multiple()` - ❌ Needs docs

## URLs Package

### Path Generators (`trim.urls`)

**Status:** ✅ Documented

**Documentation:** `docs/urls/readme.md`

**Functions:**
- `paths_named()` - ✅ Documented
- `paths_dict()` - ✅ Documented
- `paths_tuple()` - ✅ Documented

## Template Tags

### Slots (`trim.templatetags.trim_slots`)

**Status:** ✅ Documented

**Documentation:** `docs/templates/tags/`

**Tags:**
- `{% slot %}` - ✅ Documented
- `{% wrap %}` - ✅ Documented

### Links (`trim.templatetags.link`)

**Status:** ✅ Documented

**Template Tag:**
```django
{% load link %}
{% link object %}
```

## Account Package

### Models (`trim.account.models`)

**Status:** ⚠️ Partially Documented

**Classes:**
- `Account` - ✅ Documented in `docs/account.md`
- `AccountEmail` - ❌ Needs docs
- `EmailInvite` - ❌ Needs docs
- `ForgotPasswordRecord` - ❌ Needs docs

### Views (`trim.account.views`)

**Status:** ❌ Mostly Undocumented

**19 view classes need documentation** including:
- Login/logout views
- Password reset views
- Email verification views
- Profile management views

See `DOCUMENTATION_INVENTORY.md` for complete list.

## CLI Package (`trim.cli`)

**Status:** ❌ Undocumented

**Components:** 10 classes, 8 functions

**Priority:** Medium (developer tool, not end-user API)

**Stub:** Not yet generated (subpackage)

## Utilities

### Execute (`trim.execute`)

**Status:** ✅ Documented

**Documentation:** `docs/execute.md`

**Functions:**
- Command execution helpers
- Process management utilities

### Strings (`trim.strings`)

**Status:** ⚠️ Partially Documented

**Functions:**
- String manipulation utilities
- Some documented in various places

### Markdown (`trim.markdown`)

**Status:** ✅ Documented

**Documentation:** `docs/markdown.md`

**Features:**
- Markdown response class
- Template integration

## How to Find More Information

1. **Start here:** Use this quick reference for common components
2. **Detailed info:** Check `DOCUMENTATION_INVENTORY.md` for complete listings
3. **Existing docs:** Browse `docs/` directory
4. **Stubs:** New documentation templates in `docs/stubs/`
5. **Tracking:** Use `documentation_tracking.csv` for progress tracking

## Legend

- ✅ = Well documented with examples
- ⚠️ = Partially documented (some components missing)
- ❌ = Not documented (stub needed)

---

*For comprehensive documentation status, see `DOCUMENTATION_STATUS.md` and `DOCUMENTATION_INVENTORY.md`*
