import struct

class Packet:

    __data  = bytearray()
    __seqId = 0

    def __init__(self, seqId: int):
        self.__seqId = seqId

    def append(self, data: bytes):
        for dataByte in data:
            self.__data.append(dataByte)

    def getData(self):
        packet = bytearray()
        packet = packet.fromhex(
            struct.pack('i', len(self.__data)).hex() +
            struct.pack('b', self.__seqId).hex()
        )

        for dataByte in self.__data:
            packet.append(dataByte)

        return packet