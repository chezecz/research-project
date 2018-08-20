import pyaudio
import requests
import zlib
import time

from config import Audio

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format = Audio.a_format,
        channels = Audio.channels,
        rate = Audio.rate,
        input = True,
        frames_per_buffer = Audio.chunk)

    frames = []

    print("Recording...")
    for i in range (0, int(Audio.rate / Audio.chunk * Audio.record_seconds)):
        audio_content = stream.read(Audio.chunk)
        frames.append(audio_content)

    print('Stop recording')
    stream.stop_stream()
    stream.close()
    p.terminate()
    return b''.join(frames)

def get_transcription():
    for part in requests.post('http://127.0.0.1:5000/request/', data=zlib.compress(record_audio()), stream=True):
        print (f"{part.decode('utf-8')}\n")

if __name__ == '__main__':
    get_transcription()