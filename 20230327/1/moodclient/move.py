"""Module with functions to perform move command."""

import shlex


def MakeMoveMessage(x, y):
    """Make a move request."""
    # передаем как (гор, вер)
    return shlex.join(["move", str(x), str(y)])


def PerformMoveCommand(network_adapter, x, y):
    """Perform a move command."""
    network_adapter.SendInfoToServerWithoutResponse(
        MakeMoveMessage(x, y)
        )
