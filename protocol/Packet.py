import socket
import struct

from protocol import Util

class Packet:

    __data  = None
    __seqId = 0

    def __init__(self, seqId: int = 0):
        self.__data = bytearray()
        self.__seqId = seqId

    def append(self, data: bytes):
        for dataByte in data:
            self.__data.append(dataByte)

    def fromSocket(self, connection: socket.socket):
        bufferSize = connection.recv(3) + b'\x00'
        bufferSize = struct.unpack('i', bufferSize)
        bufferSize = bufferSize[0] + 1

        data = bytes()

        while len(data) < bufferSize:
            buffer = connection.recv(bufferSize)

            data = data.fromhex(data.hex() + buffer.hex())

        self.__seqId = struct.unpack('b', data[0:1])[0]
        self.__data  = data[1:]

    def createColumnPacket(self, database: str, table: str, column: str):
        self.append(Util.Util.lenEncodedString("def"))    # catalog (always "def")
        self.append(Util.Util.lenEncodedString(database)) # db (schema?)
        self.append(Util.Util.lenEncodedString(table))    # table
        self.append(Util.Util.lenEncodedString(table))    # org_table (same as table)
        self.append(Util.Util.lenEncodedString(column))   # name
        self.append(Util.Util.lenEncodedString(column))   # org_name (same as name)

    def createOkPacket(self, header: int, affectedRows: int = 0, lastInsertId: int = 0, status: int = 0, warnings: int = 0, transFlags: int = 0, errorMsg: str = ''):
        self.append(bytes(header))
        self.append(Util.Util.lenEnc(affectedRows))
        self.append(Util.Util.lenEnc(lastInsertId))
        self.append(struct.pack('i', status))
        self.append(struct.pack('i', warnings))
        self.append(struct.pack('i', transFlags))
        self.append(errorMsg.encode()) # (type = ROP)

    def getSeqId(self):
        return self.__seqId

    def getData(self, headerLess = False):
        if headerLess:
            return self.__data

        packet = bytearray()
        packet = packet.fromhex(
            struct.pack('i', len(self.__data)).hex()[0:6] + # Packet length (3 byte integer)
            struct.pack('b', self.__seqId).hex() +
            self.__data.hex()
        )

        return packet