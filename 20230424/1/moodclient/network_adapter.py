"""Module with NetworkInterface class."""

import socket
import readline


class NetworkAdapter:
    """Class with a socket interface."""

    def __init__(self, server_host, server_port=1337):
        self.server_host = server_host
        self.server_port = server_port

    def OpenSocket(self):
        """Open socket."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))

    def SendInfoToServer(self, msg):
        """Send a request to server and get response."""
        self.socket.sendall((msg + '\n').encode())
        response = self.socket.recv(1024).decode()
        return response

    def SendInfoToServerWithoutResponse(self, msg):
        """Send a request to server without waiting for response."""
        self.socket.sendall((msg + '\n').encode())

    def GetInfoFromServer(self):
        """Get response from server."""
        return self.socket.recv(1024).decode()

    def CloseSocket(self):
        """Close socket."""
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


def PrintMessageFromNetworkAdapterToCmd(network_adapter, cmd):
    """A function for asyncronous getting responses from server."""
    while (network_adapter.socket.fileno() == -1 or
           (message := network_adapter.GetInfoFromServer())):
        print(f"\n{message}{cmd.prompt}{readline.get_line_buffer()}",
              end="", flush=True)
