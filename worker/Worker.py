
from protocol import Handshake
from protocol import Auth
from protocol import Packet
from protocol import Constants
from protocol import Commands

class Worker:

    __salt         = ''
    __connectionId = 1
    __connection   = None
    __seqId        = 2
    __client       = None

    def __init__(self, connection, connectionId):
        self.__connectionId = connectionId
        self.__connection   = connection

        self.handShake()
        self.authenticate()

    def authenticate(self):
        auth = Auth.Auth()
        auth.receiveCredentials(self.__connection)

        if auth.verify('Sven', 'test', self.__salt):
            self.__client = auth.accept(self.__connection, self.__salt)

            self.commandLoop()
        else:
            auth.deny()

    def handShake(self):
        handshake   = Handshake.Handshake()
        self.__salt = handshake.send(self.__connection, self.__connectionId)

    def commandLoop(self):
        command = Commands.Commands()

        while True:
            packet = Packet.Packet()
            packet.fromSocket(self.__connection)

            if Constants.SERVER_CMD_QUERY == packet.getData(True)[0]:
                self.__seqId += 1

                command.handleQuery(self.__seqId, packet, self.__connection, self.__client)
            else:
                print('Unknown packet')
