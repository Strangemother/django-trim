import os

import json
import argparse
from pathlib import Path

import appdirs

register = { 'functions': ()}
# # create the parser for the "a" command
# parser_a = subparsers.add_parser('add', help='a help', aliases=['a'])
# parser_a.add_argument('bar', type=int, help='bar help')

class Help:
    primary = "Application primary help"
    scripts = 'Work with the loaded trim scripts'
    add = 'Add a script to the loadout'
    add_filename = 'Provide the file for loading.'


class ConfigMixin(object):

    def get_conf(self):
        """Collect a data object from JSON representation as a persistent user
        config file.

            data = self.get_conf()
            data['change'] = 1
            self.write_conf_data(data)
        """
        # info_point = appdirs.user_data_dir('v1', 'django-trim')
        # # look at base location
        # init_path = Path(info_point) / 'trim-config.json'
        conf_path = self.get_conf_path()

        data = {}
        if conf_path.exists():
            try:
                data = json.loads(conf_path.read_text())
            except json.decoder.JSONDecodeError:
                print("The pointer config file is not JSON. Failing early.")
        return data

    def get_conf_path(self):
        info_point = appdirs.user_data_dir('v1', 'django-trim')
        # look at base location
        init_path = Path(info_point) / 'trim-config.json'
        conf_path = init_path

        if conf_path.exists():
            # load as json, test for pointer.
            print('Loading path.', conf_path)
            data = json.loads(conf_path.read_text())
            pointer = data.get('pointer', None)
            if pointer is not None:
                print('Pointer path.', pointer)
                conf_path = Path(pointer)
        return conf_path

    def write_conf_data(self, data, path=None):
        """Write a data object as JSON representation to the persistent user
        config file.

            data = self.get_conf()
            data['change'] = 1
            self.write_conf_data(data)
        """
        path = path or self.get_conf_path()
        jd = json.dumps(data, indent=4)
        try:
            path.write_text(jd)
        except FileNotFoundError as err:
            if path.parent.exists() is False:
                os.makedirs(path.parent)
            path.write_text(jd)


class AppFunction(ConfigMixin):
    """The AppFunction loadout helps to build attachments to the argparser.
     Apply this class to the AppActions app_functions to insanstiate during a prep.

     The class is ran against the AppActions to manipulate the argparser options.
     For convenience a few functions abstract the cli argument. The 'prep' function
     assumes a `hook` and `setup_args` function exist

        class ScriptAdd(AppFunction):
            # parent_name = 'scripts'
            parent_name = None
            name = 'add'
            help = Help.add

            def setup_args(self, parser):
                parser.add_argument('filename', type=Path, help=Help.add_filename)
                parser.add_argument('--name', type=str, default=None, )

            def hook(self, parsed, *args, **kwargs):
                print('hook', parsed)
                data = self.get_conf()
                name = parsed.name or parsed.filename.stem
                data[name] = parsed.filename.absolute().as_posix()
                self.write_conf_data(data)

                return 'res from hook'

     If the parent name is none, the function appends as a parser. If the parent
     name exists, the function appends as a subparser of the positioned parent.

        class Script(AppFunction):
            name = 'scripts'
            help = Help.scripts


        class ScriptAdd(AppFunction):
            parent_name = 'scripts'
            name = 'add'
            help = Help.add

    """
    # parent_name = 'scripts'
    parent_name = None
    name = None
    help = None
    arguments = None
    auto_register = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # print('Register', cls)
        if cls.auto_register is True:
            register['functions'] += (cls, )

    def prep(self, app):
        """Prepare the tool with the pre-baked loadouts such as the help and
        scripts.
        """
        parser = self.hook_parser(app)
        for A in (self.arguments or ()):
            A().prep(app)
        if parser:
            self.setup_args(parser)
        return parser

    def hook_parser(self, app):
        pname = self.parent_name
        cname = self.name or self.__class__.__name__.lower()
        mypath = f'{app.primary_name}.{pname}'
        if pname is not None:
            return app.add_sub_to(mypath, self.hook, cname, help=self.help)
        return app.add_sub(self.hook, cname, help=self.help)

    def setup_args(self, parser):
        pass

    def hook(self, parsed, *args, **kwargs):
        pass


class AppArgument(AppFunction):
    """Append an agument in the form of a switch to an existing parser.


        class ScriptsAddFilenameArg(AppArgument):

            target ='scripts.add'

            def setup_args(self, parser):
                parser.add_argument('filename', type=Path)
                parser.add_argument('-n', '--name')

        AppArguments do not automatically register to the load lib as they
        may optionally append to a parent manually.
    """
    target = None
    # auto_register = False

    def hook_parser(self, app):
        parser = self.get_parser(app, self.target)
        return parser

    def get_parser(self, app, name=None):
        try:
            r = app.get_parser(name)
            return r
        except NoPosition:
            pass


class NoPosition(Exception):
    pass


class AppActions(ConfigMixin):
    prog_name = 'PROG'
    primary_name = 'primary'

    def __init__(self):
        self._subparsers = {}
        self.args = None
        self.parser = None
        self.positions = {}
        self.app_functions = ()
        self.setup()

    def setup(self):
        pass

    def prep(self):
        """Prepare the tool with the pre-baked loadouts such as the help and
        scripts.
        """
        # scripts_name = 'scripts'
        # self.add_sub(self.scripts_func, scripts_name, help=Help.scripts)
        reg = register['functions']
        for AppFuncClass in self.app_functions + reg:
            AppFuncClass().prep(self)

    def get_subparser(self, parser=None):
        """Return the 'subparser' of a given parent parser;
        such as "bar for "$foo bar". If the parent parser is not given, use
        the primary parser.
        """
        parser = parser or self.get_primary_parser()

        if self._subparsers.get(parser) is None:
            subparsers = parser.add_subparsers(help='sub-command help')
            subparsers._parent = parser._name
            self._subparsers[parser] = subparsers
        return self._subparsers[parser]

    def add_sub(self, func, name, parser=None, **kwargs):
        """Add a subparser function as the "name" to a parent parser.
        If the parent parser is not given, use the primary.

        This function applied the default function and stored the positio for
        later rebinding.

            add_parser = self.add_sub(self.scripts_func, 'scripts', help=Help.scripts)
            #positions[primary.scripts] == add_parser
        """
        # create the parser for the "b" command
        subparsers = self.get_subparser(parser)
        parser_b = subparsers.add_parser(name, **kwargs)
        parser_b._name = name
        # parser_b.add_argument('--baz', choices='XYZ', help='baz help')
        parser_b.set_defaults(func=func)
        position = f"{subparsers._parent}.{name}"
        self.positions[position] = parser_b
        return parser_b

    def add_sub_to(self, position_name, func, name, **kwargs):
        """Simplify the creation of a sub loader to an expected position:

            self.add_sub(self.scripts_func, 'add', 'primary.scripts', help=Help.scripts)
        """
        return self.add_sub(func, name, self.positions[position_name], **kwargs)

    def get_primary_parser(self):
        """Return the primary parser for the program. If the internal self.parser
        is undefined, create a new 'primary' and return it.
        """
        if self.parser is None:
            parser = argparse.ArgumentParser(prog=self.prog_name)
            parser._name = self.primary_name
            # parser.add_argument('--foo', action='store_true', help='foo help')
            parser.set_defaults(func=self.default_caller)
            self.parser = parser
        return self.parser

    def get_parser(self, name=None):
        if name in [None, 'primary', self.primary_name]:
            return self.get_primary_parser()
        try:
            return self.positions[name]
        except KeyError as err:
            s = f'No key "{name}" - available: {self.positions.keys()}'
            raise NoPosition(s)

    def parse_args(self, args=None):
        self.args = args_unit = self.parser.parse_args(args)
        return args_unit

    def get_parsed_args(self, args=None):
        if self.args is None:
            return self.parse_args(args)
        return self.args

    def run_hook(self, *args, **kwargs):
        arg_unit = self.get_parsed_args()
        func = arg_unit.func
        return func(arg_unit, *args, **kwargs)
