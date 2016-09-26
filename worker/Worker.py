
from protocol import Handshake

class Worker:

    __connectionId = 1
    __connection   = None

    def __init__(self, connection, connectionId):
        print ('Init' + str(connectionId))

        self.__connectionId = connectionId
        self.__connection   = connection

        self.handShake()

    def handShake(self):
        handshake = Handshake.Handshake()
        handshake.send(self.__connection, self.__connectionId)
