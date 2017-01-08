
import socket
import sys
import pyaudio
import wave


PORT = int(sys.argv[1])
CHUNK =  12000
AUDIOCHUNK = 3000

FORMAT = 8
CHANNELS = 2
RATE = 44100
OUTPUT = True

music_file  = "The Principle Of Moments.wav"

is_broadcasting = None

s_request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_request.connect(('localhost', PORT))

s_command = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_command.connect(('localhost', PORT))

s_broadcast = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_broadcast.connect(('localhost', PORT))

s_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_listen.connect(('localhost', PORT))

# import fcntl, os
# fcntl.fcntl(s_request, fcntl.F_SETFL, os.O_NONBLOCK)
# fcntl.fcntl(s_command, fcntl.F_SETFL, os.O_NONBLOCK)
# fcntl.fcntl(s_broadcast, fcntl.F_SETFL, os.O_NONBLOCK)
# fcntl.fcntl(s_listen, fcntl.F_SETFL, os.O_NONBLOCK)

if sys.argv[2] == 'broadcast':
    wf = wave.open(music_file, 'rb')
    print('broadcast')
else:
    print('listen')
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=OUTPUT)


while True:
    s_request.sendall(bytes('listen','ascii'))
    command = s_command.recv(CHUNK)
    #print(str(command,'ascii'))

    if str(command,'ascii') == "broadcast":
        audio_data = wf.readframes(AUDIOCHUNK)
        s_broadcast.sendall(audio_data)
        print(audio_data[0:10])
        print(len(audio_data))
    elif str(command,'ascii') == "listen":
        audio_data = s_listen.recv(CHUNK)
        print(audio_data[0:10])
        print(len(audio_data))
        stream.write(audio_data)
    else:
        print('sth unexpected happend')
