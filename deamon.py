
import socket
from worker import Worker
from _thread import *

host = '0.0.0.0'
port = 3309
connectionId = 1

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serverSocket.bind((host, port))
except socket.error as e:
    print ('Unable to create listening socket (' + (str(e)) + ')')
    quit()
    
    
serverSocket.listen(5)

while True:
    connection = serverSocket.accept()

    connectionId += 1

    start_new_thread(Worker.Worker, (connection[0], connectionId,))