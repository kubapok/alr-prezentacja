
import socket
import sys
import time

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = int(sys.argv[1]) # Arbitrary non-privileged port
CHUNK =  50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

#Bind socket to local host and port
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
        Client.all.append(self)



client1 = Client()
client2 = Client()
client3 = Client()
client4 = Client()


while True:

    request1 = client1.c_request.recv(CHUNK)
    request2 = client2.c_request.recv(CHUNK)
    request3 = client3.c_request.recv(CHUNK)
    request4 = client4.c_request.recv(CHUNK)
    print(str(request1,'ascii'))
    print(str(request2,'ascii'))
    print(str(request3,'ascii'))
    print(str(request4,'ascii'))

    client1.c_command.sendall(bytes('broadcast', 'ascii'))
    client2.c_command.sendall(bytes('listen', 'ascii'))
    client3.c_command.sendall(bytes('listen', 'ascii'))
    client4.c_command.sendall(bytes('listen', 'ascii'))

    audio_data = client1.c_broadcast.recv(CHUNK)
    client2.c_listen.sendall(audio_data)
    client3.c_listen.sendall(audio_data)
    client4.c_listen.sendall(audio_data)


s.close()
