
from protocol import Handshake

class Worker:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection
        self.handShake()

    def handShake(self):
        handshake = Handshake.Handshake()
        handshake.send(self.__connection)
