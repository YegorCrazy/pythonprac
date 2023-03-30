import sys
import socket
import shlex
import asyncio

PLAYER_DAMAGE = {
    'sword': 10,
    'spear': 15,
    'axe': 20
    }

def InvertCoordinates(const_coord):
    coord = const_coord.copy()
    coord[0], coord[1] = coord[1], coord[0]
    return coord


class Monster:

    def __init__(self, name, greeting, hp):
        self.greeting = greeting
        self.name = name
        self.hp = hp

    def ImpactOnPlayer(self, player):
        return shlex.join([self.name, self.greeting])

    def GetAttacked(self, damage):
        if self.hp > damage:
            self.hp -= damage
            return damage
        else:
            damage = self.hp
            self.hp = 0
            return damage


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
        response = 'ok'
        if replace_flag:
            response += ' replaced'
        return response

    def CheckMonster(self, player):
        # сюда приходят координаты из Player, так что тут
        # инвертировать ничего не нужно
        if self.dungeon[player.position[0]][player.position[1]] is not None:
            monster = self.dungeon[player.position[0]][player.position[1]]
            return monster.ImpactOnPlayer(player)
        else:
            return ''

    def MovePlayer(self, player, x, y):
        # сюда приходят координаты из Player, то есть
        # как в массиве, инвертируем, чтобы первая
        # координата была горизонталью, а вторая вертикалью
        # при этом (x, y) как (гор, вер)
        player_position = InvertCoordinates(player.position)
        player_position[0] = (player_position[0] + x) % self.dungeon_size[0]
        player_position[1] = (player_position[1] + y) % self.dungeon_size[1]
        # теперь обратно
        player_position = InvertCoordinates(player_position)
        response = player.ChangePosition(player_position) + ' '
        response += self.CheckMonster(player)
        return response

    def PerformPlayerAttack(self, player, monster_name, weapon_damage):
        # сюда приходят координаты из Player, то есть
        # как в массиве
        if (
            self.dungeon[player.position[0]][player.position[1]] is None
            ) or (
                self.dungeon[player.position[0]][player.position[1]].name
                != monster_name
                ):
            return "no"
        else:
            monster = self.dungeon[player.position[0]][player.position[1]]
            damage = monster.GetAttacked(weapon_damage)
            response = f'ok {damage} {monster.hp}'
            if monster.hp == 0:
                del monster
                self.dungeon[player.position[0]][player.position[1]] = None
            return response


class Player:

    def __init__(self, dungeon):
        self.dungeon = dungeon
        # позиция задается как координаты в массиве,
        # то есть (вер, гор)
        self.position = [0, 0]

    def ChangePosition(self, new_pos):
        self.position = new_pos
        return self.MakeAfterMoveMessage()

    def MakeAfterMoveMessage(self):
        # чтобы вывести в человеческом формате, надо
        # инвертировать координаты
        output_pos = InvertCoordinates(self.position)
        return f'ok {output_pos[0]} {output_pos[1]}'

    def Move(self, x, y):
        return self.dungeon.MovePlayer(self, x, y)

    def Attack(self, monster_name, weapon):
        damage = PLAYER_DAMAGE[weapon]
        return self.dungeon.PerformPlayerAttack(self, monster_name, damage)


async def ManageCommand(reader, writer):
    dungeon_size = [10, 10]
    dungeon = Dungeon(dungeon_size)
    player = Player(dungeon)
    while not reader.at_eof():
        try:
            data = await reader.readline()
            data = data.decode()
            command = shlex.split(data)
            if command == []:
                continue
            match command[0]:
                case "move":
                    # здесь x, y в формате (гор, вер)
                    x, y = command[1], command[2]
                    response = player.Move(int(x), int(y))
                    writer.write(response.encode())
                case "addmon":
                    response = dungeon.AddMonster([int(command[3]),
                                                   int(command[4])],
                                                  command[1],
                                                  command[2],
                                                  int(command[5]))
                    writer.write(response.encode())
                case "attack":
                    response = player.Attack(command[1], command[2])
                    writer.write(response.encode())
        except Exception as ex:
            print(ex)
            writer.write("error".encode())
        await writer.drain()
    writer.close()
    await writer.wait_closed()


async def Main():
    server = await asyncio.start_server(ManageCommand, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(Main())
