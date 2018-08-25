import pyaudio
import requests
import zlib
import time

from config import Audio

frames = []

def callback(input_data, frame_count, time_info, status):
    global frames
    frames.append(input_data)
    return (input_data, pyaudio.paContinue)

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format = Audio.a_format,
        channels = Audio.channels,
        rate = Audio.rate,
        input = True,
        stream_callback = callback)

    # frames = []

    # print("Recording...")
    # for i in range (0, int(Audio.rate / Audio.chunk * Audio.record_seconds)):
    #     audio_content = stream.read(Audio.chunk)
    #     frames.append(audio_content)

    # print('Stop recording')

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    # audio_content = stream.read(Audio.chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()
    get_transcription(b''.join(frames))
    # return b''.join(frames)
    return None

def get_transcription(data):
    for part in requests.post('http://127.0.0.1:5000/request/', data=zlib.compress(data), stream=True):
        print (f"{part.decode('utf-8')}\n")

if __name__ == '__main__':
    record_audio()