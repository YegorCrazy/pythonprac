m, n = eval(input())
print([x for x in range(m, n) if x >= 2 and all([x % i for i in range(2, x)])])
