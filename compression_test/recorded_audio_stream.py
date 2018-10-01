import pyaudio
import zlib
import io
import os
import sys
import audioop
import time
import asyncio
import socket
import wave

from config.config import Audio
from config.config import Server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

file_name = os.path.join(
    os.path.dirname(__file__),
    '../resources',
    sys.argv[1])

wf = wave.open(file_name, 'rb')

def callback(input_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    message = audioop.lin2adpcm(data, 2, None)
    get_transcription(message[0])
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
        data, addr = sock.recvfrom(1024)
        if data:
            print (data.decode())

    stream.stop_stream()
    stream.close()
    p.terminate()

def get_transcription(data):
    sock.sendto(zlib.compress(data), (Server.host, Server.port))

if __name__ == '__main__':
    record_audio()