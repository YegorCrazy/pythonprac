import sys
inp = sys.stdin.read()
parts_num = ord(inp[0])
sys.stdout.write(inp[0])
inp = inp[1:]
parts = [inp[i*len(inp)//parts_num:(i+1)*len(inp)//parts_num] for i in range(parts_num)]
for part in sorted(parts):
    sys.stdout.write(part)
