
import socket
import sys
import time

HOST = ''
PORT = int(sys.argv[1])
CHUNK =  50000
CLIENTQUANTITY = 2



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')


# import fcntl, os
# fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

s.listen(20)
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
        #for i in range(3):
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
            if client.isAlive:
                client.c_listen.sendall(Client.audio_data)


Client.connectClients()

# import time
# t_start = time.time()
# notification = True
# sw = False

while True:
    # if notification and 5 > time.time() - t_start > 4:
    #     notification = False
    #     print('GOWWWWNO\n' * 60 )
    #     sw = True
    #
    # if  time.time() - t_start > 8:
    #     print('SEEER\n' * 60 )
    #
    #     sw = False


    Client.receiveRequests()
    Client.setCommands()
    Client.sendCommands()
    print('command sent')
    Client.recvAudio()
    print('audio receinved')
    print(Client.audio_data[0:10])
    print(len(Client.audio_data))
    Client.sendAudio()
    print('audio sent')


    # if not sw:
    #     client1.c_command.sendall(bytes('broadcast', 'ascii'))
    #     client2.c_command.sendall(bytes('listen', 'ascii'))
    #     client3.c_command.sendall(bytes('listen', 'ascii'))
    #     client4.c_command.sendall(bytes('listen', 'ascii'))
    #
    #
    #     audio_data = client1.c_broadcast.recv(CHUNK)
    #     client2.c_listen.sendall(audio_data)
    #     client3.c_listen.sendall(audio_data)
    #     client4.c_listen.sendall(audio_data)
    # else:
    #     client1.c_command.sendall(bytes('listen', 'ascii'))
    #     client2.c_command.sendall(bytes('broadcast', 'ascii'))
    #     client3.c_command.sendall(bytes('listen', 'ascii'))
    #     client4.c_command.sendall(bytes('listen', 'ascii'))
    #
    #
    #     audio_data = client2.c_broadcast.recv(CHUNK)
    #     client1.c_listen.sendall(audio_data)
    #     client3.c_listen.sendall(audio_data)
    #     client4.c_listen.sendall(audio_data)

s.close()
