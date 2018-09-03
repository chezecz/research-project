import pyaudio
import requests
import zlib
import time
import pydub
import io
import subprocess

from pydub import AudioSegment

from config import Audio

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
    for part in requests.post('http://127.0.0.1:5000/request/', data=zlib.compress(data), stream=True):
        print (f"{part.decode('utf-8')}")
        # print(part)

if __name__ == '__main__':
    record_audio()