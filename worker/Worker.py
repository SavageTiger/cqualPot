
from protocol import Handshake
from protocol import Auth

class Worker:

    __salt         = ''
    __connectionId = 1
    __connection   = None

    def __init__(self, connection, connectionId):
        print ('Init' + str(connectionId))

        self.__connectionId = connectionId
        self.__connection   = connection

        self.handShake()
        self.authenticate()

    def authenticate(self):
        auth = Auth.Auth()
        auth.receiveCredentials(self.__connection, self.__salt)


    def handShake(self):
        handshake   = Handshake.Handshake()
        self.__salt = handshake.send(self.__connection, self.__connectionId)
