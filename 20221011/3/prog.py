start = False
width = 0
height = 0
gas = 0
water = 0

while True:
    inp = input().strip()
    if inp == '':
        continue
    if width == 0:
        width = len(inp) - 2
    if all([c == '#' for c in inp]):
        if not start:
            start = True
            continue
        else:
            break
    elif any([c == '.' for c in inp]):
        height += 1
        gas += width
    elif any([c == '~' for c in inp]):
        height += 1
        water += width

new_gas = gas
print('#' * (height + 2))
for i in range(gas // height):
    print('#' + ('.' * height) + '#')
for i in range(width - (gas // height)):
    print('#' + ('~' * height) + '#')
print('#' * (height + 2))

max_v = max([gas, water])
min_v = min([gas, water])
max_len = 20
min_len = round(max_len * min_v / max_v)
gas_len = max_len if gas > water else min_len
water_len = max_len if water > gas else min_len
max_num_len = max([len(str(gas)), len(str(water))])

print(f'{"."*gas_len:<20}', f'{gas:>{max_num_len}}/{width*height}')
print(f'{"~"*water_len:<20}', f'{water:>{max_num_len}}/{width*height}')
