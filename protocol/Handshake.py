import struct
import socket
import uuid
from . import utils


class Handshake:
    
    def send(self, connection: socket.socket, connectionId: int):

        salt   = str(uuid.uuid4())[0: 8]
        compat = 0x00000008 | 0x00000001 | 0x00000200 | 0x00080000

        connection.send(struct.pack('b', 100))   # Payload Length
        connection.send(struct.pack('b', 0))   # Filler
        connection.send(struct.pack('b', 0))   # Filler
        connection.send(struct.pack('b', 0))   # Sec ID
        connection.send(struct.pack('b', 10))  # Protocol version
        connection.send('5.6.28-0ubuntu0.15.04.1'.encode()) # MySQL version
        connection.send(struct.pack('b', 0))  # Version terminator
        connection.send(struct.pack('i', connectionId))  # Connection id
        connection.send(salt.encode())  # Auth salt
        connection.send(struct.pack('b', 0))  # Filter 1
        connection.send(compat.to_bytes(4, 'big') >> 16)  # Filter 1
