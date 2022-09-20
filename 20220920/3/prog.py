def num_detect (a):
    s = str(a)
    sum = 0
    for ch in s:
        sum += int(ch)
    if sum == 6:
        return ":=)"
    else:
        return s

N = int(input())
a = N

while a <= N + 2:
    b = N
    while b <= N + 2:
        print(a, '*', b, '=', num_detect(a * b), sep = ' ', end = ' ')
        b += 1
    print()
    a += 1
