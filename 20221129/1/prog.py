class dump(type):
    def __new__(metacls, name, parents, ns, **kwds):
        methods = [name for name in ns if callable(ns[name])]
        for name in methods:
            def new_method(self, *args, super_fun=ns[name], func_name=name, **kwargs):
##                pr_args = [arg for arg in args if
##                           any(map(lambda x: isinstance(arg, x),
##                                   [str, bool, float, int]))]
                print(f'{func_name}: {args}, {kwargs}')
                return super_fun(self, *args, **kwargs)
            ns[name] = new_method
        return super().__new__(metacls, name, parents, ns)

##class C(metaclass=dump):
##    def __init__(self, val):
##        self.val = val
##
##    def add(self, other, another=None):
##        return self.val + other + (another or self.val)
##
##c = C(10)
##print(c.add(9))
##print(c.add(9,another=10))

import sys
exec(sys.stdin.read())
