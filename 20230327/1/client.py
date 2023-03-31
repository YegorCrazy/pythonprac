import sys
import socket
import cowsay
import shlex
import cmd
import threading
import readline

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

    def SendInfoToServerWithoutResponse(self, msg):
        self.socket.sendall((msg + '\n').encode())

    def GetInfoFromServer(self):
        return self.socket.recv(1024).decode()

    def CloseSocket(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


def PrintMessageFromNetworkAdapterToCmd(network_adapter, cmd):
    while (network_adapter.socket.fileno() == -1 or
           (message := network_adapter.GetInfoFromServer())):
        print(f"\n{message}{cmd.prompt}{readline.get_line_buffer()}",
              end="", flush=True)


def MakeMoveMessage(x, y):
    # передаем как (гор, вер)
    return shlex.join(["move", str(x), str(y)])


def PerformMoveCommand(network_adapter, x, y):
    network_adapter.SendInfoToServerWithoutResponse(
        MakeMoveMessage(x, y)
        )


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


def PerformAddmonCommand(network_adapter, monster_options):
    network_adapter.SendInfoToServerWithoutResponse(
        MakeAddmonMessage(monster_options)
        )


def MakeAttackMessage(monster_name, damage):
    # сюда приходят координаты в формате (гор, вер)
    return shlex.join(["attack", monster_name, str(damage)])


def PerformAttackCommand(network_adapter, monster_name, damage):
    network_adapter.SendInfoToServerWithoutResponse(
        MakeAttackMessage(monster_name, damage)
        )


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
            return [weapon for weapon in PLAYER_WEAPONS
                    if weapon.startswith(text)]
        else:
            if len(line.split()) == 2 or (len(line.split()) == 3
                                          and 'with'.startswith(text)):
                return ['with']

    def do_sayall(self, args):
        self.network_adapter.SendInfoToServerWithoutResponse(
            'sayall ' + args.strip())

    def do_quit(self, args):
        self.network_adapter.CloseSocket()
        return True


if __name__ == '__main__':
    # аргументы: имя хост [порт]
    if len(sys.argv) < 2:
        print('username not specified')
        exit()
    name = sys.argv[1]
    if len(sys.argv) < 3:
        print('server host not specified')
        exit()
    host = sys.argv[2]
    if len(sys.argv) > 3:
        port = int(sys.argv[3])
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
        resp = shell.network_adapter.SendInfoToServer("login " + name)
        if resp == 'no':
            print(f'name {name} is occupied, try another one')
            exit()
        elif resp == 'ok':
            print(f'logined as {name}')
            server_messages_getter = threading.Thread(
                target=PrintMessageFromNetworkAdapterToCmd,
                args=(shell.network_adapter, shell))
            server_messages_getter.start()
            print('<<< Welcome to Python-MUD 0.1 >>>')
            shell.cmdloop()
