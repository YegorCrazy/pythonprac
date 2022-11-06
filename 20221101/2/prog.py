def cross(p1, p2, p3, p4):
    a = (p2[0] - p1[0]) * (p1[1] - p3[1]) - (p2[1] - p1[1]) * (p1[0] - p3[0])
    b = (p4[0] - p3[0]) * (p1[1] - p3[1]) - (p4[1] - p3[1]) * (p1[0] - p3[0])
    norm = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    if norm == 0:
        return False
    return (float(a) / norm < 1) and (float(b) / norm < 1) and (float(a) / norm > 0) and (float(b) / norm > 0)

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = tuple(p1)
        self.p2 = tuple(p2)
        self.p3 = tuple(p3)
    def __abs__(self):
        return abs((self.p2[0] - self.p1[0]) * (self.p3[1] - self.p1[1]) -
                   (self.p3[0] - self.p1[0]) * (self.p2[1] - self.p1[1])) / 2
    def __bool__(self):
        return abs(self) > 0
    def __lt__(self, other):
        return abs(self) < abs(other)
    def __eq__(self, other):
        return abs(self) == abs(other)
    def __contains__(self, other):
        if type(other) == type(tuple()):
            if abs(self) == 0:
                return False
            else:
                a = [(self.p1[0] - other[0]) * (self.p2[1] - self.p1[1]) - (self.p2[0] - self.p1[0]) * (self.p1[1] - other[1]),
                     (self.p2[0] - other[0]) * (self.p3[1] - self.p2[1]) - (self.p3[0] - self.p2[0]) * (self.p2[1] - other[1]),
                     (self.p3[0] - other[0]) * (self.p1[1] - self.p3[1]) - (self.p1[0] - self.p3[0]) * (self.p3[1] - other[1])]
                return (a[0] > 0) == (a[1] > 0) == (a[2] > 0)
        else:
            return (other.p1 in self and other.p2 in self and other.p3 in self) or abs(other) == 0
    def __and__(self, other):
        if abs(self) == 0 or abs(other) == 0:
            return False
        cross_matr = [cross(*a, *b) for a in [(self.p1, self.p2), (self.p2, self.p3), (self.p3, self.p1)]
                      for b in [(other.p1, other.p2), (other.p2, other.p3), (other.p3, other.p1)]]
        return any(cross_matr) or (self in other) or (other in self)

import sys
exec(sys.stdin.read())
