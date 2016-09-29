from protocol import Packet
from protocol import Sqlite
import socket

class Commands:

    __database = None

    def __init__(self):
        self.__database = Sqlite.Sqlite()

    def handleQuery(self, seqId: int, packet: Packet.Packet, socket: socket.socket):
        response = Packet.Packet(seqId)

        query = packet.getData(True)[1:]
        query = query.decode()

        result = self.__database.executeQuery(query)

        print('Query: "' + query + '"')
        print('Result: ' + str(result))

        response.createOkPacket(0, len(result))

        socket.send(response.getData())