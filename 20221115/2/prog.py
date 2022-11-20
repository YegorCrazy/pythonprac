class Num:

    def __get__(self, obj, cls):
        if hasattr(obj, '_value'):
            return obj._value
        return 0

    def __set__(self, obj, val):
        if hasattr(val, 'real'):
            obj._value = val.real
        elif hasattr(val, '__len__'):
            obj._value = len(val)
        else:
            raise ValueError('value in neither number nor iterable')

    def __delete__(self, obj):
        del obj._value

import sys
exec(sys.stdin.read())
