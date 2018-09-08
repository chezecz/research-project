import pyaudio
import requests
import zlib
import time
import pydub
import io
import subprocess
import asyncio

from pydub import AudioSegment

from config import Audio
from config import Server

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()

def callback(input_data, frame_count, time_info, status):
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

    return None

def get_transcription(data):
    loop = asyncio.get_event_loop()
    message = zlib.compress(data)
    connect = loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(message, loop),
        remote_addr=(Server.host, Server.port))
    transport, protocol = loop.run_until_complete(connect)
    loop.run_forever()
    transport.close()
    loop.close()


if __name__ == '__main__':
    record_audio()