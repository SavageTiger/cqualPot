from protocol import Packet
from protocol import Sqlite
from protocol import Util
import socket

class Commands:

    __database = None

    def __init__(self):
        self.__database = Sqlite.Sqlite()

    def handlePing(self, seqId: int, socket: socket.socket):
        response = Packet.Packet(seqId)
        response.createOkPacket(0)

        socket.send(response.getData())
        seqId += 1

        return seqId

    def handleQuery(self, seqId: int, packet: Packet.Packet, socket: socket.socket, client: dict):
        query = packet.getData(True)[1:]
        query = query.decode()

        result = self.__database.executeQuery(query)
        table  = self.__database.guessTable()

        # No results, return a OK package
        if (len(result) == 0):
            response = Packet.Packet(seqId)
            response.createOkPacket(0)

            socket.send(response.getData())

            seqId += 1

            return seqId

        # Stage 1: Send the column count package
        response = Packet.Packet(seqId)
        response.append(Util.Util.lenEnc(Util.Util.columnCount(result)))

        socket.send(response.getData())
        seqId += 1

        # Stage 2: Send the column definition packages
        definition = self.__database.getColumnDefinitions()

        for colDef in definition:
            response = Packet.Packet(seqId)
            response.createColumnPacket(
                client['database'], table, colDef['name'], colDef['length'], colDef['type']
            )

            socket.send(response.getData())
            seqId += 1

        # Stage 3: Column definition EOF packet
        response = Packet.Packet(seqId)
        response.createEOFPacket()

        socket.send(response.getData())
        seqId += 1

        # Stage 4: Send record rows
        for record in result:
            response = Packet.Packet(seqId)
            response.createResultPacket(record)

            socket.send(response.getData())
            seqId += 1

        # Stage 5: Rows EOF packet
        response = Packet.Packet(seqId)
        response.createEOFPacket()

        socket.send(response.getData())
        seqId += 1

        return seqId
