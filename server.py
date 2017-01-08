
import socket
import sys
import time

HOST = ''
PORT = int(sys.argv[1])
CHUNK =  50000
CLIENTQUANTITY = 4



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
    __next_id = 0

    def __init__(self,):
        self.c_request, self.addr_request = s.accept()
        self.c_command, self.addr_command = s.accept()
        self.c_broadcast, self.addr_broadcast = s.accept()
        self.c_listen, self.addr_listen = s.accept()
        self.id = Client.__next_id
        Client.__next_id +=1


        if len(Client.all) == 0:
            self.command = 'broadcast'
        else:
            self.command = 'listen'

        print('setting to', self.command)
        self.isAlive = True


    def connectClients():
        for i in range(CLIENTQUANTITY):
            client = Client()
            Client.all.append(client)


    def receiveRequests():
        for client in Client.all:
            if client.isAlive:
                client.request = str(client.c_request.recv(CHUNK),'ascii')

    def setEveryClientToListen():
        for client in Client.all:
            client.command = 'listen'
            #print('setting every client to liste triggered, setting to :', client.command)


    def SetFirstAliveWithOtherIdToBroadcast(id):
        for client in Client.all:
            if client.isAlive and client.id != id:
                client.command = 'broadcast'
                return
        print('no alive other users to broadcast')
        assert False

    def setCommands():
        # pass
        #Client.all[0].command = 'broadcast'
        #Client.all[1].command = 'listen'
        for client in Client.all:
            if client.isAlive:
                if client.command == 'listen' and client.request == 'broadcast':
                    Client.setEveryClientToListen()
                    client.command = 'broadcast'
                    return
                if client.command == 'broadcast' and client.request == 'listen':
                    Client.setEveryClientToListen()
                    Client.SetFirstAliveWithOtherIdToBroadcast(client.id)
                    return

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
    for c in Client.all:
        print(c.command)
    Client.sendCommands()
    Client.recvAudio()
    Client.sendAudio()

s.close()
