from pathlib import Path

HERE = Path(__file__).parent.absolute()
DOCS = HERE.parent / 'docs'
SRC = HERE.parent / 'src'

from pydoc import locate
from inspect import isfunction

from textwrap import dedent

django_fields_module = "trim.models.fields.django"
IGNORE_FUNCS = (
    'add_generic_key',
    'any',
    'any_model_set',
    'defaults',
    'get_cached',
)

import django
import os
import sys

APP = (HERE / '../../workspace/simple/simple').resolve()
# APP = (HERE.parent / 'workspace/simple').absolute()
sys.path.insert(0, str(APP))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple.settings')
django.setup()

def main():
    print('gen_docs', DOCS)
    django_fields = locate(django_fields_module)
    infos = ()


    for key in dir(django_fields):
        item = getattr(django_fields, key)
        if (key in IGNORE_FUNCS) or (not isfunction(item)):
            continue
        info = read_func(item, key)
        if info:
            print(f'{info["key"]} == {info["field_name"]}')
            infos += (info,)

    return process_to_file(infos)

def process_to_file(infos):
    """Convert each breakdown into writable format.
    """
    out = DOCS / "models/fields-auto.md"
    templ = DOCS / "models/fields-auto-template.md"

    header = {
            'Name': 'key',
            'Field Name': 'field_name',
            'Alias': 'func_name',
            'Help': 'doc_line',
        }

    lines = ()
    col_a_width = 0
    col_b_width = 0

    for info in infos:
        line = ()
        line += (info,)
        # for k, v in header.items():
        col_a_width = max(col_a_width, len(info['key'])+2)
        col_b_width = max(col_b_width, len(info['field_name'])+2)

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

    tt_groups = defaultdict(tuple)

    for line in lines:
        tt_groups[line['field_name']] += (line,)

    tt_lines = ()
    typed_toc_lines = ()


    for ttg_k, ttg_v in tt_groups.items():
        ttg_header = (
            f'\n\n## {ttg_k}\n'
            )
        col_b_width = 0
        col_a_width = 0
        tt_lines += (ttg_header,)
        typed_toc_lines += (f'+ [{ttg_k}](#{ttg_k})',)

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
            tt_lines +=  tt_line

        tt_lines +=  (f"\n[top](#Typed)",)


    table = '\n'.join(res)
    typed_tables = '\n'.join(tt_lines)
    typed_toc = '\n'.join(typed_toc_lines)

    t_str = templ.read_text()
    out_str = t_str % {
        'table':table,
        'typed_tables': typed_tables,
        'typed_toc':typed_toc,
        }
    out.write_text(out_str)


    return res


from collections import defaultdict
from django.db import models

def get_doc_line(line):
    doc = (line.get('doc', None) or '').split('\n')
    if len(doc[0]) > 5:
        return doc[0]
    r = ''.join(doc[0:1])
    if len(r) > 1:
        return r
    return '_no docs_'

def read_func(item, key):
    _name = item.__name__

    if _name != key:
        # the func is likely an alias.
        if _name in IGNORE_FUNCS:
            print(f'Ignore alias for "{key}" : {_name}')
            return

    args_map = {
        'fk': ('models.Model',),
        'm2m': ('models.Model',),
        'o2o': ('models.Model',),
    }

    try:
        res = item(*args_map.get(key, ()), )
    except Exception as exc:
        print(' -- Issue with', key, exc)
        raise exc

    field_name = res.__class__.__name__
    field_module = res.__class__.__module__
    doc = item.__doc__
    if doc:
        doc = dedent(doc)

    return {
        'func': item,
        'func_name': _name,
        'key': key,
        'result': res,
        'field_name': field_name,
        'field_module': field_module,
        'doc': doc,
    }


if __name__ == '__main__':
    v = main()
