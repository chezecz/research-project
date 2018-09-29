import socket
import pyaudio
import zlib
import io
import asyncio
import audioop
import time

from config import Audio
from config import Server

sock = socket.connect('127.0.0.1')

class Client:
    def __init__(self, ipAddress, portNumber, timeout = None):
        self.sock = socket.create_connection((ipAddress, portNumber), timeout)

    def get(self, key):
        self.sock.sendall(message)

        data = self.sock.recv(1024).decode()
        print(data)

    def put(self, key, value, timestamp = None):
        if timestamp == None:
            timestamp = str(int(time.time()))
        self.sock.sendall("put {} {} {}\n".format(key, value, timestamp).encode())

        if self.sock.recv(1024).decode() != "ok\n\n":
            raise ClientError()

def callback(input_data, frame_count, time_info, status):
    message = audioop.lin2adpcm(input_data, 1, None)
    # get_transcription(message[0])
    get_transcription(input_data)
    return (input_data, pyaudio.paContinue)

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format = Audio.a_format,
        channels = Audio.channels,
        rate = Audio.rate,
        input = True,
        frames_per_buffer = Audio.chunk,
        stream_callback = callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()

def get_transcription(data):
    sock.sendall(data)