class DIR:
    LEFT = 'left'
    RIGHT = 'right'

while True:
    inp = input().split()
    match inp:
        case ['about']:
            print('MUD version 0.01')
        case ['credits']:
            print('Copyright (c) developers')
        case ['credits', '--year']:
            print('Copyright (c) developers 2022')
        case ['quit']:
            break
        case ['move', *direction]:
            match direction:
                case [DIR.LEFT]:
                    print('<-moved')
                case [DIR.RIGHT]:
                    print('moved->')
                case _:
                    print('Unknown movement direction')
        case ['travel', *directions]:
            match directions:
                case []:
                    print('Nowhere to travel')
                case _:
                    for d in directions:
                        match d:
                            case DIR.LEFT:
                                print('<-moved')
                            case DIR.RIGHT:
                                print('moved->')
                            case _:
                                print('Unknown travel direction')
        case _:
            print('Cannot parse')
