from protocol import Packet
from protocol import Sqlite
from protocol import Util
from protocol import SeqId
import socket

class Commands:

    __database = None
    __client   = None

    def __init__(self, client: dict):
        self.__database = Sqlite.Sqlite(client['database'])
        self.__client   = client

    def handlePing(self, seqId: SeqId.SeqId, socket: socket.socket):
        response = Packet.Packet(seqId.getId())
        response.createOkPacket(0)

        socket.send(response.getData())

    def handleQuery(self, seqId: SeqId.SeqId, packet: Packet.Packet, socket: socket.socket):
        query = packet.getData(True)[1:]
        query = query.decode()

        result = self.__database.executeQuery(query)
        table = self.__database.guessTable()

        print('Q:' + query)
        print('T:' + table)

        # No results, return a OK package
        if (len(result) == 0):
            response = Packet.Packet(seqId.getId())
            response.createOkPacket(0)

            socket.send(response.getData())

            return None

        # Stage 1: Send the column count package
        response = Packet.Packet(seqId.getId())
        response.append(Util.Util.lenEnc(Util.Util.columnCount(result)))

        socket.send(response.getData())

        # Stage 2: Send the column definition packages
        definition = self.__database.getColumnDefinitions()

        for colDef in definition:
            response = Packet.Packet(seqId.getId())
            response.createColumnPacket(
                self.__client['database'], table, colDef['name'], colDef['length'], colDef['type']
            )

            socket.send(response.getData())

        # Stage 3: Column definition EOF packet
        response = Packet.Packet(seqId.getId())
        response.createEOFPacket()

        socket.send(response.getData())

        # Stage 4: Send record rows
        for record in result:
            response = Packet.Packet(seqId.getId())
            response.createResultPacket(record)

            socket.send(response.getData())

        # Stage 5: Rows EOF packet
        response = Packet.Packet(seqId.getId())
        response.createEOFPacket()

        socket.send(response.getData())
