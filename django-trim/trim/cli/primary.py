from .base import AppActions, Help, AppFunction, AppArgument
from pathlib import Path


class TrimApp(AppActions):
    prog_name = 'trim'
    primary_name = 'trim'

    # def setup(self):
        # return self.prep()

    def scripts_func(self, args):
        print('scripts_func', args)
        return 'res from scripts_func'

    def default_caller(self, args):
        print('default_caller', args)
        return 'res from default_caller'

    def add(self, *app_function):
        self.app_functions += app_function


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



class ScriptsAddFilenameArg(AppArgument):
    """The 'filename' argument for the `scrpits add` function.

    This is applied through the `arguments` of ScriptsAdd.

    As this defines early, it will fail the primary hook parser.
    """
    target ='scripts.add'

    def setup_args(self, parser):
        parser.add_argument('filename', type=Path, help=Help.add_filename)
        parser.add_argument('-n', '--name', type=str, default=None, )


class ScriptsAdd(AppFunction):
    parent_name = 'scripts'
    name = 'add'
    help = Help.add
    arguments = (ScriptsAddFilenameArg,)

    def hook(self, parsed, *args, **kwargs):
        print('hook', parsed)
        data = self.get_conf()
        name = parsed.name or parsed.filename.stem
        data[name] = parsed.filename.absolute().as_posix()
        self.write_conf_data(data)

        return 'res from hook'


actions = TrimApp()
# actions.add(VerboseSwitch, VersionSwitch, Scripts, ScriptsAdd, ScriptsAddFilenameArg)
actions.prep()


def main():
    print('Entry from main')
    actions.run_hook()
