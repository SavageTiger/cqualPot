
import struct

class Util:

    @staticmethod
    def columnCount(hashMap):
        if len(hashMap) == 0:
            return 0

        return len(hashMap[0])


    @staticmethod
    def lenEnc(input: int):
        if input < 251:
            return bytes(struct.pack('<B', input))
        elif input <= 65535:
            return b'\xfc' + bytes(struct.pack('<H', input))
        elif input <= 16777215:
            return b'\xfd' + bytes(struct.pack('<I', input)[0:3])
        else:
            return b'\xfe' + bytes(struct.pack('<Q', input))
