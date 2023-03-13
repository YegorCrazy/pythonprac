import cowsay
import shlex
import cmd

CUSTOM_MONSTERS = ['jgsbat']

MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY = {
    'hello': 1,
    'coords': 2,
    'hp': 1
    }


class UnknownMonsterException(Exception):
    pass


class UndefinedParameterException(Exception):

    def __init__(self, param_name):
        self.param_name = param_name


def GetAvailableMonsters():
    return cowsay.list_cows() + CUSTOM_MONSTERS


def InvertCoordinates(const_coord):
    coord = const_coord.copy()
    coord[0], coord[1] = coord[1], coord[0]
    return coord


class MonsterCreationParams:

    def __init__(self, name, greeting, coords, hp):
        self.name = name
        self.greeting = greeting
        self.coords = list(map(int, coords))
        self.hp = int(hp)


def GetMonsterCreationParams(args):
    params = [args[0]]  # имя монстра всегда первое
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


class Monster:

    def __init__(self, name, greeting, hp):
        if name in CUSTOM_MONSTERS:
            try:
                with open(name + '.cow', 'r') as cowfile:
                    self.cowfile = cowsay.read_dot_cow(cowfile)
                    self.is_custom = True
            except Exception:
                raise UnknownMonsterException
        elif name in cowsay.list_cows():
            self.is_custom = False
        else:
            raise UnknownMonsterException
        self.greeting = greeting
        self.name = name
        self.hp = hp

    def ImpactOnPlayer(self, player):
        self.SayGreetings()

    def SayGreetings(self):
        if self.is_custom:
            print(cowsay.cowsay(self.greeting, cowfile=self.cowfile))
        else:
            print(cowsay.cowsay(self.greeting, cow=self.name))


class Dungeon:

    def __init__(self, size):
        # size = [горизонтальный, вертикальный]
        self.dungeon_size = size
        self.dungeon = [[None for i in range(size[0])]
                        for j in range(size[1])]

    def AddMonster(self, coord, name, greeting, hp):
        # сюда приходят координаты в формате (гор, вер),
        # чтобы попасть в поле, которое задумывалось, нужно
        # инвертировать координаты
        array_coord = InvertCoordinates(coord)
        if self.dungeon[array_coord[0]][array_coord[1]] is not None:
            replace_flag = True
        else:
            replace_flag = False
        self.dungeon[array_coord[0]][array_coord[1]] = Monster(name,
                                                               greeting,
                                                               hp)
        print(f'Added monster to ({coord[0]}, {coord[1]}) '
              f'saying {greeting}')
        if replace_flag:
            print('Replaced the old monster')

    def CheckMonster(self, player):
        # сюда приходят координаты из Player, так что тут
        # инвертировать ничего не нужно
        if self.dungeon[player.position[0]][player.position[1]] is not None:
            monster = self.dungeon[player.position[0]][player.position[1]]
            monster.ImpactOnPlayer(player)

    def MovePlayerLeft(self, player):
        # сюда приходят координаты из Player, то есть
        # как в массиве, инвертируем, чтобы первая
        # координата была горизонталью, а вторая вертикалью
        player_position = InvertCoordinates(player.position)
        if player_position[0] > 0:
            player_position[0] -= 1
        else:
            player_position[0] = self.dungeon_size[0] - 1
        # теперь обратно
        player_position = InvertCoordinates(player_position)
        player.ChangePosition(player_position)
        self.CheckMonster(player)

    def MovePlayerRight(self, player):
        # сюда приходят координаты из Player, то есть
        # как в массиве, инвертируем, чтобы первая
        # координата была горизонталью, а вторая вертикалью
        player_position = InvertCoordinates(player.position)
        if player_position[0] < self.dungeon_size[0] - 1:
            player_position[0] += 1
        else:
            player_position[0] = 0
        # теперь обратно
        player_position = InvertCoordinates(player_position)
        player.ChangePosition(player_position)
        self.CheckMonster(player)

    def MovePlayerUp(self, player):
        # сюда приходят координаты из Player, то есть
        # как в массиве, инвертируем, чтобы первая
        # координата была горизонталью, а вторая вертикалью
        player_position = InvertCoordinates(player.position)
        if player_position[1] > 0:
            player_position[1] -= 1
        else:
            player_position[1] = self.dungeon_size[1] - 1
        # теперь обратно
        player_position = InvertCoordinates(player_position)
        player.ChangePosition(player_position)
        self.CheckMonster(player)

    def MovePlayerDown(self, player):
        # сюда приходят координаты из Player, то есть
        # как в массиве, инвертируем, чтобы первая
        # координата была горизонталью, а вторая вертикалью
        player_position = InvertCoordinates(player.position)
        if player_position[1] < self.dungeon_size[1] - 1:
            player_position[1] += 1
        else:
            player_position[1] = 0
        # теперь обратно
        player_position = InvertCoordinates(player_position)
        player.ChangePosition(player_position)
        self.CheckMonster(player)


class Player:

    def __init__(self, dungeon):
        self.dungeon = dungeon
        # позиция задается как координаты в массиве,
        # то есть (вер, гор)
        self.position = [0, 0]

    def ChangePosition(self, new_pos):
        self.position = new_pos
        self.PrintAfterMoveMessage()

    def PrintAfterMoveMessage(self):
        # чтобы вывести в человеческом формате, надо
        # инвертировать координаты
        output_pos = InvertCoordinates(self.position)
        print(f'Moved to ({output_pos[0]}, {output_pos[1]})')

    def MoveLeft(self):
        self.dungeon.MovePlayerLeft(self)

    def MoveRight(self):
        self.dungeon.MovePlayerRight(self)

    def MoveUp(self):
        self.dungeon.MovePlayerUp(self)

    def MoveDown(self):
        self.dungeon.MovePlayerDown(self)


class MUDShell(cmd.Cmd):

    prompt = '(MUD) '

    def do_left(self, args):
        player.MoveLeft()

    def do_right(self, args):
        player.MoveRight()

    def do_down(self, args):
        player.MoveDown()

    def do_up(self, args):
        player.MoveUp()

    def do_addmon(self, args):
        try:
            options_splitted = shlex.split(args)
            monster_options = GetMonsterCreationParams(
                options_splitted
                )
            dungeon.AddMonster(monster_options.coords,
                               monster_options.name,
                               monster_options.greeting,
                               monster_options.hp)
        except UnknownMonsterException:
            print('Cannot add unknown monster')
        except UndefinedParameterException as ex:
            print('Undefined parameter:', ex.param_name)
        except Exception as ex:
            print('Invalid arguments', ex)

    def complete_addmon(self, text, line, startidx, endidx):
        if line[:startidx].split()[-1] == 'addmon':
            return GetAvailableMonsters()
        command_args = MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY.keys()
        if not line[:startidx].split()[-1] in command_args:
            return [arg for arg in command_args if arg.startswith(text)]


if __name__ == '__main__':
    dungeon_size = [10, 10]
    dungeon = Dungeon(dungeon_size)
    player = Player(dungeon)
    print('<<< Welcome to Python-MUD 0.1 >>>')
    MUDShell().cmdloop()
