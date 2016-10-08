
from protocol import Handshake
from protocol import Auth
from protocol import Packet
from protocol import Constants
from protocol import Commands
from protocol import SeqId

class Worker:

    __salt         = ''
    __connectionId = 1
    __connection   = None
    __seqId        = None
    __client       = None

    def __init__(self, connection, connectionId):
        self.__seqId        = SeqId.SeqId()
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
        command = Commands.Commands(self.__client)

        while True:
            packet      = Packet.Packet()
            clientSeqId = packet.fromSocket(self.__connection)

            self.__seqId.set(clientSeqId)

            if Constants.SERVER_CMD_QUERY == packet.getData(True)[0]:
                command.handleQuery(self.__seqId, packet, self.__connection)
            elif Constants.SERVER_CMD_PING == packet.getData(True)[0]:
                command.handlePing(self.__seqId, self.__connection)
            else:
                print('Unknown packet (' + str(packet.getData(True)[0]) + ')')
