import struct
import socket
import uuid

from protocol import Packet
from protocol import Constants

class Handshake:

    def send(self, connection: socket.socket, connectionId: int):

        salt         = str(uuid.uuid4())[0: 8]
        salt2        = str(uuid.uuid4())[0: 13]
        capabilities = struct.pack(
            'I', Constants.CLIENT_PROTOCOL_41 +
                 Constants.CLIENT_SECURE_CONNECTION +
                 Constants.CLIENT_NO_SCHEMA +
                 Constants.CLIENT_IGNORE_SPACE +
                 Constants.CLIENT_LONG_PASSWORD +
                 Constants.CLIENT_INTERACTIVE +
                 Constants.CLIENT_TRANSACTIONS +
                 Constants.CLIENT_PLUGIN_AUTH +
                 Constants.CLIENT_CONNECT_WITH_DB
        )

        packet = Packet.Packet(0)
        packet.append(struct.pack('b', 10))                      # Protocol version
        packet.append('5.6.28-0ubuntu0.15.04.1'.encode())        # MySQL version
        packet.append(struct.pack('b', 0))                       # Version terminator
        packet.append(struct.pack('<I', connectionId))           # Connection id
        packet.append(salt.encode())                             # Auth salt
        packet.append(struct.pack('b', 0))                       # Salt Terminator
        packet.append(bytes([capabilities[0], capabilities[1]])) # Capabilities (lower bytes)
        packet.append(struct.pack('b', 8))                       # ID 8 = latin1_swedish_ci (usually)
        packet.append(struct.pack('b', 2))                       # Status flag (2 = autocommit is enabled)
        packet.append(struct.pack('b', 0))                       # Status terminator
        packet.append(bytes([capabilities[2], capabilities[3]])) # Capabilities (upper bytes)
        packet.append(struct.pack('b', len(salt2) + len(salt)))  # Auth data (part 2) len
        packet.append(bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))     # 10 bytes of Filler
        packet.append(salt2.encode())                            # Auth data 2
        packet.append('mysql_native_password'.encode())          # Auth plugin
        packet.append(struct.pack('b', 0))                       # Handshake terminator

        connection.send(packet.getData())

        return salt + salt2

