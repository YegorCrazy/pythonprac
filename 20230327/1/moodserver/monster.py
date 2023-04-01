"""Module with Monster class."""

import cowsay

CUSTOM_MONSTERS = ['jgsbat']


class Monster:
    """Monster class."""

    def __init__(self, name, greeting, hp):
        self.greeting = greeting
        self.name = name
        self.hp = hp
        if name in CUSTOM_MONSTERS:
            with open('./custom_cows/' + name + '.cow', 'r') as cowfile:
                self.cowfile = cowsay.read_dot_cow(cowfile)
            self.is_custom = True
        else:
            self.is_custom = False

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
