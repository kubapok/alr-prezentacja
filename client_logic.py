
import socket
import sys
import pyaudio
import wave
import os
import datetime
from config import HOST, PORT, PLAY_AUDIO

CHUNK =  12000
AUDIOCHUNK = 3000

FORMAT = 8
CHANNELS = 2
RATE = 44100
OUTPUT = True

music_file  = "The Principle Of Moments.wav"


_stderr = sys.stderr
null = open(os.devnull,'wb')
sys.stderr = _stderr

s_request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_request.connect((HOST, PORT))

s_command = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_command.connect((HOST, PORT))

s_broadcast = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_broadcast.connect((HOST, PORT))

s_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_listen.connect((HOST, PORT))


wf = wave.open(music_file, 'rb')

if PLAY_AUDIO:
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=OUTPUT)




def action(request_state):
    s_request.sendall(bytes(request_state,'ascii'))
    command = str(s_command.recv(CHUNK),'ascii')

    if command == "broadcast":
        audio_data = wf.readframes(AUDIOCHUNK)
        s_broadcast.sendall(audio_data)
    elif command == "listen":
        audio_data = s_listen.recv(CHUNK)
        if PLAY_AUDIO:
            stream.write(audio_data)
    else:
        command = 'quit'
        s_request.close()
        s_command.close()
        s_broadcast.close()
        s_listen.close()

    print('my request is to ', request_state)
    print('my command is to ', command)
    print('-'*20)
    return command
