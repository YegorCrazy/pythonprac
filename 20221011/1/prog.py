from fractions import Fraction

def count_fr (args, start, s):
    fr = args[start]
    for i in range(int(args[start - 1])):
        fr *= s
        fr += args[start + i + 1]
    return fr

def is_root (args):
    s = args[0]
    w = args[1]

    start = 3
    fr_1 = count_fr(args, start, s)
    start = start + int(args[2]) + 2
    fr_2 = count_fr(args, start, s)

    return fr_1 / fr_2 == w

args = input().split(", ")
new_args = []
for x in args:
    new_args.append(Fraction(str(x)))

print(is_root(new_args))



