import pyaudio
import audioop
import time

from opuslib import Encoder, Decoder

from config.config import Audio

rate = 48000
channels = 2
chunk = 960

enc = Encoder(rate, channels, 'audio')
dec = Decoder(rate, channels)

def callback(input_data, frame_count, time_info, status):
    audio_encoded = enc.encode(input_data, chunk)
    audio_decoded = dec.decode(audio_encoded, chunk)
    return (audio_decoded, pyaudio.paContinue)

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format = Audio.a_format,
        channels = channels,
        rate = rate,
        input = True,
        output = True,
        frames_per_buffer = chunk,
        stream_callback = callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()

record_audio()