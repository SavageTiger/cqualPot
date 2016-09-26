import struct
import socket

from protocol import Packet

class Auth:

    def receiveCredentials(self, connection: socket.socket, salt: str):

        bufferSize = connection.recv(3) + b'\x00'
        bufferSize = struct.unpack('i', bufferSize)
        bufferSize = bufferSize[0]

        data = connection.recv(bufferSize)

        print(salt)
        print(data)
