"""Module with Monster class."""

import cowsay
import os

CUSTOM_MONSTERS = ['jgsbat']


class Monster:
    """Monster class."""

    def __init__(self, name, greeting, hp, position):
        self.greeting = greeting
        self.name = name
        self.hp = hp
        # позиция задается как координаты в массиве,
        # то есть (вер, гор)
        self.position = position
        if name in CUSTOM_MONSTERS:
            path_to_directory = os.path.dirname(os.path.abspath(__file__))
            with open(path_to_directory +
                      '/custom_cows/' + name + '.cow', 'r') as cowfile:
                self.cowfile = cowsay.read_dot_cow(cowfile)
            self.is_custom = True
        else:
            self.is_custom = False

    def ChangePosition(self, new_pos):
        """Change monster position."""
        self.position = new_pos

    def ImpactOnPlayer(self, player):
        """
        Impact on player.

        Impact on player on the same dungeon cell
        and return player messages.
        """
        return self.SayGreetings()

    def SayGreetings(self):
        """
        Say greetings to player.

        Render a monster picture saying greetings and
        return it.
        """
        if self.is_custom:
            return cowsay.cowsay(self.greeting, cowfile=self.cowfile)
        else:
            return cowsay.cowsay(self.greeting, cow=self.name)

    def GetAttacked(self, damage):
        """Get attacked by player."""
        if self.hp > damage:
            self.hp -= damage
            return damage
        else:
            damage = self.hp
            self.hp = 0
            return damage
