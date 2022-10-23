from math import *
import re

str_counter = 0
functions = {}

def quit(s):
    s = args_resolver(s)
    return s.format(len(functions), str_counter)
functions["quit"] = quit

def args_resolver(x):
    if x.isdigit():
        return int(x)
    elif re.fullmatch("[+-]?([0-9]*[.])?[0-9]+", x):
        return float(x)
    else:
        return x[1:-1]

def create_func(args, func):
    def res(*num_arg):
        num_arg = [args_resolver(arg) for arg in num_arg]
        local_vars = {args[i] : num_arg[i] for i in range(len(args))}
        return eval(func, globals(), local_vars)
    return res

while True:
    s = input()
    if s == '':
        break
    str_counter += 1
    if s[0] == ':':
        s = s.split()
        func_name = s[0][1:]
        func = s[-1]
        arg_names = s[1:-1]
        functions[func_name] = create_func(arg_names, func)
    else:
        s = s.split()
        func_name = s[0]
        if func_name == "quit":
            args = [' '.join(s[1:])]
        else:
            args = s[1:]
        print(functions[func_name](*args))
        if func_name == "quit":
            break
    
    

