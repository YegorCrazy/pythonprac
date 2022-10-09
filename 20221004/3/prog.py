def substract (a, b):
    try:
        return a - b
    except TypeError as err:
        if type(a)() == type(b)() == []:
            return [x for x in a if x not in b]
        elif type(a)() == type(b)() == ():
            return tuple(x for x in a if x not in b)
        else:
            raise err

print(substract(*eval(input())))
