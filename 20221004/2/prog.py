def compare (a, b):
    if a[0] <= b[0] and a[1] <= b[1] and (a[0] < b[0] or a[1] < b[1]):
        return True
    return False

def Pareto (*pairs):
    res = []
    for pair in pairs:
        for other in pairs:
            if compare(pair, other):
                break
        else:
            res.append(pair)
    return tuple(res)

print(Pareto(*eval(input())))
