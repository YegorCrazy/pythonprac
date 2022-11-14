class InvalidInput(Exception): pass
class BadTriangle(Exception): pass

def triangleSquare(s):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(s)
    except Exception:
        raise InvalidInput
    for c in [x1, y1, x2, y2, x3, y3]:
        if type(c) != type(1) and type(c) != type(1.5):
            raise BadTriangle
    sq = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2
    if sq == 0:
        raise BadTriangle
    return sq

while s := input():
    try:
        res = triangleSquare(s)
    except InvalidInput:
        print('Invalid input')
    except BadTriangle:
        print('Not a triangle')
    else:
        print('{0:.2f}'.format(res))
