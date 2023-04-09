"""Module with main server functions."""

import shlex
import asyncio
from .dungeon import Dungeon
from .player import Player
from .response import Response

# ВНИМАНИЕ, ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
dungeon_size = [10, 10]
dungeon = Dungeon(dungeon_size)
occupied_names = set()
clients = {}


def PerformCommand(command, player, dungeon, player_name):
    """
    Perform server command.

    Parse a command to server, perform it and
    return an array of Responses.
    """
    match command[0]:
        case "sayall":
            return [Response(shlex.join([player_name + ':'] + command[1:]),
                             'broadcast')]
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


async def ManageCommand(reader, writer):
    """
    A server function.

    Login a player, get commands from it, send responses
    to him and other players and close connection.
    """
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
                    writer.write("error\n".encode())
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
    """Server start and serve function."""
    server = await asyncio.start_server(ManageCommand, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()