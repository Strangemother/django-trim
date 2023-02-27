from .base import AppActions, Help as BHelp, AppFunction, AppArgument, ConfigMixin, print_help, SubHelpFormatter
from pathlib import Path
from functools import partial
import shlex
from trim import execute

import argparse


# def print_help(parser):

#     # retrieve subparsers from parser
#     subparsers_actions = [
#         action for action in parser._actions
#         if isinstance(action, argparse._SubParsersAction)]
#     # there will probably only be one subparser_action,
#     # but better safe than sorry
#     for subparsers_action in subparsers_actions:
#         # get all subparsers and print help

#         for choice, subparser in subparsers_action.choices.items():
#             print("--- Subparser '{}'".format(choice))
#             subparser.formatter_class = SubHelpFormatter
#             print(subparser.format_help())

class Help(BHelp):
    double_dash = ('apply a double-switch before the '
                    'input to ensure switch aggregation.')
    pattern_append = ('Append a partial string to the filename split pattern')


class GraphApps(object):
    verbose = 0

    def build_graph_parsers(self, top, parser=None, depth=0, position=None):
        """Given a nested tree of parsers build sub apps into the argparser

            {
                "graph": {
                    "keys": [
                        "download",
                    ],
                    "download": {
                        "depth": 0,
                        "keys": ["db"],
                        "position": ["db"],
                        "items": [
                            "download"
                        ],
                        "db": {
                            "depth": 1,
                            "keys": [],
                            "position": [],
                            "items": [
                                "db"
                            ]
                        }
                    }
                },
                "db": "py scripts/download_remote.py"
            }

            trim download db
        """
        for key in top.get('keys', ()):
            data = top[key]
            inner_keys = data.get('keys', ())
            position = tuple(data.get('position', ()))
            position = (position or ()) + (key,)
            if self.verbose > 0:
                w =' ' * depth
                print(w, 'Adding', position)
            # build a caller
            func = partial(self.depthed_default_caller, data)
            # Push into the parsers
            sub_parser = self.add_sub(func, key, parser, formatter_class=SubHelpFormatter)
            # recurse.
            self.build_graph_parsers(data, sub_parser, depth=depth+1, position=position)

    def depthed_default_caller(self, content, args=None):
        items = content.get('items', ())
        conf = self.get_conf()
        datas = {x:conf.get(x) for x in items}
        self.namespace = args
        self.run_units(datas)
        return 'res from default_caller'

    def run_units(self, datas):
        # print('\nKey', datas)
        # print('  default_caller: Key', self.namespace)
        for i, (k, d) in enumerate(datas.items()):
            self.execute_step(i, k, d)

    def execute_step(self, i, k, d):
        pass


class StepExecute(object):

    def execute_step(self, i, k, d):
        # Shell true, because the user is building the scripts.
        command = shlex.split(d)
        command += self.namespace.unknown_args
        print('  Running', k, ' -> ', command)
        execute.read_one_stream_command(command)


class TrimApp(AppActions, StepExecute, GraphApps):
    """TrimApp extends AppActions to present provide trim app functions
    for the CLI

    """
    prog_name = 'trim'
    primary_name = 'trim'

    def setup(self):
        conf = self.get_conf()
        graph = conf.get('graph', {})
        self.verbose = conf.get('verbose', 0)
        self.build_graph_parsers(graph)

    def scripts_func(self, args):
        print('scripts_func', args)
        return 'res from scripts_func'

    def default_caller(self, args):
        print_help(self.get_primary_parser())
        return 'res from default_caller'

    def add(self, *app_function):
        self.app_functions += app_function


class TrimAdminApp(TrimApp):
    register_name = 'admin'

    def get_conf(self):
        return {}


class VerboseSwitch(AppArgument):

    def setup_args(self, parser):
        parser.add_argument('--verbose', '-v', action='count', default=0)


class VersionSwitch(AppArgument):
    _version = '1.0'
    target =  'primary'

    def setup_args(self, parser):
        parser.add_argument('--version',
                    action='version',
                    version=f'%(prog)s {self._version}'
                )


class Scripts(AppFunction):
    # name = 'scripts'
    help = Help.scripts
    register_name ='admin'


class ScriptsAddFilenameArg(AppArgument):
    """The 'filename' argument for the `scripts add` function.

    This is applied through the `arguments` of ScriptsAdd.

    As this defines early, it will fail the primary hook parser.
    """
    target ='scripts.add'

    def setup_args(self, parser):
        parser.add_argument('filename', type=str, nargs='*', help=Help.add_filename, default='.')
        parser.add_argument('--', dest='_', nargs='+', type=str, default=None, help=Help.double_dash)
        parser.add_argument('--type', type=str, default='raw', choices=('raw', 'path',))
        parser.add_argument('-n', '--name', type=str, default=None, )
        parser.add_argument('-d', '--dry', action='store_true', )
        parser.add_argument('-f', '--dry-full', action='store_true', )
        parser.add_argument('-p', '--pattern', type=str, default=None)
        parser.add_argument('-pa', '--pattern-append', type=str, default=None, help=Help.pattern_append)


import re
from pprint import pprint as pp


class DefaultHelp(AppArgument):
    target = 'primary'

    def setup_args(self, parser):
        # parser.add_help = False
        del parser._option_string_actions['--help']
        del parser._option_string_actions['-h']
        parser.add_argument('-h', '--help', action='help')
        # parser.set_defaults(func=self.caller)

    def caller(self, *args, **kwargs):
        print('HELP', args, kwargs)

    # def prep(self, parser):
    #     print('DefaultHelp.prep')
    #     parser.primary_init_kwargs['add_help'] = False
    #     return super().prep(parser)


class ScriptInstall(ConfigMixin):
    """Install a script given through the CLI by file.
    """

    def parse_script_path_place(self, parsed, **kwargs):
        return parsed.filename.absolute().as_posix()

    def parse_raw_path_place(self, parsed, **kwargs):
        return str(parsed.filename)

    def as_path(self, parts):
        return Path(''.join(parts))

    def install(self, parsed, **kwargs):
        path = getattr(self, f'parse_{parsed.type}_path_place')(parsed, **kwargs)

        name = parsed.name or self.as_path(parsed.filename).stem
        parts = self.parse_name(name, parsed.pattern_append, parsed.pattern)
        print('Installing', name)
        data = self.get_conf()
        if parsed.dry:
            r = self.append_graph(data if parsed.dry_full else {}, parts, name)
            r[name] = path
            pp(r)
            return
        self.append_graph(data, parts, name)
        data[name] = path
        self.write_conf_data(data)

    def append_graph(self, data, parts, name, graph=None):

        graph = graph or data.get('graph', None)
        if 'graph' not in data:
            data['graph'] = { 'keys': []}
        leaf = data['graph']

        for i, part in enumerate(parts):
            if part not in leaf:
                print('Add leaf', part)
                leaf[part] = {'depth': i, 'keys': [], 'position': parts[0: i] }
            keys = set(leaf['keys'])
            keys.add(part)
            leaf['keys'] = tuple(keys)
            leaf = leaf[part]

        items = set(leaf.get('items') or [])
        items.add(name)
        leaf['items'] = tuple(items)
        return data

    def parse_name(self, name, append_pattern='', pattern=None):
        safe_ap = append_pattern or ''
        pattern = pattern or f"[_ -{safe_ap}]"
        return re.split(pattern, name)


class ScriptsAdd(AppFunction):
    """The "scripts add [filename]" command for installing a command into
    the persistent store.
    """
    parent_name = 'scripts'
    name = 'add'
    help = Help.add
    register_name ='admin'

    arguments = (ScriptsAddFilenameArg,)

    def hook(self, parsed, *args, **kwargs):
        print('hook', parsed)
        si = ScriptInstall()
        si.install(parsed, **kwargs)
        return 'res from hook'


actions = TrimApp()
# actions.add(VerboseSwitch, VersionSwitch, Scripts, ScriptsAdd, ScriptsAddFilenameArg)
actions.prep()

admin_actions = TrimAdminApp()
admin_actions.add(AppActions, Scripts)
# admin_actions.add(VerboseSwitch, VersionSwitch, Scripts, ScriptsAdd, ScriptsAddFilenameArg)
admin_actions.prep()


def main():
    print('Entry from main')
    actions.run_hook()


def main_admin():
    print('Admin entry from main')
    admin_actions.run_hook()
