import inspect
import typing

class check(type):
    def __init__(cls, name, parents, ns, **kwds):
        def new_fun(self):
            ann = inspect.get_annotations(self.__class__)
            for name in ann:
                try:
                    attr = getattr(self, name)
                except AttributeError:
                    #print("no value", name)
                    return False
                attr_type = (ann[name]
                             if typing.get_origin(ann[name]) == None
                             else typing.get_origin(ann[name]))
                if not isinstance(attr, attr_type):
                    #print("types differ", name, type(attr), attr_type)
                    return False
            return True
        setattr(cls, 'check_annotations', new_fun)
        return super().__init__(name, parents, ns)

import sys
exec(sys.stdin.read())
