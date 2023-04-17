import sys
import socket

def sqrootnet(coeffs, s):
    s.sendall((coeffs + '\n').encode())
    return s.recv(1024).decode().strip()


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1337))
        while coeffs := input():
            print(sqrootnet(coeffs, s))
