import pyaudio
import audioop
import time
from config.config import Audio

def callback(input_data, frame_count, time_info, status):
    message = audioop.lin2adpcm(input_data, 2, None)
    message = audioop.adpcm2lin(message[0], 2, None)
    return (message[0], pyaudio.paContinue)

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format = Audio.a_format,
        channels = Audio.channels,
        rate = Audio.rate,
        input = True,
        output = True,
        frames_per_buffer = Audio.chunk,
        stream_callback = callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()

record_audio()