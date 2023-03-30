import sys
import socket
import cowsay
import shlex
import cmd

CUSTOM_MONSTERS = ['jgsbat']

MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY = {
    'hello': 1,
    'coords': 2,
    'hp': 1
    }

PLAYER_WEAPONS = [
    'sword',
    'spear',
    'axe'
    ]


class UnknownMonsterException(Exception):
    pass


class UndefinedParameterException(Exception):

    def __init__(self, param_name):
        self.param_name = param_name


def GetAvailableMonsters():
    return cowsay.list_cows() + CUSTOM_MONSTERS


class NetworkAdapter:
    def __init__(self, server_host, server_port=1337):
        self.server_host = server_host
        self.server_port = server_port

    def OpenSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))

    def SendInfoToServer(self, msg):
        self.socket.sendall((msg + '\n').encode())
        response = self.socket.recv(1024).decode()
        return response

    def CloseSocket(self):
        self.socket.close()


def MakeMoveMessage(x, y):
    # передаем как (гор, вер)
    return shlex.join(["move", str(x), str(y)])


def PrintSuccessMoveMessage(response):
    # получаем как (гор, вер)
    new_x, new_y = response[1], response[2]
    print(f'Moved to ({new_x}, {new_y})')
    if len(response) > 3:
        monster_name = response[3]
        monster_greeting = response[4]
        if monster_name in CUSTOM_MONSTERS:
            with open(monster_name + '.cow', 'r') as file:
                cowfile = cowsay.read_dot_cow(file)
                print(cowsay.cowsay(monster_greeting,
                                    cowfile=cowfile))
        else:
            print(cowsay.cowsay(monster_greeting,
                                cow=monster_name))


def PerformMoveCommand(network_adapter, x, y):
    response = network_adapter.SendInfoToServer(
        MakeMoveMessage(x, y)
        )
    response = shlex.split(response)
    if response[0] == 'ok':
        PrintSuccessMoveMessage(response)
    else:
        print('Internal error while moving')


class MonsterCreationParams:

    def __init__(self, name, greeting, coords, hp):
        self.name = name
        self.greeting = greeting
        self.coords = list(map(int, coords))
        self.hp = int(hp)


def GetMonsterCreationParams(args):
    monster_name = args[0]  # имя монстра всегда первое
    if monster_name not in GetAvailableMonsters():
        raise UnknownMonsterException
    params = [monster_name]
    for param_name in MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY.keys():
        if param_name not in args:
            raise UndefinedParameterException(param_name)
        index = args.index(param_name)
        if MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY[param_name] == 1:
            params.append(args[index + 1])
        else:
            param_value = []
            param_quantity = MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY[
                param_name
                ]
            for i in range(index + 1,
                           index + 1 + param_quantity
                           ):
                param_value.append(args[i])
            params.append(param_value)
    return MonsterCreationParams(*params)


def MakeAddmonMessage(monster_options):
    # сюда приходят координаты в формате (гор, вер)
    return shlex.join(["addmon", monster_options.name,
                       monster_options.greeting,
                       str(monster_options.coords[0]),
                       str(monster_options.coords[1]),
                       str(monster_options.hp)])


def PrintSuccessAddmonMessage(response, monster_options):
    print(f'Added monster {monster_options.name} to '
          f'({monster_options.coords[0]}, {monster_options.coords[1]}) '
          f'saying {monster_options.greeting}')
    if len(response) > 1:
        print('Replaced the old monster')


def PerformAddmonCommand(network_adapter, monster_options):
    response = network_adapter.SendInfoToServer(
        MakeAddmonMessage(monster_options)
        )
    response = shlex.split(response)
    if response[0] == 'ok':
        PrintSuccessAddmonMessage(response, monster_options)
    else:
        print('Internal error while adding monster')


def MakeAttackMessage(monster_name, damage):
    # сюда приходят координаты в формате (гор, вер)
    return shlex.join(["attack", monster_name, str(damage)])


def PrintSuccessAttackMessage(response, monster_name):
    damage = response[1]
    hp_left = response[2]
    print(f'Attacked {monster_name}, damage {damage} hp')
    if int(hp_left) == 0:
        print(f'{monster_name} died')
    else:
        print(f'{monster_name} now has {hp_left} hp')


def PerformAttackCommand(network_adapter, monster_name, damage):
    response = network_adapter.SendInfoToServer(
        MakeAttackMessage(monster_name, damage)
        )
    response = shlex.split(response)
    if response[0] == 'ok':
        PrintSuccessAttackMessage(response, monster_name)
    elif response[0] == 'no':
        print(f"No {monster_name} here")
    else:
        print('Internal error while attacking monster')


class MUDShell(cmd.Cmd):

    def SetNetworkAdapter(self, network_adapter):
        self.network_adapter = network_adapter

    def ActivateNetworkAdapter(self):
        self.network_adapter.OpenSocket()

    prompt = '(MUD) '

    def do_left(self, args):
        PerformMoveCommand(self.network_adapter, -1, 0)

    def do_right(self, args):
        PerformMoveCommand(self.network_adapter, 1, 0)

    def do_down(self, args):
        PerformMoveCommand(self.network_adapter, 0, 1)

    def do_up(self, args):
        PerformMoveCommand(self.network_adapter, 0, -1)

    def do_addmon(self, args):
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

    def complete_addmon(self, text, line, startidx, endidx):
        if line[:startidx].split()[-1] == 'addmon':
            return [monster for monster in GetAvailableMonsters()
                    if monster.startswith(text)]
        command_args = MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY.keys()
        if not line[:startidx].split()[-1] in command_args:
            return [arg for arg in command_args if arg.startswith(text)]

    def do_attack(self, args):
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

    def complete_attack(self, text, line, startidx, endidx):
        if line[:startidx].split()[-1] == 'attack':
            return [monster for monster in GetAvailableMonsters()
                    if monster.startswith(text)]
        elif line[:startidx].split()[-1] == 'with':
            return [weapon for weapon in PLAYER_WEAPON
                    if weapon.startswith(text)]
        else:
            if len(line.split()) == 2 or (len(line.split()) == 3
                                          and 'with'.startswith(text)):
                return ['with']

    def do_quit(self, args):
        self.network_adapter.CloseSocket()
        return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('server host not specified')
        exit()
    host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
        network_adapter = NetworkAdapter(host, port)
    else:
        network_adapter = NetworkAdapter(host)
    shell = MUDShell()
    shell.SetNetworkAdapter(network_adapter)
    try:
        shell.ActivateNetworkAdapter()
    except Exception:
        print("Can't access the server.")
    else:
        print('<<< Welcome to Python-MUD 0.1 >>>')
        shell.cmdloop()
