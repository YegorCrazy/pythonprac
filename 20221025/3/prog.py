import itertools
print(*list(filter(lambda s: s.count("TOR") == 2, [''.join(x) for x in itertools.product('ORT', repeat=int(input()))])), sep=', ')
