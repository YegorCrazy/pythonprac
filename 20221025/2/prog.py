import itertools

def slide(seq, n):
    start = 0
    while True:
        res = itertools.tee(seq, 3)
        copy = res[0]
        seq = res[1]
        copy_slice = itertools.tee(itertools.islice(copy, start, start + n))
        if len(list(copy_slice[0])) == 0:
            break
        yield from copy_slice[1]
        start += 1

import sys
exec(sys.stdin.read())

