"""Module with functions to perform addmon command."""
import shlex


def MakeAddmonMessage(monster_options):
    """Make a addmon request."""
    # сюда приходят координаты в формате (гор, вер)
    return shlex.join(["addmon", monster_options.name,
                       monster_options.greeting,
                       str(monster_options.coords[0]),
                       str(monster_options.coords[1]),
                       str(monster_options.hp)])


def PerformAddmonCommand(network_adapter, monster_options):
    """Perform a addmon command."""
    network_adapter.SendInfoToServerWithoutResponse(
        MakeAddmonMessage(monster_options)
        )
