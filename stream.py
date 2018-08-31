import pyaudio
import requests
import zlib
import time
import pydub
import io
import subprocess

from pydub import AudioSegment

from config import Audio

frames = []

def callback(input_data, frame_count, time_info, status):
    global frames
    frames.append(input_data)
    get_transcription(b''.join(frames))
    return (input_data, pyaudio.paContinue)

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format = Audio.a_format,
        channels = Audio.channels,
        rate = Audio.rate,
        input = True,
        frames_per_buffer = Audio.chunk,
        stream_callback = callback)

    # frames = []

    # print("Recording...")
    # for i in range (0, int(Audio.rate / Audio.chunk * Audio.record_seconds)):
    #     audio_content = stream.read(Audio.chunk)
    #     # AudioSegment(audio_content, sample_width = Audio.width, frame_rate = Audio.rate, channels = Audio.channels)
    #     # AudioSegment.from_file(audio_content).export(x, format = "mp3")
    #     frames.append(audio_content)

    # print('Stop recording')

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    # audio_content = stream.read(Audio.chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # ffmpeg -i input.flv -f s16le -acodec pcm_s16le output.raw

    # ffmpegcmd = ['ffmpeg', '-f', 'u16le', '-ac', '1', '-ar', '44100', '-i',  'rawaudio']
    # ffmpeg = subprocess.Popen(ffmpegcmd, stdin = b''.join(frames), stdout = subprocess.PIPE)
    # data = io.BytesIO(p.stdout)
    # return data
    # y = b''.join(frames)
    # AudioSegment(y, sample_width = Audio.width, frame_rate = Audio.rate, channels = Audio.channels)
    # s = io.BytesIO(y)
    # AudioSegment.from_file(s).export(x, format = "mp3")
    # return b''.join(frames)
    # return x
    return None

def get_transcription(data):
    for part in requests.post('http://127.0.0.1:5000/request/', data=zlib.compress(data), stream=True):
        print (f"{part.decode('utf-8')}\n")

if __name__ == '__main__':
    # get_transcription()
    record_audio()