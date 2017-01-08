
import socket
import sys
import time

HOST = ''
PORT = int(sys.argv[1])
CHUNK =  50000
CLIENTQUANTITY = 2



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

s.listen(10)
print('Socket now listening')

class Client():
    all = list()
    def __init__(self,):
        self.c_request, self.addr_request = s.accept()
        self.c_command, self.addr_command = s.accept()
        self.c_broadcast, self.addr_broadcast = s.accept()
        self.c_listen, self.addr_listen = s.accept()

        self.isAlive = True

        self.request = None
        self.command = None

    def connectClients():
        for i in range(CLIENTQUANTITY):
            client = Client()
            Client.all.append(client)

    def receiveRequests():
        for client in Client.all:
            if client.isAlive:
                client.request = str(client.c_request.recv(CHUNK),'ascii')

    def setCommands():
        Client.all[0].command = 'broadcast'
        Client.all[1].command = 'listen'

    def sendCommands():
        for client in Client.all:
            if client.isAlive:
                client.c_command.sendall(bytes(client.command, 'ascii'))


    def recvAudio():
        for client in Client.all:
            if client.isAlive and client.command == 'broadcast':
                Client.audio_data = client.c_broadcast.recv(CHUNK)
                break

    def sendAudio():
        for client in Client.all:
            if client.isAlive and client.command == 'listen':
                client.c_listen.sendall(Client.audio_data)


Client.connectClients()
while True:
    Client.receiveRequests()
    Client.setCommands()
    Client.sendCommands()
    Client.recvAudio()
    Client.sendAudio()

s.close()
