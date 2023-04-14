"""Module with main server functions."""

import shlex
import asyncio
from .dungeon import Dungeon, MoveMonsters
from .player import Player
from .response import Response
from .l10n import TranslateWithInsertions

# ВНИМАНИЕ, ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
occupied_names = set()
clients = {}
clients_locales = {}

async def ManageResponses(responses, me=None):
    """
    Send messages to players.

    Put messages to player's queues. Player's names are
    got from response "player" field or "me" argument.
    """
    global clients
    for response in responses:
        if response.send_method == 'broadcast':
            for client in clients:
                locale = clients_locales[client]
                text_to_send = TranslateWithInsertions(response.text,
                                                       response.insert_values,
                                                       locale)
                await clients[client].put(text_to_send)
        elif response.send_method == 'personal':
            if me is None and response.player is None:
                raise Exception('don\'t know where to send message')
            send_to = me if me is not None else response.player
            text_to_send = TranslateWithInsertions(response.text,
                                                   response.insert_values,
                                                   clients_locales[send_to])
            await clients[send_to].put(text_to_send)
        elif response.send_method == 'others':
            if me is None and response.player is None:
                raise Exception('don\'t know where to send message')
            not_send_to = me if me is not None else response.player
            for client in clients:
                if client != not_send_to:
                    locale = clients_locales[client]
                    text_to_send = TranslateWithInsertions(response.text,
                                                           response.insert_values,
                                                           locale)
                    await clients[client].put(text_to_send)


# ВНИМАНИЕ, ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
dungeon_size = [10, 10]
dungeon = Dungeon(dungeon_size, ManageResponses)


def PerformCommand(command, player, dungeon, player_name):
    """
    Perform server command.

    Parse a command to server, perform it and
    return an array of Responses.
    """
    match command[0]:
        case "sayall":
            return [Response(shlex.join([player_name + ':'] + command[1:]), [],
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

connected_message_template = '{} was connected'
disconnected_message_template = '{} was disconnected'

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
    print(connected_message_template.format(me))
    global dungeon
    global clients
    # очередь игрока me тут еще не создана
    await ManageResponses([Response(connected_message_template, [me], 'broadcast')])
    player = Player(dungeon, me)
    clients_locales[me] = 'en'
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
                    elif command[0] == 'locale':
                        clients_locales[me] = command[1]
                        await ManageResponses([Response('Set {} locale', [command[1]],
                                                        'personal')], me)
                    else:
                        responses = PerformCommand(command, player, dungeon, me)
                        await ManageResponses(responses, me)
                except Exception as ex:
                    print(ex)
                    writer.write("error\n".encode())
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(disconnected_message_template.format(me))
    del clients[me]
    del clients_locales[me]
    # очередь игрока me уже удалена
    await ManageResponses([Response(disconnected_message_template, [me], 'broadcast')])
    occupied_names.remove(me)
    writer.close()
    await writer.wait_closed()


async def Main():
    """Server start and serve function."""
    to_run = await asyncio.gather(asyncio.start_server(ManageCommand,
                                                       '0.0.0.0',
                                                       1337),
                                  MoveMonsters(dungeon))
    async with to_run:
        await to_run.serve_forever()
