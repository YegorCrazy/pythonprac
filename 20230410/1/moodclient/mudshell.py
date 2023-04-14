"""Module with MUDShell class."""

import shlex
import cmd
from .move import PerformMoveCommand
from .monster_options import MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY
from .monster_options import UndefinedParameterException
from .monster_options import UnknownMonsterException
from .monster_options import GetMonsterCreationParams
from .monster_options import GetAvailableMonsters
from .addmon import PerformAddmonCommand
from .attack import PerformAttackCommand, PLAYER_WEAPONS

supported_languages = ['en', 'ru']

class MUDShell(cmd.Cmd):
    """Shell class."""

    def SetNetworkAdapter(self, network_adapter):  # noqa: D102
        self.network_adapter = network_adapter

    def ActivateNetworkAdapter(self):  # noqa: D102
        self.network_adapter.OpenSocket()

    prompt = '(MUD) '

    def do_left(self, args):  # noqa: D102
        PerformMoveCommand(self.network_adapter, -1, 0)

    def do_right(self, args):  # noqa: D102
        PerformMoveCommand(self.network_adapter, 1, 0)

    def do_down(self, args):  # noqa: D102
        PerformMoveCommand(self.network_adapter, 0, 1)

    def do_up(self, args):  # noqa: D102
        PerformMoveCommand(self.network_adapter, 0, -1)

    def do_addmon(self, args):  # noqa: D102
        try:
            options_splitted = shlex.split(args)
            monster_options = GetMonsterCreationParams(
                options_splitted
                )
        except UnknownMonsterException:
            print('Cannot add unknown monster')
        except UndefinedParameterException as ex:
            print('Undefined parameter:', ex.param_name)
        except Exception as ex:
            print('Invalid arguments', ex)
        else:
            PerformAddmonCommand(self.network_adapter, monster_options)

    def complete_addmon(self, text, line, startidx, endidx):  # noqa: D102
        if line[:startidx].split()[-1] == 'addmon':
            return [monster for monster in GetAvailableMonsters()
                    if monster.startswith(text)]
        command_args = MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY.keys()
        if not line[:startidx].split()[-1] in command_args:
            return [arg for arg in command_args if arg.startswith(text)]

    def do_attack(self, args):  # noqa: D102
        args = args.split()
        if len(args) < 1:
            print('Monster name not specified')
            return
        monster_name = args[0]
        if 'with' in args:
            weapon = args[args.index('with') + 1]
            if weapon not in PLAYER_WEAPONS:
                print('Unknown weapon')
                return
        else:
            weapon = 'sword'
        PerformAttackCommand(self.network_adapter,
                             monster_name,
                             weapon)

    def complete_attack(self, text, line, startidx, endidx):  # noqa: D102
        if line[:startidx].split()[-1] == 'attack':
            return [monster for monster in GetAvailableMonsters()
                    if monster.startswith(text)]
        elif line[:startidx].split()[-1] == 'with':
            return [weapon for weapon in PLAYER_WEAPONS
                    if weapon.startswith(text)]
        else:
            if len(line.split()) == 2 or (len(line.split()) == 3
                                          and 'with'.startswith(text)):
                return ['with']

    def do_sayall(self, args):  # noqa: D102
        self.network_adapter.SendInfoToServerWithoutResponse(
            'sayall ' + args.strip())

    def do_locale(self, args):  #noqa: D102
        locale = args.strip()
        if locale in supported_languages:
            self.network_adapter.SendInfoToServerWithoutResponse(
                'locale ' + locale)
        else:
            print('Unknown locale')

    def complete_locale(self, text, line, startidx, endidx):  #noqa: D102
        return [locale for locale in supported_languages
                if locale.startswith(text)]

    def do_quit(self, args):  # noqa: D102
        self.network_adapter.CloseSocket()
        return True
