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
    for i in range(10):
        try:
            necro(i)
        except Skeleton:
            print('Skeleton')
        except Zombie:
            print('Zombie')
        except Undead:
            print('Generic Undead')
