class Undead(Exception):
    pass

class Skeleton(Undead):
    pass

class Zombie(Undead):
    pass

class Ghoul(Undead):
    pass

def necro(a):
    if a % 3 == 0:
        raise Skeleton
    elif a % 3 == 1:
        raise Zombie
    else:
        raise Ghoul

if __name__ == '__main__':
    a, b = eval(input())
    for i in range(a, b):
        try:
            necro(i)
        except Skeleton:
            print('Skeleton')
        except Zombie:
            print('Zombie')
        except Undead:
            print('Generic Undead')
