from math import *

def Calc (s, t, u):
    def res_fun (x):
        x_1 = eval(s)
        y = eval(t)
        x = x_1
        return eval(u)
    return res_fun

fun = Calc(*eval(input()))
print(fun(eval(input())))
