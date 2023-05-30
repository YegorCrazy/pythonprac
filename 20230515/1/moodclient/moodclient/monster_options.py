"""Module with utils for monster creation."""
import cowsay

CUSTOM_MONSTERS = ['jgsbat']

MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY = {
    'hello': 1,
    'coords': 2,
    'hp': 1
    }


class UnknownMonsterException(Exception):
    """Exception to show that monster name is invalid."""

    pass


class UndefinedParameterException(Exception):
    """Exception to show that some monster creation parameter is undefined."""

    def __init__(self, param_name):
        self.param_name = param_name


def GetAvailableMonsters():
    """Get available monsters list."""
    return cowsay.list_cows() + CUSTOM_MONSTERS


class MonsterCreationParams:
    """Class containing monster creation parameters."""

    def __init__(self, name, greeting, coords, hp):
        self.name = name
        self.greeting = greeting
        self.coords = list(map(int, coords))
        self.hp = int(hp)


def GetMonsterCreationParams(args):
    """Parse monster cration parameters into MonsterCreationParams."""
    monster_name = args[0]  # имя монстра всегда первое
    if monster_name not in GetAvailableMonsters():
        raise UnknownMonsterException
    params = [monster_name]
    for param_name in MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY.keys():
        if param_name not in args:
            raise UndefinedParameterException(param_name)
        index = args.index(param_name)
        if MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY[param_name] == 1:
            params.append(args[index + 1])
        else:
            param_value = []
            param_quantity = MONSTER_CREATION_PARAMS_NAME_AND_QUANTITY[
                param_name
                ]
            for i in range(index + 1,
                           index + 1 + param_quantity
                           ):
                param_value.append(args[i])
            params.append(param_value)
    return MonsterCreationParams(*params)
