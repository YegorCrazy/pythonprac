from fractions import Fraction

args = input().split(", ")
new_args = []
for x in args:
    new_args.append(Fraction(str(x)))

s = new_args[0]
w = new_args[1]

fr_1 = Fraction(1)
for i in range(new_args[2]):
    
