import pyaudio
import zlib
import io
import audioop
import time
import asyncio
import socket

from config import Audio
from config import Server

i = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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