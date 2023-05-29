"""Module with functions to perform attack command."""
import shlex

PLAYER_WEAPONS = [
    'sword',
    'spear',
    'axe'
    ]


def MakeAttackMessage(monster_name, damage):
    """Make a attack request."""
    # сюда приходят координаты в формате (гор, вер)
    return shlex.join(["attack", monster_name, str(damage)])


def PerformAttackCommand(network_adapter, monster_name, damage):
    """Perform a attack command."""
    network_adapter.SendInfoToServerWithoutResponse(
        MakeAttackMessage(monster_name, damage)
        )
