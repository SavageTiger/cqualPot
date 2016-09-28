import struct
import socket
from hashlib import sha1

from protocol import Constants
from protocol import Packet

class Auth:

    __client = None

    def accept(self):
        print('accept')
        pass

    def deny(self):
        print('deny')
        pass

    def verify(self, username: str, password: str, salt: str):
        # Convert salt to bytes
        salt  = salt.encode()

        print(self.__client)

        passwordHashStage1 = sha1(password.encode()).digest()
        passwordHashStage2 = sha1(passwordHashStage1).digest()
        xorKey             = sha1(salt + passwordHashStage2).digest()

        expectedHash = bytearray()
        for i in range(0, len(xorKey)):
            expectedHash.append(xorKey[i] ^ passwordHashStage1[i])

        print(expectedHash)

        return \
            self.__client['username'].lower() == username.lower() and \
            self.__client['passwordHash'] == expectedHash

    def receiveCredentials(self, connection: socket.socket):

        packet = Packet.Packet()
        packet.fromSocket(connection)

        data = packet.getData(True)

        client                 = { 'username': '', 'passwordHash': b'', 'database': '', 'pluginName': '' }
        client['seqId']        = packet.getSeqId()
        client['capabilities'] = struct.unpack('i', data[0:4])[0]
        client['maxPacket']    = struct.unpack('i', data[4:8])[0]
        client['charSet']      = struct.unpack('b', data[8:9])[0]

        # Skip reserved
        data = data[9 + 23:]

        # Read username until terminator
        while data[0:1] != b'\x00':
            client['username'] = client['username'] + data[0:1].decode()
            data = data[1:]

        # Remove terminator
        data = data[1:]

        # Password is expected to be a 20 bytes SHA1 hash
        # The protocol checks anyway :) (Most likely to support other hash algorithms)

        hashLength = struct.unpack('b', data[0:1])[0]
        data = data[1:]
        client['passwordHash'] = data[0:hashLength]

        # Remove password
        data = data[hashLength:]

        # Read database name until terminator
        if client['capabilities'] & Constants.CLIENT_CONNECT_WITH_DB:
            while data[0:1] != b'\x00':
                client['database'] = client['database'] + data[0:1].decode()
                data = data[1:]

        # Remove terminator
        data = data[1:]

        # Read plugin name until terminator
        while data[0:1] != b'\x00':
            client['pluginName'] = client['pluginName'] + data[0:1].decode()
            data = data[1:]

        self.__client = client
