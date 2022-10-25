def fib(m, n):
    a, b = 1, 1
    for i in range(m - 1):
        a, b = b, a + b
    for i in range(m - 1, n):
        yield b
        a, b = b, a + b

import sys
exec(sys.stdin.read())
