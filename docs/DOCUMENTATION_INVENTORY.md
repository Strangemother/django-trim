# Django-Trim Documentation Inventory

**Generated:** 2025-12-08 00:54:24

## Summary

- **Total Modules:** 100
- **Total Public Classes:** 110
- **Total Public Functions:** 314
- **Total Documentation Files:** 63

### Documentation Gaps

- **Undocumented Modules:** 12
- **Undocumented Classes:** 75
- **Undocumented Functions:** 137
- **Partially Documented Modules:** 48


## Detailed Module Inventory

**Legend:**

- ✅ = Documented (found references in docs)

- ❌ = Not documented (no references found)

- 📝 = Needs stub

### `trim.account.apps`

**File:** `/workspaces/django-trim/src/trim/account/apps.py`

**Module Documentation:** ✅ Referenced in:
  - `apps.md`
  - `account.md`
  - `readme.md`
  - `urls/functions.md`
  - `urls/readme.md`
  - *...and 6 more*

#### Classes (1)

- **`AccountConfig`** ❌ 📝
  - Inherits: `AppConfig`
  - Key methods: `ready`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.account.forms`

**File:** `/workspaces/django-trim/src/trim/account/forms.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `views.md`
  - `readme.md`
  - `README-4.md`
  - `README-2.md`
  - *...and 8 more*

#### Classes (1)

- **`EmailChangeToken`** ❌ 📝
  - Inherits: `forms.Form`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.account.models`

**File:** `/workspaces/django-trim/src/trim/account/models.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `views.md`
  - `apps.md`
  - `trim-beacon.md`
  - `readme.md`
  - *...and 24 more*

#### Classes (4)

- **`Account`** ✅
  - Inherits: `models.Model`
  - Documented in: `account.md`, `urls/functions.md`

- **`AccountEmail`** ❌ 📝
  - Inherits: `models.Model`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`EmailInvite`** ❌ 📝
  - Inherits: `models.Model`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ForgotPasswordRecord`** ❌ 📝
  - Inherits: `models.Model`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.account.signals`

**File:** `/workspaces/django-trim/src/trim/account/signals.py`

**Module Documentation:** ✅ Referenced in:
  - `research/trim bundle.md`

#### Functions (1)

- **`create_user_account`** ❌ 📝
  - Args: `sender`, `instance`, `created`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.account.views.account`

**File:** `/workspaces/django-trim/src/trim/account/views/account.py`

**Module Documentation:** ✅ Referenced in:
  - `account.md`
  - `urls/functions.md`
  - `urls/readme.md`
  - `old/views.md`
  - `old/old r.md`
  - *...and 1 more*

#### Classes (7)

- **`PasswordChangeView`** ❌ 📝
  - Inherits: `LoginRequiredMixin`, `shorts.FormView`
  - Key methods: `form_valid`, `get_form_kwargs`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`PasswordResetView`** ❌ 📝
  - Inherits: `auth_views.PasswordResetView`
  - Key methods: `form_valid`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ProfileForgotPasswordSuccessView`** ❌ 📝
  - Inherits: `shorts.TemplateView`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ProfileInactiveAccount`** ❌ 📝
  - Inherits: `shorts.TemplateView`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ProfileLogin`** ❌ 📝
  - Inherits: `LoginView`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ProfileLogout`** ❌ 📝
  - Inherits: `LogoutView`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ProfilePasswordUpdateView`** ❌ 📝
  - Inherits: `PasswordChangeView`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (1)

- **`logout_view`** ❌ 📝
  - Args: `request`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.account.views.email`

**File:** `/workspaces/django-trim/src/trim/account/views/email.py`

**Module Documentation:** ✅ Referenced in:
  - `account.md`
  - `README-4.md`
  - `README-2.md`
  - `models/fields-auto-template.md`
  - `models/fields.md`
  - *...and 7 more*

#### Classes (2)

- **`VerifiedEmailUpdateView`** ❌ 📝
  - Inherits: `ProfileUpdateView`
  - Key methods: `get_initial`, `form_valid`, `send_email`, `get_object`, `new_model`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`VerifyEmailTokenView`** ❌ 📝
  - Inherits: `views.FormView`
  - Key methods: `get_initial`, `get`, `form_valid`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.account.views.invite`

**File:** `/workspaces/django-trim/src/trim/account/views/invite.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Classes (2)

- **`EmailInviteCreateView`** ❌ 📝
  - Inherits: `views.CreateView`
  - Key methods: `get_initial`, `form_valid`, `get_success_url`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`EmailInviteListView`** ❌ 📝
  - Inherits: `views.ListView`
  - Key methods: `get_queryset`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.account.views.profile`

**File:** `/workspaces/django-trim/src/trim/account/views/profile.py`

**Module Documentation:** ✅ Referenced in:
  - `account.md`
  - `old/urls.md`

#### Classes (5)

- **`ProfileEmailUpdateView`** ❌ 📝
  - Inherits: `ProfileUpdateView`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ProfileNewAccount`** ❌ 📝
  - Inherits: `views.TemplateView`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ProfileUpdateView`** ❌ 📝
  - Inherits: `views.UpdateView`
  - Key methods: `get_object`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ProfileUsernameUpdateView`** ❌ 📝
  - Inherits: `ProfileUpdateView`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ProfileView`** ✅
  - Inherits: `views.TemplateView`
  - Documented in: `old/urls.md`

### `trim.admin`

**File:** `/workspaces/django-trim/src/trim/admin.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `apps.md`
  - `account.md`
  - `readme.md`
  - `README-4.md`
  - *...and 8 more*

#### Functions (2)

- **`register`** ✅
  - Documented in: `README-3.md`, `trim-beacon.md`

- **`register_models`** ✅
  - Args: `models`, `ignore`
  - Documented in: `README-4.md`, `README-2.md`

### `trim.apps`

**File:** `/workspaces/django-trim/src/trim/apps.py`

**Module Documentation:** ✅ Referenced in:
  - `apps.md`
  - `account.md`
  - `readme.md`
  - `urls/functions.md`
  - `urls/readme.md`
  - *...and 6 more*

#### Classes (1)

- **`ShortConfig`** ❌ 📝
  - Inherits: `AppConfig`
  - Key methods: `ready`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (2)

- **`live_import`** ✅
  - Args: `module_name`
  - Documented in: `apps.md`

- **`silent_import_package_module`** ❌ 📝
  - Args: `package_name`, `module_name`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.cli.base`

**File:** `/workspaces/django-trim/src/trim/cli/base.py`

**Module Documentation:** ✅ Referenced in:
  - `markdown.md`
  - `theming/readme.md`
  - `research/themes.md`
  - `research/trim bundle.md`

#### Classes (7)

- **`AppActions`** ❌ 📝
  - Inherits: `ConfigMixin`
  - Key methods: `__init__`, `setup`, `prep`, `get_register_function`, `get_subparser`
 *...+5 more*
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`AppArgument`** ❌ 📝
  - Inherits: `AppFunction`
  - Key methods: `hook_parser`, `get_parser`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`AppFunction`** ❌ 📝
  - Inherits: `ConfigMixin`
  - Key methods: `__init_subclass__`, `prep`, `hook_parser`, `setup_args`, `hook`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ConfigMixin`** ❌ 📝
  - Inherits: `object`
  - Key methods: `get_conf`, `get_conf_path`, `write_conf_data`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`Help`** ✅
  - Documented in: `markdown.md`, `models/fields-auto.md`

- **`NoPosition`** ❌ 📝
  - Inherits: `Exception`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`SubHelpFormatter`** ❌ 📝
  - Inherits: `argparse.HelpFormatter`
  - Key methods: `__init__`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (3)

- **`get_subactions`** ❌ 📝
  - Args: `parser`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`print_help`** ❌ 📝
  - Args: `parser`, `less`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`print_sub_help`** ❌ 📝
  - Args: `choices`, `subparser`, `depth`, `add_spaces`, `prefix`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.cli.primary`

**File:** `/workspaces/django-trim/src/trim/cli/primary.py`

**Module Documentation:** ✅ Referenced in:
  - `apps.md`
  - `urls/functions.md`
  - `urls/readme.md`
  - `old/slots.md`
  - `old/views.md`
  - *...and 2 more*

#### Classes (12)

- **`DefaultHelp`** ❌ 📝
  - Inherits: `AppArgument`
  - Key methods: `setup_args`, `caller`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`GraphApps`** ❌ 📝
  - Inherits: `object`
  - Key methods: `build_graph_parsers`, `depthed_default_caller`, `run_units`, `execute_step`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`Help`** ✅
  - Inherits: `BHelp`
  - Documented in: `markdown.md`, `models/fields-auto.md`

- **`ScriptInstall`** ❌ 📝
  - Inherits: `ConfigMixin`
  - Key methods: `parse_script_path_place`, `parse_raw_path_place`, `as_path`, `install`, `append_graph`
 *...+1 more*
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`Scripts`** ✅
  - Inherits: `AppFunction`
  - Documented in: `old/notes.md`, `research/trim bundle.md`

- **`ScriptsAdd`** ❌ 📝
  - Inherits: `AppFunction`
  - Key methods: `hook`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ScriptsAddFilenameArg`** ❌ 📝
  - Inherits: `AppArgument`
  - Key methods: `setup_args`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`StepExecute`** ❌ 📝
  - Inherits: `object`
  - Key methods: `execute_step`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`TrimAdminApp`** ❌ 📝
  - Inherits: `TrimApp`
  - Key methods: `get_conf`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`TrimApp`** ❌ 📝
  - Inherits: `AppActions`, `StepExecute`, `GraphApps`
  - Key methods: `setup`, `scripts_func`, `default_caller`, `add`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`VerboseSwitch`** ❌ 📝
  - Inherits: `AppArgument`
  - Key methods: `setup_args`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`VersionSwitch`** ❌ 📝
  - Inherits: `AppArgument`
  - Key methods: `setup_args`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (2)

- **`main`** ✅
  - Documented in: `models/auto_model_mixin.md`, `old/views.md`

- **`main_admin`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.cli.run`

**File:** `/workspaces/django-trim/src/trim/cli/run.py`

**Module Documentation:** ✅ Referenced in:
  - `old/views.md`
  - `research/trim-scripts.md`
  - `templates/tags/wrap-slots.md`

#### Functions (8)

- **`inj`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`main`** ✅
  - Documented in: `models/auto_model_mixin.md`, `old/views.md`

- **`read_one_stream_command`** ✅
  - Args: `command`, `show`
  - Documented in: `readme.md`, `execute.md`

- **`run_command`** ❌ 📝
  - Args: `command`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`run_command2`** ❌ 📝
  - Args: `cmd`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`run_poll_command`** ❌ 📝
  - Args: `command`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`subcall_stream`** ❌ 📝
  - Args: `cmd`, `fail_on_error`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`test_entry_point`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.conf`

**File:** `/workspaces/django-trim/src/trim/conf.py`

**Module Documentation:** ✅ Referenced in:
  - `apps.md`
  - `theming/readme.md`

#### Classes (1)

- **`LiveConfigure`** ❌ 📝
  - Inherits: `object`
  - Key methods: `installed_apps`, `middleware`, `configure_settings`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.context`

**File:** `/workspaces/django-trim/src/trim/context.py`

**Module Documentation:** ✅ Referenced in:
  - `apps.md`
  - `forms/quickforms.md`
  - `views/files-up-down.md`
  - `templates/tags/strings.md`
  - `templates/tags/wrap.md`

#### Functions (1)

- **`appname`** ✅
  - Args: `request`
  - Documented in: `old/views.md`, `research/themes.md`

### `trim.cuts`

**File:** `/workspaces/django-trim/src/trim/cuts.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Functions (1)

- **`get_model`** ✅
  - Documented in: `models/live.md`

### `trim.execute`

**File:** `/workspaces/django-trim/src/trim/execute.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `readme.md`
  - `README-4.md`
  - `execute.md`
  - `README-2.md`
  - *...and 1 more*

#### Functions (3)

- **`clean`** ✅
  - Args: `text`, `default`
  - Documented in: `README-4.md`, `README-2.md`

- **`proc_wait`** ❌ 📝
  - Args: `proc`, `timeout`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`read_one_stream_command`** ✅
  - Args: `command`
  - Documented in: `readme.md`, `execute.md`

### `trim.forms.demo`

**File:** `/workspaces/django-trim/src/trim/forms/demo.py`

**Module Documentation:** ✅ Referenced in:
  - `README-4.md`
  - `models/live.md`
  - `forms/readme.md`
  - `forms/all-fields-form.md`

#### Classes (1)

- **`AllFieldsForm`** ✅
  - Inherits: `forms.Form`
  - Documented in: `forms/readme.md`, `forms/all-fields-form.md`

### `trim.forms.fields`

**File:** `/workspaces/django-trim/src/trim/forms/fields.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `views.md`
  - `trim-beacon.md`
  - `readme.md`
  - `README-4.md`
  - *...and 18 more*

#### Functions (35)

- **`boolean`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`boolean_false`** ✅
  - Documented in: `models/fields-auto.md`, `forms/all-fields-form.md`

- **`boolean_true`** ✅
  - Documented in: `models/fields-auto.md`, `forms/all-fields-form.md`

- **`chars`** ✅
  - Documented in: `README-4.md`, `README-2.md`

- **`choice`** ✅
  - Documented in: `execute.md`, `forms/all-fields-form.md`

- **`combo`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`date`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`datetime`** ✅
  - Documented in: `trim-beacon.md`, `models/fields.md`

- **`decimal`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`duration`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`email`** ✅
  - Documented in: `account.md`, `README-4.md`

- **`file`** ✅
  - Documented in: `README-3.md`, `apps.md`

- **`file_path`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`files`** ✅
  - Documented in: `README-3.md`, `apps.md`

- **`float`** ✅
  - Documented in: `models/fields-auto.md`, `forms/all-fields-form.md`

- **`generic_ip_address`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`hidden`** ✅
  - Args: `field`
  - Documented in: `readme.md`, `widgets/hidden.md`

- **`hidden_chars`** ✅
  - Documented in: `widgets/hidden.md`, `forms/all-fields-form.md`

- **`image`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`integer`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`json`** ✅
  - Documented in: `README-3.md`, `README-4.md`

- **`modelchoice`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`multi_value`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`multiple_choice`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`null_boolean`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`password`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`regex`** ✅
  - Documented in: `forms/all-fields-form.md`, `research/trim-docs.md`

- **`slug`** ✅
  - Documented in: `urls/readme.md`, `models/fields.md`

- **`split_datetime`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`text`** ✅
  - Documented in: `readme.md`, `README-4.md`

- **`time`** ✅
  - Documented in: `README-3.md`, `apps.md`

- **`typed_choice`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`typed_multiple_choice`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`url`** ✅
  - Documented in: `README-3.md`, `account.md`

- **`uuid`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

### `trim.forms.list`

**File:** `/workspaces/django-trim/src/trim/forms/list.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `views.md`
  - `README-4.md`
  - `README-2.md`
  - `theming/readme.md`
  - *...and 16 more*

#### Classes (1)

- **`ListForm`** ✅
  - Inherits: `forms.Form`
  - Documented in: `views/list-views.md`

### `trim.forms.upload`

**File:** `/workspaces/django-trim/src/trim/forms/upload.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `README-4.md`
  - `README-2.md`
  - `models/fields-auto.md`
  - `views/files-up-down.md`
  - *...and 1 more*

#### Classes (4)

- **`FileChunkForm`** ❌ 📝
  - Inherits: `forms.Form`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`FileForm`** ❌ 📝
  - Inherits: `forms.Form`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`FilesForm`** ❌ 📝
  - Inherits: `forms.Form`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`MergeConfirmForm`** ❌ 📝
  - Inherits: `forms.Form`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (1)

- **`file_upload_loc`** ❌ 📝
  - Args: `instance`, `filename`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.forms.widgets`

**File:** `/workspaces/django-trim/src/trim/forms/widgets.py`

**Module Documentation:** ✅ Referenced in:
  - `readme.md`
  - `widgets/hidden.md`

#### Classes (1)

- **`MultipleFileInput`** ❌ 📝
  - Inherits: `widgets.ClearableFileInput`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (27)

- **`base`** ✅
  - Documented in: `markdown.md`, `theming/readme.md`

- **`checkbox`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`checkboxes`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`choice`** ✅
  - Documented in: `execute.md`, `forms/all-fields-form.md`

- **`clearable_file_input`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`date`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`date_time`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`date_time_base`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`email`** ✅
  - Documented in: `account.md`, `README-4.md`

- **`file`** ✅
  - Documented in: `README-3.md`, `apps.md`

- **`hidden`** ✅
  - Documented in: `readme.md`, `widgets/hidden.md`

- **`multi_widget`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`multiple_hidden`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`null_boolean_select`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`number`** ✅
  - Documented in: `models/fields-auto.md`

- **`ordered_set`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`password`** ✅
  - Documented in: `forms/all-fields-form.md`

- **`radios`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`select`** ✅
  - Documented in: `research/trim-docs.md`

- **`select_date`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`select_multiple`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`split_date_time`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`split_hidden_date_time`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`text`** ✅
  - Documented in: `readme.md`, `README-4.md`

- **`textarea`** ✅
  - Documented in: `old/old r.md`, `forms/readme.md`

- **`time`** ✅
  - Documented in: `README-3.md`, `apps.md`

- **`url`** ✅
  - Documented in: `README-3.md`, `account.md`

### `trim.management.commands.gen_doc`

**File:** `/workspaces/django-trim/src/trim/management/commands/gen_doc.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Classes (1)

- **`Command`** ✅
  - Inherits: `BaseCommand`
  - Key methods: `handle`, `out`
  - Documented in: `execute.md`, `old/notes.md`

### `trim.markdown.response`

**File:** `/workspaces/django-trim/src/trim/markdown/response.py`

**Module Documentation:** ✅ Referenced in:
  - `markdown.md`
  - `old/Custom 404.md`
  - `views/files-up-down.md`
  - `templates/tags/quickform.md`

#### Classes (5)

- **`MarkdownDoubleTemplateResponse`** ❌ 📝
  - Inherits: `MarkdownTemplateResponse`
  - Key methods: `rendered_content`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`MarkdownReponseMixin`** ✅
  - Inherits: `object`
  - Documented in: `markdown.md`

- **`MarkdownTemplateResponse`** ✅
  - Inherits: `TemplateResponse`
  - Key methods: `rendered_content`, `get_markdown_object`
  - Documented in: `markdown.md`

- **`MarkdownToMarkdownTemplateResponse`** ❌ 📝
  - Inherits: `MarkdownTemplateResponse`
  - Key methods: `rendered_content`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`MissingImportError`** ❌ 📝
  - Inherits: `ImportError`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.merge`

**File:** `/workspaces/django-trim/src/trim/merge.py`

**Module Documentation:** ✅ Referenced in:
  - `views/files-up-down.md`
  - `templates/tags/strings.md`

#### Classes (1)

- **`FileExists`** ❌ 📝
  - Inherits: `Exception`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (2)

- **`recombine`** ❌ 📝
  - Args: `dir_path`, `output_filepath`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`split_i`** ❌ 📝
  - Args: `item`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.models.auto`

**File:** `/workspaces/django-trim/src/trim/models/auto.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `readme.md`
  - `README-4.md`
  - `README-2.md`
  - `models/fields.md`
  - *...and 5 more*

#### Classes (1)

- **`AutoModelMixin`** ✅
  - Inherits: `object`
  - Key methods: `__init_subclass__`
  - Documented in: `models/auto_model_mixin.md`

#### Functions (5)

- **`bind_mixins`** ❌ 📝
  - Args: `sender`, `lists`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`get_classes`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`hook_init_model_mixins`** ❌ 📝
  - Args: `sender`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`hook_model_mixin_class`** ❌ 📝
  - Args: `cls`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`hook_waiting_model_mixins`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.models.base`

**File:** `/workspaces/django-trim/src/trim/models/base.py`

**Module Documentation:** ✅ Referenced in:
  - `markdown.md`
  - `theming/readme.md`
  - `research/themes.md`
  - `research/trim bundle.md`

#### Functions (4)

- **`cache_known`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`get_model`** ✅
  - Documented in: `models/live.md`

- **`grab_models`** ✅
  - Args: `_models`, `ignore`
  - Documented in: `admin.md`, `old/views.md`

- **`is_model`** ❌ 📝
  - Args: `name`, `unit`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.models.fields.base`

**File:** `/workspaces/django-trim/src/trim/models/fields/base.py`

**Module Documentation:** ✅ Referenced in:
  - `markdown.md`
  - `theming/readme.md`
  - `research/themes.md`
  - `research/trim bundle.md`

#### Functions (2)

- **`blank_null`** ✅
  - Args: `b`, `n`
  - Documented in: `models/fields-auto.md`

- **`defaults`** ✅
  - Args: `args`, `params`, `nil_sub`, `nil_key`
  - Documented in: `README-3.md`, `theming/readme.md`

### `trim.models.fields.django`

**File:** `/workspaces/django-trim/src/trim/models/fields/django.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `views.md`
  - `apps.md`
  - `trim-beacon.md`
  - `account.md`
  - *...and 38 more*

#### Classes (1)

- **`LazyImport`** ❌ 📝
  - Key methods: `get_GenericForeignKey`, `get_ContentType`, `__getitem__`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (54)

- **`add_generic_key`** ❌ 📝
  - Args: `model`, `field`, `content_type_field`, `id_field`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`any`** ✅
  - Args: `prefix`, `content_type_field`, `id_field`
  - Documented in: `README-3.md`, `apps.md`

- **`any_model_set`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`auto`** ✅
  - Documented in: `README-3.md`, `readme.md`

- **`big_auto`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`big_int`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`binary`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`blank_dt`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`boolean`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`chars`** ✅
  - Args: `first_var`
  - Documented in: `README-4.md`, `README-2.md`

- **`contenttype_fk`** ✅
  - Args: `content_type`
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`date`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`datetime`** ✅
  - Documented in: `trim-beacon.md`, `models/fields.md`

- **`decimal`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`dt_created`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`dt_cu_pair`** ✅
  - Documented in: `models/fields-auto-template.md`, `models/fields.md`

- **`dt_updated`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`duration`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`email`** ✅
  - Documented in: `account.md`, `README-4.md`

- **`false_bool`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`file`** ✅
  - Documented in: `README-3.md`, `apps.md`

- **`filepath`** ✅
  - Documented in: `markdown.md`, `models/fields.md`

- **`fk`** ✅
  - Args: `other`
  - Documented in: `README-3.md`, `README-4.md`

- **`float_`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`generic_fk`** ✅
  - Args: `content_type_field`, `id_field`
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`get_cached`** ❌ 📝
  - Args: `name`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`get_user_model`** ✅
  - Documented in: `models/fields-auto.md`, `models/auto_model_mixin.md`

- **`image`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`integer`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`ip_addr`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`json`** ✅
  - Documented in: `README-3.md`, `README-4.md`

- **`m2m`** ✅
  - Args: `other`
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`null_bool`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`o2o`** ✅
  - Args: `other`
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`pk_uuid`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`pos_big_int`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`pos_int`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`pos_small_int`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`rand_str`** ✅
  - Documented in: `models/fields-auto.md`

- **`self_fk`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`self_m2m`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`slug`** ✅
  - Documented in: `urls/readme.md`, `models/fields.md`

- **`small_auto`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`small_int`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`str_uuid`** ✅
  - Documented in: `models/fields-auto.md`

- **`text`** ✅
  - Documented in: `readme.md`, `README-4.md`

- **`time`** ✅
  - Documented in: `README-3.md`, `apps.md`

- **`true_bool`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`url`** ✅
  - Documented in: `README-3.md`, `account.md`

- **`user_fk`** ✅
  - Documented in: `models/fields-auto-template.md`, `models/fields.md`

- **`user_m2m`** ✅
  - Documented in: `models/fields-auto.md`, `old/views.md`

- **`user_o2o`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`uuid`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`uuid_null`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

### `trim.models.fields.wagtail`

**File:** `/workspaces/django-trim/src/trim/models/fields/wagtail.py`

**Module Documentation:** ✅ Referenced in:
  - `account.md`
  - `old/views.md`

#### Functions (2)

- **`image_fk`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`streamfield`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.models.live`

**File:** `/workspaces/django-trim/src/trim/models/live.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `apps.md`
  - `trim-beacon.md`
  - `readme.md`
  - `README-4.md`
  - *...and 5 more*

#### Classes (2)

- **`MagicModelApp`** ✅
  - Inherits: `object`
  - Key methods: `__getattr__`
  - Documented in: `models/live.md`

- **`MagicModelModel`** ✅
  - Inherits: `object`
  - Key methods: `__init__`, `__getattr__`
  - Documented in: `models/live.md`

### `trim.models.panels.wagtail`

**File:** `/workspaces/django-trim/src/trim/models/panels/wagtail.py`

**Module Documentation:** ✅ Referenced in:
  - `account.md`
  - `old/views.md`

#### Functions (5)

- **`field`** ✅
  - Documented in: `README-3.md`, `trim-beacon.md`

- **`image`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`inline`** ✅
  - Documented in: `research/trim-scripts.md`, `templates/tags/link/readme.md`

- **`snippet`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`streamfield`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.names`

**File:** `/workspaces/django-trim/src/trim/names.py`

**Module Documentation:** ✅ Referenced in:
  - `readme.md`
  - `urls/functions.md`
  - `urls/readme.md`
  - `models/fields.md`
  - `old/slots.md`
  - *...and 4 more*

#### Functions (6)

- **`crud`** ✅
  - Documented in: `views.md`, `old/views.md`

- **`get_mapped_name`** ❌ 📝
  - Args: `instance`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`get_url`** ❌ 📝
  - Args: `name`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`history`** ✅
  - Documented in: `views.md`, `old/views.md`

- **`render_defaults`** ❌ 📝
  - Args: `names`, `parts`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`tidy_enforcements`** ❌ 📝
  - Args: `enforcements`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.oven`

**File:** `/workspaces/django-trim/src/trim/oven.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Functions (1)

- **`cook`** ❌ 📝
  - Args: `func`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.perms`

**File:** `/workspaces/django-trim/src/trim/perms.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Classes (2)

- **`EasyPermissionString`** ❌ 📝
  - Inherits: `object`
  - Key methods: `__init__`, `__getattr__`, `push`, `crud`, `__add__`
 *...+3 more*
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`SlofTuple`** ❌ 📝
  - Inherits: `tuple`
  - Key methods: `slof`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (1)

- **`test`** ✅
  - Documented in: `views/authed-views.md`, `research/trim more.md`

### `trim.rand`

**File:** `/workspaces/django-trim/src/trim/rand.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Functions (1)

- **`rand_str`** ✅
  - Args: `length`
  - Documented in: `models/fields-auto.md`

### `trim.response`

**File:** `/workspaces/django-trim/src/trim/response.py`

**Module Documentation:** ✅ Referenced in:
  - `markdown.md`
  - `old/Custom 404.md`
  - `views/files-up-down.md`
  - `templates/tags/quickform.md`

#### Functions (2)

- **`content_data_response`** ❌ 📝
  - Args: `filedata`, `filename`, `content_types`, `default`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`content_type_response`** ❌ 📝
  - Args: `filepath`, `ext`, `content_types`, `default`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.signals`

**File:** `/workspaces/django-trim/src/trim/signals.py`

**Module Documentation:** ✅ Referenced in:
  - `research/trim bundle.md`

#### Functions (3)

- **`model_pre_init`** ❌ 📝
  - Args: `sender`, `args`, `kwargs`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`repr_printer`** ❌ 📝
  - Args: `self`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`str_printer`** ❌ 📝
  - Args: `self`, `alts`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.strings`

**File:** `/workspaces/django-trim/src/trim/strings.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `readme.md`
  - `README-4.md`
  - `old/views.md`
  - `templates/tags/strings.md`
  - *...and 1 more*

#### Functions (2)

- **`bytes_to_hex`** ❌ 📝
  - Args: `bytes_content`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`str_to_hex`** ❌ 📝
  - Args: `str_content`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templates.trim.upload.upload`

**File:** `/workspaces/django-trim/src/trim/templates/trim/upload/upload.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `README-4.md`
  - `README-2.md`
  - `models/fields-auto.md`
  - `views/files-up-down.md`
  - *...and 1 more*

#### Classes (5)

- **`AssetMixin`** ❌ 📝
  - Inherits: `object`
  - Key methods: `get_uuid`, `get_asset`, `ensure_dir`, `get_upload_dir`, `get_fs`
 *...+2 more*
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`MergeAssetView`** ✅
  - Inherits: `FormView`, `AssetMixin`
  - Key methods: `get_success_url`, `get_out_dir`, `form_valid`, `delete_cache`, `perform`
  - Documented in: `views/files-up-down.md`

- **`UploadAssetSuccessView`** ✅
  - Inherits: `TemplateView`, `AssetMixin`
  - Key methods: `get_context_data`
  - Documented in: `views/files-up-down.md`

- **`UploadAssetView`** ✅
  - Inherits: `FormView`, `AssetMixin`
  - Key methods: `get_context_data`, `form_valid`
  - Documented in: `views/files-up-down.md`

- **`UploadChunkView`** ✅
  - Inherits: `FormView`, `AssetMixin`
  - Key methods: `ensure_fullpath`, `form_valid`, `write_file`
  - Documented in: `views/files-up-down.md`

#### Functions (3)

- **`get_cache`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`unlink_dir_files`** ❌ 📝
  - Args: `dir_path`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`verify_file`** ❌ 📝
  - Args: `asset`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.datetime`

**File:** `/workspaces/django-trim/src/trim/templatetags/datetime.py`

**Module Documentation:** ✅ Referenced in:
  - `trim-beacon.md`
  - `models/fields.md`
  - `models/fields-auto.md`
  - `old/models.md`
  - `old/old r.md`
  - *...and 2 more*

#### Functions (3)

- **`localize_timedelta`** ❌ 📝
  - Args: `delta`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`str_timedelta_tag`** ❌ 📝
  - Args: `late_time`, `early_time`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`timedelta_tag`** ❌ 📝
  - Args: `late_time`, `early_time`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.functional`

**File:** `/workspaces/django-trim/src/trim/templatetags/functional.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `readme.md`
  - `README-4.md`
  - `README-2.md`
  - `old/old r.md`
  - *...and 1 more*

#### Functions (1)

- **`functional`** ✅
  - Args: `name`
  - Documented in: `README-3.md`, `readme.md`

### `trim.templatetags.link`

**File:** `/workspaces/django-trim/src/trim/templatetags/link.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `apps.md`
  - `readme.md`
  - `README-4.md`
  - `README-2.md`
  - *...and 6 more*

#### Classes (1)

- **`ShadowDict`** ❌ 📝
  - Inherits: `dict`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (9)

- **`abs_link`** ❌ 📝
  - Args: `context`, `link`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`css_link`** ❌ 📝
  - Args: `link`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`gen_link`** ❌ 📝
  - Args: `link`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`link`** ✅
  - Args: `link`
  - Documented in: `README-3.md`, `apps.md`

- **`link_info`** ❌ 📝
  - Args: `view_name`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`new_link`** ❌ 📝
  - Args: `link`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`new_url_link`** ❌ 📝
  - Args: `link`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`script_link`** ❌ 📝
  - Args: `link`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`url_link`** ❌ 📝
  - Args: `link`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.markdown`

**File:** `/workspaces/django-trim/src/trim/templatetags/markdown.py`

**Module Documentation:** ✅ Referenced in:
  - `markdown.md`
  - `readme.md`
  - `README-4.md`
  - `README-2.md`
  - `recipes/todo-list.md`
  - *...and 1 more*

#### Classes (2)

- **`IncludeNode`** ❌ 📝
  - Inherits: `Node`
  - Key methods: `__init__`, `__repr__`, `render`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`MarkdownContentNode`** ❌ 📝
  - Inherits: `template.Node`
  - Key methods: `__init__`, `render`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (6)

- **`do_markdown_file`** ❌ 📝
  - Args: `parser`, `token`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`do_slot`** ✅
  - Args: `parser`, `token`
  - Documented in: `old/slots.md`

- **`get_file_contents`** ❌ 📝
  - Args: `path`, `parent`, `safe`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`get_markdown_object`** ❌ 📝
  - Args: `context`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`src_code_content_template`** ❌ 📝
  - Args: `context`, `part_a`, `part_b`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`src_code_content_text`** ❌ 📝
  - Args: `context`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.quickforms`

**File:** `/workspaces/django-trim/src/trim/templatetags/quickforms.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `readme.md`
  - `README-4.md`
  - `README-2.md`
  - `forms/quickforms.md`
  - *...and 2 more*

#### Functions (2)

- **`quickform`** ✅
  - Args: `context`, `view_name`
  - Documented in: `README-3.md`, `readme.md`

- **`quickform_template`** ❌ 📝
  - Args: `context`, `view_name`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.shared_tools`

**File:** `/workspaces/django-trim/src/trim/templatetags/shared_tools.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Functions (3)

- **`extract_with_statement`** ❌ 📝
  - Args: `token`, `parser`, `splits`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`parse_tag`** ❌ 📝
  - Args: `parser`, `token`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`parse_until`** ❌ 📝
  - Args: `parser`, `token`, `ends`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.slots.base`

**File:** `/workspaces/django-trim/src/trim/templatetags/slots/base.py`

**Module Documentation:** ✅ Referenced in:
  - `markdown.md`
  - `theming/readme.md`
  - `research/themes.md`
  - `research/trim bundle.md`

#### Classes (1)

- **`SlotList`** ✅
  - Inherits: `object`
  - Key methods: `__init__`, `add`, `set`, `apply_lost`, `get_nodes`
 *...+2 more*
  - Documented in: `old/slots.md`

#### Functions (2)

- **`inject_node`** ❌ 📝
  - Args: `parser`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`parse_until`** ❌ 📝
  - Args: `parser`, `token`, `ends`, `delete_first`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.slots.slot_node`

**File:** `/workspaces/django-trim/src/trim/templatetags/slots/slot_node.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Classes (2)

- **`DefineSlotNode`** ✅
  - Inherits: `template.Node`
  - Key methods: `__init__`, `get_default_name`, `get_slot_names`, `apply_parent`, `resolve_extra_context`
 *...+2 more*
  - Documented in: `old/slots.md`

- **`SlotNode`** ✅
  - Inherits: `template.Node`
  - Key methods: `__init__`, `get_default_name`, `get_slot_names`, `render`, `default_render`
  - Documented in: `old/slots.md`

#### Functions (3)

- **`do_define_slot`** ✅
  - Args: `parser`, `token`
  - Documented in: `old/slots.md`

- **`do_slot`** ✅
  - Args: `parser`, `token`
  - Documented in: `old/slots.md`

- **`slot_into_parent`** ❌ 📝
  - Args: `parser`, `slotnode`, `slotlist_name`, `parent_node_name`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.slots.wrap_node`

**File:** `/workspaces/django-trim/src/trim/templatetags/slots/wrap_node.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Classes (1)

- **`WrappedContentNode`** ❌ 📝
  - Inherits: `template.Node`
  - Key methods: `__init__`, `announce_wrapper`, `render`, `slot_render`, `filter_not`
 *...+2 more*
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (1)

- **`do_wrap`** ✅
  - Args: `parser`, `token`
  - Documented in: `old/slots.md`

### `trim.templatetags.stock`

**File:** `/workspaces/django-trim/src/trim/templatetags/stock.py`

**Module Documentation:** ✅ Referenced in:
  - `urls/readme.md`
  - `models/fields.md`
  - `models/auto_model_mixin.md`
  - `templates/tags/quickform.md`
  - `templates/tags/wrap.md`

#### Functions (1)

- **`stockcount_product`** ❌ 📝
  - Args: `context`, `stockcount_id`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.strings`

**File:** `/workspaces/django-trim/src/trim/templatetags/strings.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `readme.md`
  - `README-4.md`
  - `old/views.md`
  - `templates/tags/strings.md`
  - *...and 1 more*

#### Functions (1)

- **`str_merge`** ✅
  - Documented in: `templates/tags/strings.md`

### `trim.templatetags.trim`

**File:** `/workspaces/django-trim/src/trim/templatetags/trim.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `views.md`
  - `apps.md`
  - `account.md`
  - `markdown.md`
  - *...and 38 more*

#### Classes (2)

- **`SlotNode`** ✅
  - Inherits: `template.Node`
  - Key methods: `__init__`, `render`
  - Documented in: `old/slots.md`

- **`WrappedContentNode`** ❌ 📝
  - Inherits: `template.Node`
  - Key methods: `__init__`, `render`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (4)

- **`do_slot`** ✅
  - Args: `parser`, `token`
  - Documented in: `old/slots.md`

- **`do_wrap`** ✅
  - Args: `parser`, `token`
  - Documented in: `old/slots.md`

- **`inject_node`** ❌ 📝
  - Args: `parser`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`parse_until`** ❌ 📝
  - Args: `parser`, `token`, `ends`, `delete_first`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.trim_slots`

**File:** `/workspaces/django-trim/src/trim/templatetags/trim_slots.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Classes (2)

- **`SlotNode`** ✅
  - Inherits: `template.Node`
  - Key methods: `__init__`, `render`, `render_mode_render`, `render_mode_fragment`
  - Documented in: `old/slots.md`

- **`WrappedContentNode`** ❌ 📝
  - Inherits: `template.Node`
  - Key methods: `__init__`, `render`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (3)

- **`do_slot`** ✅
  - Args: `parser`, `token`
  - Documented in: `old/slots.md`

- **`do_wrap`** ✅
  - Args: `parser`, `token`
  - Documented in: `old/slots.md`

- **`inject_node`** ❌ 📝
  - Args: `parser`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.templatetags.updated_params`

**File:** `/workspaces/django-trim/src/trim/templatetags/updated_params.py`

**Module Documentation:** ✅ Referenced in:
  - `templates/tags/updated-params.md`

#### Functions (1)

- **`updated_params`** ✅
  - Args: `context`
  - Documented in: `templates/tags/updated-params.md`

### `trim.theming.apps`

**File:** `/workspaces/django-trim/src/trim/theming/apps.py`

**Module Documentation:** ✅ Referenced in:
  - `apps.md`
  - `account.md`
  - `readme.md`
  - `urls/functions.md`
  - `urls/readme.md`
  - *...and 6 more*

#### Classes (1)

- **`ThemingConfig`** ❌ 📝
  - Inherits: `AppConfig`
  - Key methods: `ready`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.theming.config`

**File:** `/workspaces/django-trim/src/trim/theming/config.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `apps.md`
  - `theming/readme.md`
  - `research/trim-docs.md`
  - `research/trim-beacon.md`
  - *...and 1 more*

#### Functions (6)

- **`get_theme_map`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`install`** ✅
  - Documented in: `README-3.md`, `account.md`

- **`name_default_redirect`** ✅
  - Args: `origin`, `target`, `target_template`, `default_template`, `default_word`
  - Documented in: `theming/readme.md`, `research/themes.md`

- **`name_redirect`** ❌ 📝
  - Args: `origin`, `target`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`set_ready_map`** ❌ 📝
  - Args: `data`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`theme_option`** ❌ 📝
  - Args: `key`, `var`, `default`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.theming.context`

**File:** `/workspaces/django-trim/src/trim/theming/context.py`

**Module Documentation:** ✅ Referenced in:
  - `apps.md`
  - `forms/quickforms.md`
  - `views/files-up-down.md`
  - `templates/tags/strings.md`
  - `templates/tags/wrap.md`

#### Classes (2)

- **`NoThemingTemplateFound`** ❌ 📝
  - Inherits: `Exception`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`Theming`** ✅
  - Inherits: `object`
  - Key methods: `__init__`, `get_theme_map`, `_resolve`, `_template_resolve`, `resolve_theme_parent`
 *...+4 more*
  - Documented in: `readme.md`, `theming/readme.md`

#### Functions (3)

- **`build_default_themer`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`find_template`** ❌ 📝
  - Args: `mappings`, `name`, `root`, `version`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`magic_strings`** ❌ 📝
  - Args: `request`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.theming.templatetags.theming`

**File:** `/workspaces/django-trim/src/trim/theming/templatetags/theming.py`

**Module Documentation:** ✅ Referenced in:
  - `readme.md`
  - `theming/readme.md`
  - `recipes/listview.md`
  - `research/themes.md`

#### Classes (1)

- **`ThemeExtendsNode`** ❌ 📝
  - Inherits: `Node`
  - Key methods: `__init__`, `get_parent_token`, `__repr__`, `find_template`, `resolve_parent`
 *...+3 more*
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (3)

- **`do_theme_extends`** ❌ 📝
  - Args: `parser`, `token`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`get_attr`** ❌ 📝
  - Args: `value`, `arg`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`theme_string`** ❌ 📝
  - Args: `context`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.urls`

**File:** `/workspaces/django-trim/src/trim/urls.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `apps.md`
  - `account.md`
  - `readme.md`
  - `README-4.md`
  - *...and 16 more*

#### Functions (19)

- **`absolute_reverse`** ✅
  - Args: `request`, `name`
  - Documented in: `urls/functions.md`, `urls/readme.md`

- **`absolutify`** ✅
  - Args: `request`, `path`
  - Documented in: `urls/functions.md`, `urls/readme.md`

- **`as_templates`** ✅
  - Documented in: `urls/functions.md`, `urls/readme.md`

- **`clean_str`** ❌ 📝
  - Args: `variant`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`error_handlers`** ✅
  - Args: `name`, `setup`, `template_dir`
  - Documented in: `urls/functions.md`

- **`favicon_path`** ✅
  - Args: `ingress_path`, `static_path`
  - Documented in: `urls/functions.md`, `urls/readme.md`

- **`index`** ✅
  - Args: `name`
  - Documented in: `apps.md`, `markdown.md`

- **`path_include`** ✅
  - Args: `url_name`, `url_module`, `path_name`
  - Documented in: `account.md`, `urls/functions.md`

- **`path_includes`** ✅
  - Documented in: `account.md`, `urls/functions.md`

- **`path_includes_pair`** ✅
  - Documented in: `urls/functions.md`, `urls/readme.md`

- **`path_urls`** ❌ 📝
  - Args: `views`, `path_rels`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`paths`** ✅
  - Args: `path_dict`
  - Documented in: `README-3.md`, `markdown.md`

- **`paths_default`** ✅
  - Args: `views_module`, `model_list`, `ignore_missing_views`, `views`
  - Documented in: `old/views.md`

- **`paths_dict`** ✅
  - Args: `views`, `patterns`, `view_prefix`, `ignore_missing_views`, `url_pattern_prefix`
  - Documented in: `urls/functions.md`, `urls/readme.md`

- **`paths_less`** ❌ 📝
  - Args: `views`, `model_list`, `ignore_missing_views`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`paths_named`** ✅
  - Args: `views`, `view_prefix`, `ignore_missing_views`, `url_pattern_prefix`, `url_name_prefix`
  - Documented in: `README-3.md`, `README-4.md`

- **`paths_tuple`** ✅
  - Args: `views`, `patterns`
  - Documented in: `urls/functions.md`, `old/urls.md`

- **`static_redirect_path`** ❌ 📝
  - Args: `ingress_path`, `static_path`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`template_view`** ✅
  - Args: `url_string`, `html_path`, `name`
  - Documented in: `urls/functions.md`, `urls/readme.md`

### `trim.views.auth`

**File:** `/workspaces/django-trim/src/trim/views/auth.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `research/trim bundle.md`

#### Classes (3)

- **`IsStaffMixin`** ✅
  - Inherits: `UserPassesTestMixin`
  - Key methods: `test_func`
  - Documented in: `views.md`, `views/authed-views.md`

- **`MissingField`** ❌ 📝
  - Inherits: `Exception`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`UserOwnedMixin`** ✅
  - Inherits: `UserPassesTestMixin`
  - Key methods: `test_func`
  - Documented in: `views/authed-views.md`, `views/readme.md`

#### Functions (1)

- **`is_staff_or_admin`** ❌ 📝
  - Args: `user`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.views.base`

**File:** `/workspaces/django-trim/src/trim/views/base.py`

**Module Documentation:** ✅ Referenced in:
  - `markdown.md`
  - `theming/readme.md`
  - `research/themes.md`
  - `research/trim bundle.md`

#### Classes (1)

- **`ShortMixin`** ❌ 📝
  - Key methods: `get_template_names`, `get_context_data`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (14)

- **`copy_update`** ❌ 📝
  - Args: `entity`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`create_class_slot`** ❌ 📝
  - Args: `master_class`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`crud`** ✅
  - Args: `model`, `class_module_name`, `success_url`, `success_url_bit`
  - Documented in: `views.md`, `old/views.md`

- **`crud_classes`** ✅
  - Args: `target_name`, `model_class`, `success_url`, `success_url_bit`, `models`
  - Documented in: `views.md`, `old/views.md`

- **`discover_models`** ❌ 📝
  - Args: `target_name`, `models`, `module_needles`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`ensure_tuple`** ❌ 📝
  - Args: `items`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`extract_location`** ❌ 📝
  - Args: `target`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`first_bit`** ❌ 📝
  - Args: `word`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`gen_class`** ❌ 📝
  - Args: `crud_name`, `crud_parents`, `class_definition`, `class_module_name`, `master_class_position`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`gen_packed_views`** ❌ 📝
  - Args: `name`, `class_module_name`, `view_packs`, `master_class_position`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`gen_thin_packs`** ❌ 📝
  - Args: `parts`, `base_definition`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`history`** ✅
  - Args: `model`, `class_module_name`
  - Documented in: `views.md`, `old/views.md`

- **`history_classes`** ✅
  - Args: `target_name`, `model_class`, `models`, `class_module_name`, `module_needles`
  - Documented in: `old/views.md`

- **`thin_parts_gen`** ❌ 📝
  - Args: `parts`, `name`, `base_definition`, `class_module_name`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.views.download`

**File:** `/workspaces/django-trim/src/trim/views/download.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `trim-beacon.md`
  - `README-4.md`
  - `views/files-up-down.md`

#### Classes (1)

- **`RangeFileWrapper`** ❌ 📝
  - Inherits: `object`
  - Key methods: `__init__`, `close`, `__iter__`, `next`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (2)

- **`stream`** ✅
  - Args: `request`, `path`
  - Documented in: `readme.md`, `execute.md`

- **`streamfile_response`** ✅
  - Args: `real_filepath`, `output_filename`, `chunk_size`, `content_type`, `range_header`
  - Documented in: `views/files-up-down.md`

### `trim.views.errors.__init__`

**File:** `/workspaces/django-trim/src/trim/views/errors/__init__.py`

**Module Documentation:** ✅ Referenced in:
  - `old/slots.md`

#### Functions (4)

- **`handler400`** ❌ 📝
  - Args: `request`, `exception`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`handler403`** ❌ 📝
  - Args: `request`, `exception`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`handler404`** ❌ 📝
  - Args: `request`, `exception`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`handler500`** ❌ 📝
  - Args: `request`, `exception`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.views.errors.custom404`

**File:** `/workspaces/django-trim/src/trim/views/errors/custom404.py`

**Module Documentation:** ✅ Referenced in:
  - `old/Custom 404.md`

#### Classes (3)

- **`Custom404`** ✅
  - Inherits: `object`
  - Key methods: `dispatch`, `custom_404`, `custom_404_view`, `get_custom_404_url`, `custom_404_redirect_response`
  - Documented in: `old/Custom 404.md`

- **`Custom404TemplateView`** ❌ 📝
  - Inherits: `TemplateView`
  - Key methods: `get_context_data`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`Missing404RedirectUrl`** ✅
  - Inherits: `Exception`
  - Documented in: `old/Custom 404.md`

### `trim.views.list`

**File:** `/workspaces/django-trim/src/trim/views/list.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `views.md`
  - `README-4.md`
  - `README-2.md`
  - `theming/readme.md`
  - *...and 16 more*

#### Classes (1)

- **`OrderPaginatedListView`** ✅
  - Inherits: `ListView`
  - Key methods: `get_ordering_fields`, `get_form`, `filter_data`, `get_filter_data`, `get_orderby_field`
 *...+5 more*
  - Documented in: `views/list-views.md`

### `trim.views.serialized`

**File:** `/workspaces/django-trim/src/trim/views/serialized.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `README-4.md`
  - `README-2.md`
  - `views/readme.md`
  - `views/serialized.md`

#### Classes (6)

- **`JSONListResponseMixin`** ❌ 📝
  - Inherits: `object`
  - Key methods: `render_to_json_response`, `get_dump_object`, `get_serialiser`, `serialize_result`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`JSONResponseMixin`** ❌ 📝
  - Inherits: `object`
  - Key methods: `render_to_json_response`, `get_data`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`JsonDetailView`** ✅
  - Inherits: `JsonListView`
  - Key methods: `get_results`, `get`, `json_response`, `generate_response`
  - Documented in: `views/serialized.md`

- **`JsonListView`** ✅
  - Inherits: `JSONResponseMixin`, `JSONListResponseMixin`, `DetailView`
  - Key methods: `get_results`, `get_response_extra`, `get`
  - Documented in: `views/serialized.md`

- **`JsonSerializer`** ❌ 📝
  - Inherits: `Serializer`
  - Key methods: `get_dump_object`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`JsonView`** ✅
  - Inherits: `JSONResponseMixin`, `TemplateView`
  - Key methods: `get_serialiser`, `get`
  - Documented in: `views/serialized.md`

### `trim.views.upload`

**File:** `/workspaces/django-trim/src/trim/views/upload.py`

**Module Documentation:** ✅ Referenced in:
  - `README-3.md`
  - `README-4.md`
  - `README-2.md`
  - `models/fields-auto.md`
  - `views/files-up-down.md`
  - *...and 1 more*

#### Classes (5)

- **`AssetMixin`** ❌ 📝
  - Inherits: `object`
  - Key methods: `get_uuid`, `get_asset`, `ensure_dir`, `get_upload_dir`, `get_fs`
 *...+2 more*
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`MergeAssetView`** ✅
  - Inherits: `FormView`, `AssetMixin`
  - Key methods: `get`, `get_success_url`, `get_out_dir`, `form_valid`, `perform_all`
 *...+3 more*
  - Documented in: `views/files-up-down.md`

- **`UploadAssetSuccessView`** ✅
  - Inherits: `TemplateView`, `AssetMixin`
  - Key methods: `get_context_data`
  - Documented in: `views/files-up-down.md`

- **`UploadAssetView`** ✅
  - Inherits: `FormView`, `AssetMixin`
  - Key methods: `get_context_data`, `save_asset`, `form_valid`
  - Documented in: `views/files-up-down.md`

- **`UploadChunkView`** ✅
  - Inherits: `FormView`, `AssetMixin`
  - Key methods: `ensure_fullpath`, `save_file_part`, `generate_store_path`, `form_valid`, `write_file`
  - Documented in: `views/files-up-down.md`

#### Functions (3)

- **`get_cache`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`unlink_dir_files`** ❌ 📝
  - Args: `dir_path`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`verify_file`** ❌ 📝
  - Args: `asset`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.wagtail.blocks`

**File:** `/workspaces/django-trim/src/trim/wagtail/blocks.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Functions (28)

- **`api_field`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`blockquote`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`boolean`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`chars`** ✅
  - Documented in: `README-4.md`, `README-2.md`

- **`choice`** ✅
  - Documented in: `execute.md`, `forms/all-fields-form.md`

- **`date`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`datetime`** ✅
  - Documented in: `trim-beacon.md`, `models/fields.md`

- **`decimal`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`documentchooser`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`email`** ✅
  - Documented in: `account.md`, `README-4.md`

- **`embed`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`field_panel`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`float_`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`imagechooser`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`integer`** ✅
  - Documented in: `models/fields.md`, `models/fields-auto.md`

- **`list_`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`multiplechoice`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`pagechooser`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`rawhtml`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`regex`** ✅
  - Documented in: `forms/all-fields-form.md`, `research/trim-docs.md`

- **`richtext`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`snippetchooser`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`static`** ✅
  - Documented in: `theming/readme.md`, `frontend/readme.md`

- **`stream`** ✅
  - Documented in: `readme.md`, `execute.md`

- **`struct`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`text`** ✅
  - Documented in: `readme.md`, `README-4.md`

- **`time`** ✅
  - Documented in: `README-3.md`, `apps.md`

- **`url`** ✅
  - Documented in: `README-3.md`, `account.md`

### `trim.wagtail.markdown`

**File:** `/workspaces/django-trim/src/trim/wagtail/markdown.py`

**Module Documentation:** ✅ Referenced in:
  - `markdown.md`
  - `readme.md`
  - `README-4.md`
  - `README-2.md`
  - `recipes/todo-list.md`
  - *...and 1 more*

#### Classes (3)

- **`LinkStructValue`** ❌ 📝
  - Inherits: `StructValue`
  - Key methods: `html`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`MarkdownBlock`** ❌ 📝
  - Inherits: `t_blocks.StructBlock`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`Styles`** ❌ 📝
  - Inherits: `t_blocks.StructBlock`
  - Key methods: `__init__`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.wagtail.streamfield`

**File:** `/workspaces/django-trim/src/trim/wagtail/streamfield.py`

**Module Documentation:** ❌ **NEEDS STUB**

#### Classes (3)

- **`HeadingBlock`** ❌ 📝
  - Inherits: `TabbedStructBlock`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`RichTextBlock`** ❌ 📝
  - Inherits: `TabbedStructBlock`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`TabbedStructBlock`** ❌ 📝
  - Inherits: `blocks.StructBlock`
  - Key methods: `render_form_template`
  - **⚠️ NEEDS DOCUMENTATION STUB**

#### Functions (5)

- **`as_api_fields`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`as_fieldpanel_list`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`get_fields`** ❌ 📝
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`pre_install_global_block`** ❌ 📝
  - Args: `name`, `class_`
  - **⚠️ NEEDS DOCUMENTATION STUB**

- **`prepared_streamfield`** ❌ 📝
  - Args: `group`
  - **⚠️ NEEDS DOCUMENTATION STUB**

### `trim.wagtail.views.generic`

**File:** `/workspaces/django-trim/src/trim/wagtail/views/generic.py`

**Module Documentation:** ✅ Referenced in:
  - `account.md`
  - `markdown.md`
  - `urls/readme.md`
  - `models/auto_model_mixin.md`
  - `views/files-up-down.md`
  - *...and 3 more*

#### Classes (1)

- **`StructuredPage`** ❌ 📝
  - Inherits: `Page`
  - **⚠️ NEEDS DOCUMENTATION STUB**


## Documentation Stubs Needed

### Priority 1: Core Modules (No Documentation)

- **`trim.cuts`**
  - 0 classes, 1 functions
  - Suggested file: `docs/trim/cuts.md`

- **`trim.oven`**
  - 0 classes, 1 functions
  - Suggested file: `docs/trim/oven.md`

- **`trim.perms`**
  - 2 classes, 1 functions
  - Suggested file: `docs/trim/perms.md`

- **`trim.rand`**
  - 0 classes, 1 functions
  - Suggested file: `docs/trim/rand.md`

### Priority 2: Undocumented Classes
- `trim.account.apps.AccountConfig`
- `trim.account.forms.EmailChangeToken`
- `trim.account.models.AccountEmail`
- `trim.account.models.EmailInvite`
- `trim.account.models.ForgotPasswordRecord`
- `trim.account.views.account.PasswordChangeView`
- `trim.account.views.account.PasswordResetView`
- `trim.account.views.account.ProfileForgotPasswordSuccessView`
- `trim.account.views.account.ProfileInactiveAccount`
- `trim.account.views.account.ProfileLogin`
- `trim.account.views.account.ProfileLogout`
- `trim.account.views.account.ProfilePasswordUpdateView`
- `trim.account.views.email.VerifiedEmailUpdateView`
- `trim.account.views.email.VerifyEmailTokenView`
- `trim.account.views.invite.EmailInviteCreateView`
- `trim.account.views.invite.EmailInviteListView`
- `trim.account.views.profile.ProfileEmailUpdateView`
- `trim.account.views.profile.ProfileNewAccount`
- `trim.account.views.profile.ProfileUpdateView`
- `trim.account.views.profile.ProfileUsernameUpdateView`
- `trim.apps.ShortConfig`
- `trim.cli.base.AppActions`
- `trim.cli.base.AppArgument`
- `trim.cli.base.AppFunction`
- `trim.cli.base.ConfigMixin`
- `trim.cli.base.NoPosition`
- `trim.cli.base.SubHelpFormatter`
- `trim.cli.primary.DefaultHelp`
- `trim.cli.primary.GraphApps`
- `trim.cli.primary.ScriptInstall`

*...and 45 more undocumented classes*

### Priority 3: Undocumented Functions
- `trim.account.signals.create_user_account`
- `trim.account.views.account.logout_view`
- `trim.apps.silent_import_package_module`
- `trim.cli.base.get_subactions`
- `trim.cli.base.print_help`
- `trim.cli.base.print_sub_help`
- `trim.cli.primary.main_admin`
- `trim.cli.run.inj`
- `trim.cli.run.run_command`
- `trim.cli.run.run_command2`
- `trim.cli.run.run_poll_command`
- `trim.cli.run.subcall_stream`
- `trim.cli.run.test_entry_point`
- `trim.execute.proc_wait`
- `trim.forms.upload.file_upload_loc`
- `trim.forms.widgets.checkbox`
- `trim.forms.widgets.checkboxes`
- `trim.forms.widgets.clearable_file_input`
- `trim.forms.widgets.date_time`
- `trim.forms.widgets.date_time_base`
- `trim.forms.widgets.multi_widget`
- `trim.forms.widgets.multiple_hidden`
- `trim.forms.widgets.null_boolean_select`
- `trim.forms.widgets.ordered_set`
- `trim.forms.widgets.radios`
- `trim.forms.widgets.select_date`
- `trim.forms.widgets.select_multiple`
- `trim.forms.widgets.split_date_time`
- `trim.forms.widgets.split_hidden_date_time`
- `trim.merge.recombine`

*...and 107 more undocumented functions*