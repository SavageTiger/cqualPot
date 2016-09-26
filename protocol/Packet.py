import struct

class Packet:

    __data  = None
    __seqId = 0

    def __init__(self, seqId: int):
        print (self.__seqId)
        self.__data = bytearray()
        self.__seqId = seqId

    def append(self, data: bytes):
        for dataByte in data:
            self.__data.append(dataByte)

    def getData(self):
        packet = bytearray()
        packet = packet.fromhex(
            struct.pack('i', len(self.__data)).hex()[0:6] + # Packet length (3 byte integer)
            struct.pack('b', self.__seqId).hex() +
            self.__data.hex()
        )

        return packet