from collections import UserString

class DivStr(UserString):
    def __init__(self, data=None):
        if data == None:
            self.data = ''
        else:
            super().__init__(data)
    def __floordiv__(self, n):
        res = []
        len_str = len(self.data) // n
        for i in range(n):
            res += [self.__class__(self.data[i * len_str : (i + 1) * len_str])]
        return iter(res)
    def __mod__(self, n):
        len_str = len(self.data) % n
        return self.__class__(self.data[-len_str:])

import sys
exec(sys.stdin.read())
