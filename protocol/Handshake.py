import struct
import socket
import uuid

from protocol import Packet

CLIENT_LONG_PASSWORD		= 0x00001	# new more secure passwords
CLIENT_FOUND_ROWS			= 0x00002	# Found instead of affected rows
CLIENT_LONG_FLAG			= 0x00004	# Get all column flags
CLIENT_CONNECT_WITH_DB		= 0x00008	# One can specify db on connect
CLIENT_NO_SCHEMA			= 0x00010	# Don't allow database.table.column
CLIENT_COMPRESS				= 0x00020	# Can use compression protocol
CLIENT_ODBC					= 0x00040	# Odbc client
CLIENT_LOCAL_FILES			= 0x00080	# Can use LOAD DATA LOCAL
CLIENT_IGNORE_SPACE			= 0x00100	# Ignore spaces before '('
CLIENT_PROTOCOL_41			= 0x00200	# New 4.1 protocol
CLIENT_INTERACTIVE			= 0x00400	# This is an interactive client
CLIENT_SSL					= 0x00800	# Switch to SSL after handshake
CLIENT_IGNORE_SIGPIPE		= 0x01000	# IGNORE sigpipes
CLIENT_TRANSACTIONS			= 0x02000	# Client knows about transactions
CLIENT_RESERVED				= 0x04000	# Old flag for 4.1 protocol
CLIENT_SECURE_CONNECTION	= 0x08000	# New 4.1 authentication


class Handshake:

    def send(self, connection: socket.socket, connectionId: int):

        auth   = ''
        salt   = str(uuid.uuid4())[0: 8]
        compat = struct.pack('I', CLIENT_LONG_FLAG|CLIENT_CONNECT_WITH_DB|CLIENT_PROTOCOL_41|CLIENT_TRANSACTIONS|CLIENT_SECURE_CONNECTION|CLIENT_LONG_PASSWORD)

        packet = Packet.Packet(0)
        packet.append(struct.pack('b', 10))  # Protocol version
        packet.append('5.6.28-0ubuntu0.15.04.1'.encode()) # MySQL version
        packet.append(struct.pack('b', 0))  # Version terminator
        packet.append(struct.pack('<I', connectionId))  # Connection id
        packet.append(salt.encode())  # Auth salt
        packet.append(struct.pack('b', 0))  # Salt Terminator
        packet.append(bytes([compat[0], compat[1]])) # Compat
        packet.append(struct.pack('b', 8)) # ID 8 = latin1_swedish_ci (usually)
        packet.append(struct.pack('b', 2))  # Status flag (autocommit is enabled)
        packet.append(bytes([compat[2], compat[3]]))  # Compat
        packet.append(struct.pack('b', len(salt))) # Auth data len
        packet.append('mysql_native_password'.encode())  # Auth plugin
        packet.append(struct.pack('b', 0))  # Terminator

        connection.send(packet.getData())
