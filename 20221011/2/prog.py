from math import *

def func_cr(fun_str):
    def fun(x):
        return eval(fun_str)
    return fun
    

args = input().split()
W, H, A, B, *fun = args
W = int(W)
H = int(H)
A = float(A)
B = float(B)
fun = func_cr(''.join(fun))

res = [[' ' for i in range(W)] for j in range(H)]

fun_max = fun(A)
fun_min = fun(A)

for i in range(W):
    cur_x = (i / (W - 1)) * (B - A) + A
    cur_y = fun(cur_x)
    if cur_y < fun_min:
        fun_min = cur_y
    if cur_y > fun_max:
        fun_max = cur_y

prev_y = -1
for i in range(W):
    cur_x = (i / (W - 1)) * (B - A) + A
    y_ind = round(((fun(cur_x) - fun_min) / (fun_max - fun_min)) * (H - 1))
    res[y_ind][i] = '*'
    if prev_y != -1:
        if abs(prev_y - y_ind) > 1:
            step = 1 if y_ind > prev_y else -1
            for med in range(prev_y, (prev_y + y_ind) // 2, step):
                res[med][i - 1] = '*'
            for med in range((prev_y + y_ind) // 2, y_ind, step):
                res[med][i] = '*'
    prev_y = y_ind

res.reverse()
for str in res:
    print(''.join(str))
