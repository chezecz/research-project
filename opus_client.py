import pyaudio
import audioop
import time
import socket
import zlib

from opuslib import Encoder

from config import Opus, Server

enc = Encoder(Opus.rate, Opus.channels, 'audio')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def callback(input_data, frame_count, time_info, status):
    audio_encoded = enc.encode(input_data, Opus.chunk)
    get_transcription(zlib.compress(audio_encoded))
    return (input_data, pyaudio.paContinue)

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format = Opus.a_format,
        channels = Opus.channels,
        rate = Opus.rate,
        input = True,
        frames_per_buffer = Opus.chunk,
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
    sock.sendto(data, (Server.host, Server.port))

if __name__ == '__main__':
    record_audio()