"""
Generate documentation for trim.forms.fields module.

This script reads the trim.forms.fields module and generates a comprehensive
markdown document listing all available form field shortcuts with their
Django equivalents and documentation.
"""

from pathlib import Path
from pydoc import locate
from inspect import isfunction
from textwrap import dedent
from collections import defaultdict

HERE = Path(__file__).parent.absolute()
DOCS = HERE.parent / 'docs'
SRC = HERE.parent / 'src'

forms_fields_module = "trim.forms.fields"

# Functions to ignore (internal helpers and aliases handled separately)
IGNORE_FUNCS = (
    '_pop_push',
    '_pop',
    '_push',
)

# Aliases to document separately
ALIASES = {
    'img': 'image',
    'int': 'integer',
    'pwd': 'password',
    'bool': 'boolean',
    'false_bool': 'boolean_false',
    'bool_false': 'boolean_false',
    'true_bool': 'boolean_true',
    'bool_true': 'boolean_true',
    'str': 'chars',
    'char': 'chars',
    'chars_hidden': 'chars',
    'hide': 'hidden',
    'textarea': 'text',
    'file_multi': 'files',
    'multi_file': 'files',
}


def main():
    print('Generating form fields docs...', DOCS)
    
    # Import the module without Django setup since forms don't require it
    import sys
    sys.path.insert(0, str(SRC))
    
    forms_fields = locate(forms_fields_module)
    infos = ()

    for key in dir(forms_fields):
        item = getattr(forms_fields, key)
        
        # Skip private, dunder, and ignored functions
        if key.startswith('_') or (key in IGNORE_FUNCS) or (not isfunction(item)):
            continue
            
        # Skip aliases - we'll handle them separately
        if key in ALIASES:
            continue
        
        info = read_func(item, key)
        if info:
            print(f'{info["key"]} == {info["field_name"]}')
            infos += (info,)

    return process_to_file(infos)


def read_func(item, key):
    """Extract information about a form field function."""
    _name = item.__name__
    
    if _name != key:
        # The func is likely an alias
        if _name in IGNORE_FUNCS:
            print(f'Ignore alias for "{key}" : {_name}')
            return

    # Get function documentation
    doc = item.__doc__
    if doc:
        doc = dedent(doc)
    
    # Try to determine the Django field type by inspecting the function
    field_name = None
    field_module = None
    
    # Parse the function to find the Django field it returns
    import inspect
    source = inspect.getsource(item)
    
    # Look for forms.XxxField pattern
    if 'forms.' in source:
        import re
        match = re.search(r'forms\.(\w+Field)', source)
        if match:
            field_name = match.group(1)
            field_module = 'django.forms'
    
    # If we couldn't determine it, mark as custom/special
    if not field_name:
        field_name = 'Custom/Special'
        field_module = 'trim.forms'

    return {
        'func': item,
        'func_name': _name,
        'key': key,
        'field_name': field_name,
        'field_module': field_module,
        'doc': doc,
    }


def get_doc_line(line):
    """Extract the first meaningful line of documentation."""
    doc = (line.get('doc', None) or '').split('\n')
    if len(doc[0]) > 5:
        return doc[0]
    r = ''.join(doc[0:2])
    if len(r) > 1:
        return r.strip()
    return '_no docs_'


def process_to_file(infos):
    """Convert field information into a markdown document."""
    out = DOCS / "forms/fields-auto.md"
    templ = DOCS / "forms/fields-auto-template.md"

    header = {
        'Name': 'key',
        'Django Field': 'field_name',
        'Alias': 'func_name',
        'Description': 'doc_line',
    }

    lines = ()
    col_a_width = 0
    col_b_width = 0

    for info in infos:
        line = ()
        line += (info,)
        col_a_width = max(col_a_width, len(info['key']) + 2)
        col_b_width = max(col_b_width, len(info['field_name']) + 2)
        lines += line

    template = '| {0} | {1} | {2} | {3}'
    line_template = '| {key:<{col_a_width}} | {tick_field_name:<{col_b_width}} | {func_name} | {doc_line}'

    splits = ('---',) * len(header)
    res = (
        template.format(*header.keys()),
        template.format(*splits),
    )

    for line in lines:
        if line['func_name'] == line['key']:
            line['func_name'] = ' -- '
        else:
            line['func_name'] = f"`{line['func_name']}`"
        line['key'] = f"`{line['key']}`"
        line['tick_field_name'] = f"`{line['field_name']}`"
        line['doc_line'] = get_doc_line(line)

        res += (line_template.format(col_a_width=col_a_width,
                                    col_b_width=col_b_width, **line), )

    # Group by Django field type
    tt_groups = defaultdict(tuple)

    for line in lines:
        tt_groups[line['field_name']] += (line,)

    tt_lines = ()
    typed_toc_lines = ()

    for ttg_k, ttg_v in tt_groups.items():
        ttg_header = f'\n\n## {ttg_k}\n'
        col_b_width = 0
        col_a_width = 0
        tt_lines += (ttg_header,)
        typed_toc_lines += (f'+ [{ttg_k}](#{ttg_k.replace("/", "")})',)

        for item in ttg_v:
            col_a_width = max(col_a_width, len(item['key']))
            col_b_width = max(col_b_width, len(item['field_name']))

        tt_lines += (
            '',
            template.format(*header.keys()),
            template.format(*splits),
        )
        for item in ttg_v:
            tt_line = (line_template.format(col_a_width=col_a_width,
                                          col_b_width=col_b_width, **item), )
            tt_lines += tt_line

        tt_lines += (f"\n[top](#Typed)",)

    table = '\n'.join(res)
    typed_tables = '\n'.join(tt_lines)
    typed_toc = '\n'.join(typed_toc_lines)

    # Generate aliases table
    aliases_lines = ['| Alias | Points To |', '| --- | --- |']
    for alias, target in sorted(ALIASES.items()):
        aliases_lines.append(f'| `{alias}` | `{target}` |')
    aliases_table = '\n'.join(aliases_lines)

    # Read template and substitute
    t_str = templ.read_text()
    
    # Debug: Check what variables the template expects
    import re
    expected_vars = set(re.findall(r'%\((\w+)\)s', t_str))
    print(f"Template expects: {expected_vars}")
    
    substitutions = {
        'table': table,
        'typed_tables': typed_tables,
        'typed_toc': typed_toc,
        'aliases_table': aliases_table,
    }
    
    print(f"Providing: {set(substitutions.keys())}")
    
    out_str = t_str % substitutions
    out.write_text(out_str)

    print(f'\nGenerated: {out}')
    return res


if __name__ == '__main__':
    v = main()
    print(f'\nGenerated {len(v)} field entries')
