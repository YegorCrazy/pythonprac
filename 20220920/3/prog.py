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
    outp = ''
    while b <= N + 2:
        outp += '{} * {} = {}'.format(a, b, num_detect(a * b))
        if b != N + 2:
            outp += ' '
        b += 1
    print(outp)
    a += 1
