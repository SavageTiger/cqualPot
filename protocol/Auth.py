import struct
import socket

from protocol import Constants
from protocol import Packet

class Auth:

    def receiveCredentials(self, connection: socket.socket, salt: str):

        packet = Packet.Packet()
        packet.fromSocket(connection)

        data = packet.getData(True)

        print (data)

        client                 = {}
        client['seqId']        = packet.getSeqId()
        client['capabilities'] = struct.unpack('i', data[0:4])[0]
        client['maxPacket']    = struct.unpack('i', data[4:8])[0]
        client['charSet']      = struct.unpack('b', data[8:9])[0]

        # Skip reserved
        data = data[16:]

        return client