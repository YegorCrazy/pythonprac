import shlex
import asyncio
import cowsay

CUSTOM_MONSTERS = ['jgsbat']

PLAYER_DAMAGE = {
    'sword': 10,
    'spear': 15,
    'axe': 20
    }


def InvertCoordinates(const_coord):
    coord = const_coord.copy()
    coord[0], coord[1] = coord[1], coord[0]
    return coord


class Response:

    def __init__(self, text, send_method):
        assert send_method in ['broadcast', 'personal', 'others']
        self.text = text
        self.send_method = send_method


class Monster:

    def __init__(self, name, greeting, hp):
        self.greeting = greeting
        self.name = name
        self.hp = hp
        if name in CUSTOM_MONSTERS:
            self.is_custom = True
        else:
            self.is_custom = False

    def ImpactOnPlayer(self, player):
        return self.SayGreetings()

    def SayGreetings(self):
        if self.is_custom:
            return cowsay.cowsay(self.greeting, cowfile=self.cowfile)
        else:
            return cowsay.cowsay(self.greeting, cow=self.name)

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

    def AddMonster(self, coord, name, greeting, hp, player_name):
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
        personal_text = (f'Added monster to ({coord[0]}, {coord[1]}) '
                         f'saying {greeting}')
        broadcast_text = (f'{player_name} added monster to ({coord[0]}, '
                          f'{coord[1]}) saying {greeting}')
        if replace_flag:
            personal_text += '\n' + 'Replaced the old monster'
            broadcast_text += 'and replaced the old monster'
        return [Response(personal_text, 'personal'),
                Response(broadcast_text, 'others')]

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
        response = player.ChangePosition(player_position)
        monster = self.CheckMonster(player)
        if monster != '':
            response += '\n' + monster
        return response

    def PerformPlayerAttack(self, player, monster_name, weapon, player_name):
        # сюда приходят координаты из Player, то есть
        # как в массиве
        if (
            self.dungeon[player.position[0]][player.position[1]] is None
            ) or (
                self.dungeon[player.position[0]][player.position[1]].name
                != monster_name
                ):
            return [Response(f'No {monster_name} here', 'personal')]
        else:
            weapon_damage = PLAYER_DAMAGE[weapon]
            monster = self.dungeon[player.position[0]][player.position[1]]
            damage = monster.GetAttacked(weapon_damage)
            personal_text = (f'Attacked {monster_name} with {weapon}, '
                             f'damage {damage} hp')
            broadcast_text = (f'{player_name} attacked {monster_name} '
                              f'with {weapon}, damage {damage} hp')
            if monster.hp == 0:
                del monster
                self.dungeon[player.position[0]][player.position[1]] = None
                personal_text += f'\n{monster_name} died'
                broadcast_text += f'\n{monster_name} died'
            else:
                personal_text += f'\n{monster_name} now has {monster.hp} hp'
                broadcast_text += f'\n{monster_name} now has {monster.hp} hp'
            return [Response(personal_text, 'personal'),
                    Response(broadcast_text, 'others')]


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
        return f'Moved to ({output_pos[0]}, {output_pos[1]})'

    def Move(self, x, y):
        text = self.dungeon.MovePlayer(self, x, y)
        return [Response(text, 'personal')]

    def Attack(self, monster_name, weapon, player_name):
        return self.dungeon.PerformPlayerAttack(self, monster_name,
                                                weapon, player_name)


def PerformCommand(command, player, dungeon, player_name):
    match command[0]:
        case "move":
            # здесь x, y в формате (гор, вер)
            x, y = command[1], command[2]
            responses = player.Move(int(x), int(y))
            return responses
        case "addmon":
            responses = dungeon.AddMonster([int(command[3]),
                                            int(command[4])],
                                           command[1],
                                           command[2],
                                           int(command[5]),
                                           player_name)
            return responses
        case "attack":
            responses = player.Attack(command[1], command[2], player_name)
            return responses


# ВНИМАНИЕ, ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
dungeon_size = [10, 10]
dungeon = Dungeon(dungeon_size)
occupied_names = set()
clients = {}


async def ManageCommand(reader, writer):
    login_request = await reader.readline()
    login_request = shlex.split(login_request.decode())
    if login_request[0] != 'login':
        print(f'first command is not login: {login_request}')
        writer.close()
        return
    me = login_request[1]
    global occupied_names
    if me in occupied_names:
        writer.write('no'.encode())
        writer.close()
        return
    writer.write('ok'.encode())
    occupied_names.add(me)
    connected_message = f'{me} was connected'
    print(connected_message)
    global dungeon
    global clients
    # очередь игрока me тут еще не создана
    for client in clients.values():
        await client.put(connected_message)
    player = Player(dungeon)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive],
                                           return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                data = q.result().decode()
                try:
                    command = shlex.split(data)
                    if command == []:
                        continue
                    responses = PerformCommand(command, player, dungeon, me)
                    for response in responses:
                        if response.send_method == 'broadcast':
                            for client in clients.values():
                                await client.put(response.text)
                        elif response.send_method == 'personal':
                            await clients[me].put(response.text)
                        elif response.send_method == 'others':
                            for client in clients.values():
                                if client != clients[me]:
                                    await client.put(response.text)
                except Exception as ex:
                    print(ex)
                    writer.write("error".encode())
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    disconnected_message = f'{me} was disconnected'
    print(disconnected_message)
    del clients[me]
    # очередь игрока me уже удалена
    for client in clients.values():
        await client.put(disconnected_message)
    occupied_names.remove(me)
    writer.close()
    await writer.wait_closed()


async def Main():
    server = await asyncio.start_server(ManageCommand, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(Main())
