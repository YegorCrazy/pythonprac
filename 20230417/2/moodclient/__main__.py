"""Module with main client commands."""

import sys
import threading
from .network_adapter import NetworkAdapter
from .network_adapter import PrintMessageFromNetworkAdapterToCmd
from .mudshell import MUDShell


if __name__ == '__main__':
    # аргументы: имя хост [порт]
    if len(sys.argv) < 2:
        print('username not specified')
        exit()
    name = sys.argv[1]
    if len(sys.argv) < 3:
        print('server host not specified')
        exit()
    host = sys.argv[2]
    if len(sys.argv) > 3:
        port = int(sys.argv[3])
        network_adapter = NetworkAdapter(host, port)
    else:
        network_adapter = NetworkAdapter(host)
    shell = MUDShell()
    shell.SetNetworkAdapter(network_adapter)
    try:
        shell.ActivateNetworkAdapter()
    except Exception:
        print("Can't access the server.")
    else:
        resp = shell.network_adapter.SendInfoToServer("login " + name)
        if resp == 'no':
            print(f'name {name} is occupied, try another one')
            exit()
        elif resp == 'ok':
            print(f'logined as {name}')
            server_messages_getter = threading.Thread(
                target=PrintMessageFromNetworkAdapterToCmd,
                args=(shell.network_adapter, shell))
            server_messages_getter.start()
            print('<<< Welcome to Python-MUD 0.1 >>>')
            shell.cmdloop()
