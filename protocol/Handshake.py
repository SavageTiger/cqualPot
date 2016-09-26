import struct
import socket
import uuid

from protocol import Packet

class Handshake:
    
    def send(self, connection: socket.socket, connectionId: int):

        salt   = str(uuid.uuid4())[0: 8]
        compat = 0x00000008 | 0x00000001 | 0x00000200 | 0x00080000

        packet = Packet.Packet(0)
        packet.append(struct.pack('b', 10))  # Protocol version
        packet.append('5.6.28-0ubuntu0.15.04.1'.encode()) # MySQL version
        packet.append(struct.pack('b', 0))  # Version terminator
        packet.append(struct.pack('i', connectionId))  # Connection id
        packet.append(salt.encode())  # Auth salt
        packet.append(struct.pack('b', 0))  # Filter 1

        connection.send(packet.getData())
