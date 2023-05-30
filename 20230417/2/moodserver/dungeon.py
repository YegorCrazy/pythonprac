"""Module with Dungeon class."""

from .utils import InvertCoordinates
from .response import Response
from .player import PLAYER_DAMAGE
from .monster import Monster
from .l10n import Translatable, NTranslatable

import random
import asyncio


async def MoveMonsters(dungeon):
    """
    Move random monster from dungeon.

    Choose random monster from dungeon and movement direction,
    move it and send info about it to players.
    """
    directions_dict = {
        'right': [1, 0],
        'left': [-1, 0],
        'down': [0, 1],
        'up': [0, -1]
        }
    while True:
        if len(dungeon.monsters) != 0:
            while True:
                monster = random.choice(list(dungeon.monsters))
                direction = random.choice(list(directions_dict.keys()))
                x_move = directions_dict[direction][0]
                y_move = directions_dict[direction][1]
                move_result = dungeon.MoveMonster(monster, x_move, y_move)
                if move_result is not False:
                    break
            responses = [Response('{} moved one cell {}',
                                  [monster.name, Translatable(direction)],
                                  'broadcast')]
            print(f'{monster.name} moved one cell '
                  f'{direction}')
            responses += move_result
            await dungeon.manage_responses_method(responses, None)
        await asyncio.sleep(30)


class Dungeon:
    """Dungeon class."""

    def __init__(self, size, manage_responses_method):
        # size = [горизонтальный, вертикальный]
        self.dungeon_size = size
        # в массивах координаты [вер][гор]
        self.dungeon = [[None for i in range(size[0])]
                        for j in range(size[1])]
        self.players = [[dict() for i in range(size[0])]
                        for j in range(size[1])]
        # массив монстров, чтобы знать, кого можно двигать
        self.monsters = set()
        self.manage_responses_method = manage_responses_method

    def AddMonster(self, coord, name, greeting, hp, player_name):
        """
        Add monster to dungeon.

        Create monster (assuming options were checked on client),
        put it into the dungeon and return messages for players.
        """
        # сюда приходят координаты в формате (гор, вер),
        # чтобы попасть в поле, которое задумывалось, нужно
        # инвертировать координаты
        array_coord = InvertCoordinates(coord)
        if self.dungeon[array_coord[0]][array_coord[1]] is not None:
            replace_flag = True
        else:
            replace_flag = False
        monster_to_add = Monster(name, greeting, hp, array_coord)
        self.dungeon[array_coord[0]][array_coord[1]] = monster_to_add
        self.monsters.add(monster_to_add)
        personal_text = 'Added monster to ({}, {}) saying {}'
        personal_insert_values = [coord[0], coord[1], greeting]
        broadcast_text = '{} added monster to ({}, {}) saying {}'
        broadcast_insert_values = [player_name, coord[0], coord[1], greeting]
        if replace_flag:
            personal_text += '\nReplaced the old monster'
            broadcast_text += ' and replaced the old monster'
        return [Response(personal_text, personal_insert_values, 'personal'),
                Response(broadcast_text, broadcast_insert_values, 'others')]

    def AddPlayer(self, player, x=0, y=0):
        """Register player in dungeon."""
        self.players[x][y][player.nickname] = player

    def CheckMonster(self, player):
        """
        Check if player meets a monster.

        Check if player meets a monster, impact to player if yes
        and return message for players.
        """
        # сюда приходят координаты из Player, так что тут
        # инвертировать ничего не нужно
        if self.dungeon[player.position[0]][player.position[1]] is not None:
            monster = self.dungeon[player.position[0]][player.position[1]]
            return monster.ImpactOnPlayer(player)
        else:
            return ''

    def CheckPlayers(self, monster):
        """
        Check if monster meets a player.

        Check if monster meets a player and return responses to them
        with "player" fields.
        """
        # сюда приходят координаты из Monster, так что тут
        # инвертировать ничего не нужно
        responses = []
        players = self.players[monster.position[0]][
            monster.position[1]].values()
        for player in players:
            text = monster.ImpactOnPlayer(player)
            responses.append(Response(text, [], 'personal', player.nickname))
        return responses

    def MoveMonster(self, monster, x, y):
        """
        Move monster in the dungeon.

        x and y are changes to coordinates.
        """
        old_monster_position = monster.position
        # сюда приходят координаты из Monster, то есть
        # как в массиве, инвертируем, чтобы первая
        # координата была горизонталью, а вторая вертикалью
        # при этом (x, y) как (гор, вер)
        monster_position = InvertCoordinates(monster.position)
        monster_position[0] = (monster_position[0] + x) % self.dungeon_size[0]
        monster_position[1] = (monster_position[1] + y) % self.dungeon_size[1]
        # теперь инвертируем обратно
        monster_position = InvertCoordinates(monster_position)
        # проверяем, нет ли монстра на клетке, куда хотим передвинуться
        # если там занято, возвращаем False и не двигаем монстра
        if self.dungeon[monster_position[0]][monster_position[1]] is not None:
            return False
        # удаляем монстра со старой позиции
        self.dungeon[old_monster_position[0]][old_monster_position[1]] = None
        # добавляем монстра на новую позицию
        self.dungeon[monster_position[0]][monster_position[1]] = monster
        monster.ChangePosition(monster_position)
        return self.CheckPlayers(monster)

    def MovePlayer(self, player, x, y):
        """
        Move player in the dungeon.

        x and y are changes to coordinates.
        """
        # удаляем игрока со старой позиции
        del self.players[player.position[0]][player.position[1]][
            player.nickname
            ]
        # сюда приходят координаты из Player, то есть
        # как в массиве, инвертируем, чтобы первая
        # координата была горизонталью, а вторая вертикалью
        # при этом (x, y) как (гор, вер)
        player_position = InvertCoordinates(player.position)
        player_position[0] = (player_position[0] + x) % self.dungeon_size[0]
        player_position[1] = (player_position[1] + y) % self.dungeon_size[1]
        # теперь инвертируем обратно
        player_position = InvertCoordinates(player_position)
        # добавляем игрока на новую позицию
        self.players[player_position[0]][player_position[1]][
            player.nickname
            ] = player
        move_response = player.ChangePosition(player_position)
        responses = [move_response]
        monster = self.CheckMonster(player)
        if monster != '':
            responses.append(Response(monster, [], 'personal'))
        return responses

    def PerformPlayerAttack(self, player, monster_name, weapon, player_name):
        """
        Perform player attack.

        Check if there is a required monster on a player cell,
        attack it and return player message
        """
        # сюда приходят координаты из Player, то есть
        # как в массиве
        if (
            self.dungeon[player.position[0]][player.position[1]] is None
            ) or (
                self.dungeon[player.position[0]][player.position[1]].name
                != monster_name
                ):
            return [Response('No {} here', [monster_name], 'personal')]
        else:
            weapon_damage = PLAYER_DAMAGE[weapon]
            monster = self.dungeon[player.position[0]][player.position[1]]
            damage = monster.GetAttacked(weapon_damage)
            personal_text = 'Attacked {} with {}, damage {} {}'
            personal_insert_values = [monster_name, Translatable(weapon),
                                      damage, NTranslatable('hp', 'hp', damage)]
            broadcast_text = '{} attacked {} with {}, damage {} {}'
            broadcast_insert_values = [player_name, monster_name, Translatable(weapon),
                                       damage, NTranslatable('hp', 'hp', damage)]
            responses = [Response(personal_text, personal_insert_values, 'personal'),
                         Response(broadcast_text, broadcast_insert_values, 'others')]
            if monster.hp == 0:
                self.dungeon[player.position[0]][player.position[1]] = None
                self.monsters.remove(monster)
                del monster
                personal_text = '{} died'
                personal_insert_values = [monster_name]
                broadcast_text = '{} died'
                broadcast_insert_values = [monster_name]
            else:
                personal_text = '{} now has {} {}'
                personal_insert_values = [monster_name, monster.hp,
                                          NTranslatable('hp', 'hp', monster.hp)]
                broadcast_text = '{} now has {} {}'
                broadcast_insert_values = [monster_name, monster.hp,
                                           NTranslatable('hp', 'hp', monster.hp)]
            responses += [Response(personal_text, personal_insert_values, 'personal'),
                          Response(broadcast_text, broadcast_insert_values, 'others')]
            return responses