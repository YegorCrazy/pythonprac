sum = 0

while new := input():
    new = int(new)
    if new > 0:
        sum += new
        if sum > 21:
            print(sum)
            break
    else:
        print(new)
        break
