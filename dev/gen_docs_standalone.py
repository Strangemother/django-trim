#!/usr/bin/env python3
"""
Generate the fields-auto.md documentation from trim.models.fields.django

This is a standalone version that sets up minimal Django configuration.
Run from the django-trim root directory:
    python dev/gen_docs_standalone.py
"""

from pathlib import Path
import sys
import os

# Setup paths
HERE = Path(__file__).parent.absolute()
DOCS = HERE.parent / "docs"
SRC = HERE.parent / "src"

# Add src to path so we can import trim
sys.path.insert(0, str(SRC))

# Minimal Django configuration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")

# Configure Django settings inline
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
        ],
        SECRET_KEY="dev-secret-key-for-doc-generation",
        USE_TZ=True,
    )

import django

django.setup()

# Now we can import the rest
from pydoc import locate
from inspect import isfunction
from textwrap import dedent
from collections import defaultdict
from django.db import models

# Configuration
django_fields_module = "trim.models.fields.django"
IGNORE_FUNCS = (
    "add_generic_key",
    "any",
    "any_model_set",
    "defaults",
    "get_cached",
)


def main():
    print("🔧 Generating fields documentation...")
    print(f"   Source: {django_fields_module}")
    print(f'   Output: {DOCS / "models/fields-auto.md"}')
    print()

    django_fields = locate(django_fields_module)
    if not django_fields:
        print(f"❌ Error: Could not locate module {django_fields_module}")
        return 1

    infos = ()

    print("📝 Processing fields:")
    for key in dir(django_fields):
        item = getattr(django_fields, key)
        if (key in IGNORE_FUNCS) or (not isfunction(item)):
            continue
        info = read_func(item, key)
        if info:
            print(f'   ✓ {info["key"]:20} -> {info["field_name"]}')
            infos += (info,)

    print(f"\n✅ Processed {len(infos)} field functions")

    result = process_to_file(infos)
    print(f"\n✨ Documentation generated successfully!")
    return 0


def process_to_file(infos):
    """Convert each breakdown into writable format."""
    out = DOCS / "models/fields-auto.md"
    templ = DOCS / "models/fields-auto-template.md"

    if not templ.exists():
        print(f"❌ Error: Template file not found: {templ}")
        return None

    header = {
        "Name": "key",
        "Field Name": "field_name",
        "Alias": "func_name",
        "Help": "doc_line",
    }

    lines = ()
    col_a_width = 0
    col_b_width = 0

    for info in infos:
        line = ()
        line += (info,)
        col_a_width = max(col_a_width, len(info["key"]) + 2)
        col_b_width = max(col_b_width, len(info["field_name"]) + 2)
        lines += line

    template = "| {0} | {1} | {2} | {3}"
    line_template = "| {key:<{col_a_width}} | {tick_field_name:<{col_b_width}} | {func_name} | {doc_line}"

    splits = ("---",) * len(header)
    res = (
        template.format(*header.keys()),
        template.format(*splits),
    )

    for line in lines:
        if line["func_name"] == line["key"]:
            line["func_name"] = " -- "
        else:
            line["func_name"] = f"`{line['func_name']}`"
        line["key"] = f"`{line['key']}`"
        line["tick_field_name"] = f"`{line['field_name']}`"
        line["doc_line"] = get_doc_line(line)

        res += (
            line_template.format(
                col_a_width=col_a_width, col_b_width=col_b_width, **line
            ),
        )

    # Generate typed groups
    tt_groups = defaultdict(tuple)

    for line in lines:
        tt_groups[line["field_name"]] += (line,)

    tt_lines = ()
    typed_toc_lines = ()

    for ttg_k, ttg_v in tt_groups.items():
        ttg_header = f"\n\n## {ttg_k}\n"
        col_b_width = 0
        col_a_width = 0
        tt_lines += (ttg_header,)
        typed_toc_lines += (f"+ [{ttg_k}](#{ttg_k})",)

        for item in ttg_v:
            col_a_width = max(col_a_width, len(item["key"]))
            col_b_width = max(col_b_width, len(item["field_name"]))

        tt_lines += (
            "",
            template.format(*header.keys()),
            template.format(*splits),
        )
        for item in ttg_v:
            tt_line = (
                line_template.format(
                    col_a_width=col_a_width, col_b_width=col_b_width, **item
                ),
            )
            tt_lines += tt_line

        tt_lines += (f"\n[top](#Typed)",)

    # Combine all parts
    table = "\n".join(res)
    typed_tables = "\n".join(tt_lines)
    typed_toc = "\n".join(typed_toc_lines)

    # Read template and substitute
    t_str = templ.read_text()
    out_str = t_str % {
        "table": table,
        "typed_tables": typed_tables,
        "typed_toc": typed_toc,
    }
    out.write_text(out_str)

    print(f"   📄 Written: {out}")
    print(f"   📊 Lines: {len(out_str.splitlines())}")

    return res


def get_doc_line(line):
    """Extract the first meaningful line from docstring."""
    doc = (line.get("doc", None) or "").split("\n")
    if len(doc[0]) > 5:
        return doc[0]
    r = "".join(doc[0:1])
    if len(r) > 1:
        return r
    return "_no docs_"


def read_func(item, key):
    """Extract information from a field function."""
    _name = item.__name__

    if _name != key:
        # The func is likely an alias
        if _name in IGNORE_FUNCS:
            print(f'   ⚠ Ignoring alias for "{key}": {_name}')
            return

    args_map = {
        "fk": ("models.Model",),
        "m2m": ("models.Model",),
        "o2o": ("models.Model",),
    }

    try:
        res = item(
            *args_map.get(key, ()),
        )
    except Exception as exc:
        print(f"   ❌ Issue with {key}: {exc}")
        raise exc

    field_name = res.__class__.__name__
    field_module = res.__class__.__module__
    doc = item.__doc__
    if doc:
        doc = dedent(doc)

    return {
        "func": item,
        "func_name": _name,
        "key": key,
        "result": res,
        "field_name": field_name,
        "field_module": field_module,
        "doc": doc,
    }


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code or 0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
