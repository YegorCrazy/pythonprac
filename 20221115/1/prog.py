def objcount(cls):
    cls.counter = 0
    def new_init(self, *args, **kwargs):
        self.__class__.counter += 1
        return self.__init(*args, **kwargs)
    cls.__init = cls.__init__
    cls.__init__ = new_init
    def new_del(self, *args, **kwargs):
        self.__class__.counter -= 1
        return self.__del(*args, **kwargs)
    def new_old_del(self):
        pass
    cls.__del = cls.__del__ if '__del__' in dir(cls) else new_old_del
    cls.__del__ = new_del
    return cls

import sys
exec(sys.stdin.read())
