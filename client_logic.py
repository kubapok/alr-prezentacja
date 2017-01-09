
import socket
import sys
import pyaudio
import wave
import os
import datetime

PORT = 9995
CHUNK =  12000
AUDIOCHUNK = 3000

FORMAT = 8
CHANNELS = 2
RATE = 44100
OUTPUT = True

music_file  = "The Principle Of Moments.wav"

s_request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_request.connect(('localhost', PORT))

s_command = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_command.connect(('localhost', PORT))

s_broadcast = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_broadcast.connect(('localhost', PORT))

s_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_listen.connect(('localhost', PORT))


wf = wave.open(music_file, 'rb')
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=OUTPUT)


dir_list = os.listdir()
for i in range(1,20):
    if not str(i) in dir_list:
        log_file = open(str(i), 'w+')
        log_id = str(i)
        break


def action(request_state):
    s_request.sendall(bytes(request_state,'ascii'))
    command = str(s_command.recv(CHUNK),'ascii')
    print('command received: ', command)
    print('I have to', command)


    if command == "broadcast":
        log_file.write(str(datetime.datetime.now())[-15:]+'-'+log_id+ '-broadcasting\n')
        audio_data = wf.readframes(AUDIOCHUNK)
        s_broadcast.sendall(audio_data)
    elif command == "listen":
        log_file.write(str(datetime.datetime.now())[-15:]+'-'+log_id+ '-listening\n')
        audio_data = s_listen.recv(CHUNK)
        stream.write(audio_data)
    else:
        command = 'quit'
    return command
