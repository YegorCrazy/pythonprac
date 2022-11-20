class Alpha:
    __slots__ = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    
    def __init__(self, **kwargs):
        for var_name in kwargs.keys():
            setattr(self, var_name, kwargs[var_name])

    def __str__(self):
        attrs = []
        for var_name in self.__slots__:
            if hasattr(self, var_name):
                attrs += [var_name]
        return ', '.join('{}: {}'.format(name, getattr(self, name))
                         for name in attrs)

class AlphaQ:
    allowed = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    
    def __init__(self, **kwargs):
        self._int_dict = {}
        for var_name in kwargs.keys():
            if var_name in self.allowed:
                self._int_dict[var_name] = kwargs[var_name]
            else:
                raise AttributeError

    def __setattr__(self, var, val):
        if var == '_int_dict':
            return super().__setattr__(var, val)
        if var in self.allowed:
            self._int_dict[var] = val
        else:
            raise AttributeError

    def __getattr__(self, var):
        if var in self._int_dict.keys():
            return self._int_dict[var]
        else:
            raise AttributeError

    def __str__(self):
        return ', '.join('{}: {}'.format(var, self._int_dict[var])
                         for var in sorted(self._int_dict.keys()))

import sys
exec(sys.stdin.read())
        
