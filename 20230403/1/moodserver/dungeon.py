"""Module with Dungeon class."""

from .utils import InvertCoordinates
from .response import Response
from .player import PLAYER_DAMAGE
from .monster import Monster


class Dungeon:
    """Dungeon class."""

    def __init__(self, size):
        # size = [горизонтальный, вертикальный]
        self.dungeon_size = size
        self.dungeon = [[None for i in range(size[0])]
                        for j in range(size[1])]
        self.players = [[dict() for i in range(size[0])]
                        for j in range(size[1])]

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

    def AddPlayer(self, player, x=0, y=0):
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

    def MovePlayer(self, player, x, y):
        """
        Move player in the dungeon.

        x and y are changes to coordinates.
        """
        # сюда приходят координаты из Player, то есть
        # как в массиве, инвертируем, чтобы первая
        # координата была горизонталью, а вторая вертикалью
        # при этом (x, y) как (гор, вер)
        player_position = InvertCoordinates(player.position)
        # удаляем игрока со старой позиции
        del self.players[player_position[0]][player_position[1]][
            player.nickname
            ]
        player_position[0] = (player_position[0] + x) % self.dungeon_size[0]
        player_position[1] = (player_position[1] + y) % self.dungeon_size[1]
        # добавляем игрока на новую позицию
        self.players[player_position[0]][player_position[1]][
            player.nickname
            ] = player
        # теперь инвертируем обратно
        player_position = InvertCoordinates(player_position)
        response = player.ChangePosition(player_position)
        monster = self.CheckMonster(player)
        if monster != '':
            response += '\n' + monster
        return response

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
