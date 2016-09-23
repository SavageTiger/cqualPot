
import socket

class Handshake:
    
    def send(self, connection: socket.socket):
        print (connection)
        connection.send('Test'.encode())
