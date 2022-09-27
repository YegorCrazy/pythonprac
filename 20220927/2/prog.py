def key (x):
    return (x * x) % 100

l = list(eval(input()))

flag = True
while flag:
    flag = True
    for i in range(len(l) - 1):
        if key(l[i]) > key(l[i + 1]):
            l[i], l[i + 1] = l[i + 1], l[i]
            flag = False
    if flag:
        break
print(l)
