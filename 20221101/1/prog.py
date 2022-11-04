class Omnibus:
    attr_dict = {}
    def __setattr__(self, attr, val):
        if attr in self.__dict__:
            return
        else:
            type(self).attr_dict[attr] = type(self).attr_dict.get(attr, 0) + 1
            self.__dict__[attr] = 1
    def __getattribute__(self, attr):
        if attr[0] == '_':
            return super().__getattribute__(attr)
        return type(self).attr_dict.get(attr, 0)
    def __delattr__(self, attr):
        if attr not in self.__dict__:
            return
        else:
            del self.__dict__[attr]
            type(self).attr_dict[attr] -= 1

import sys
exec(sys.stdin.read())
