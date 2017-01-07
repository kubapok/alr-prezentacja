
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



cli1 = list()
for i in range(4):
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    cli1.append(conn)


cli2 = list()
for i in range(4):
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    cli2.append(conn)



while True:
    request1 = cli1[0].recv(CHUNK)
    request2 = cli2[0].recv(CHUNK)
    print(str(request1,'ascii'))
    print(str(request2,'ascii'))

    cli1[1].sendall(bytes('broadcast', 'ascii'))
    cli2[1].sendall(bytes('listen', 'ascii'))

    audio_data = cli1[2].recv(CHUNK)
    cli2[3].send(audio_data)





s.close()
