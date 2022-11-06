import math

class Grange:
    def __init__(self, b0, q, bn):
        self.b0 = b0
        self.q = q
        self.bn = bn
    def __len__(self):
        return math.ceil(math.log(self.bn / self.b0, self.q))
    def __iter__(self):
        return iter([self.b0 * (self.q ** n) for n in range(len(self))])
    def __getitem__(self, index):
        if type(index) == type(slice(1)):
            return Grange(index.start, self.q if index.step == None else self.q ** index.step, index.stop)
        return self.b0 * (self.q ** index)
    def __str__(self):
        return f'grange({self.b0}, {self.q}, {self.bn})'
    def __repr__(self):
        return f'grange({self.b0}, {self.q}, {self.bn})'

import sys
exec(sys.stdin.read())
