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

##class C(metaclass=check):
##    A: list[int]
##    B: str = "QQ"
##
##c = C()
##print(c.check_annotations())
##c.A = "ZZ"
##print(c.check_annotations())
##c.A = [100500, 42, 0]
##print(c.check_annotations())
##c.B = type("Boo",(str,),{})(42)
##print(c.check_annotations())
##c.A = ["FALSE"]
##print(c.check_annotations())

import sys
exec(sys.stdin.read())
