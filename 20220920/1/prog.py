def simb (a):
    if a:
        return '+'
    else:
        return '-'

a = int(input())

print('A', simb((a % 25 == 0) and (a % 2 == 0)),
      'B', simb((a % 25 == 0) and (a % 2 == 1)),
      'C', simb(a % 8 == 0),
      sep = ' ')
