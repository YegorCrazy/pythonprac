import sys
import struct

def join_bytes(inp):
    return ''.join(ch.decode() for ch in inp)

file = sys.stdin.buffer.read()
try:
    res = struct.unpack('cccciccccccccihhiihhcccci', file[:44])
except Exception as ex:
    print('NO')
else:
    if (join_bytes(res[:4]) == 'RIFF'
        and join_bytes(res[5:9]) == 'WAVE'
        and join_bytes(res[9:13]) == 'fmt' + chr(32)
        and join_bytes(res[20:24]) == 'data'):
        print(f'Size={res[4]}, Type={res[14]}, Channels={res[15]}, Rate={res[16]}, Bits={res[19]}, Data size={res[-1]}')
    else:
        print('NO')
