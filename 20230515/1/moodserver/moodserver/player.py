"""Module with Player class."""

from .utils import InvertCoordinates
from .response import Response

PLAYER_DAMAGE = {
    'sword': 10,
    'spear': 15,
    'axe': 20
    }


class Player:
    """Player class."""

    def __init__(self, dungeon, nickname):
        self.dungeon = dungeon
        self.nickname = nickname
        # позиция задается как координаты в массиве,
        # то есть (вер, гор)
        self.position = [0, 0]
        dungeon.AddPlayer(self)

    def ChangePosition(self, new_pos):
        """Change player position and return after-move message."""
        self.position = new_pos
        return self.MakeAfterMoveMessage()

    def MakeAfterMoveMessage(self):
        """Make after-move message."""
        # чтобы вывести в человеческом формате, надо
        # инвертировать координаты
        output_pos = InvertCoordinates(self.position)
        return Response('Moved to ({}, {})', [output_pos[0], output_pos[1]],
                        'personal')

    def Move(self, x, y):
        """Try to move a player through the dungeon."""
        responses = self.dungeon.MovePlayer(self, x, y)
        return responses

    def Attack(self, monster_name, weapon, player_name):
        """Attack a monster by it's name."""
        return self.dungeon.PerformPlayerAttack(self, monster_name,
                                                weapon, player_name)
