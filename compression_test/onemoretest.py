import pyaudio
import wave
import io
import sys
import os
import time

from opuslib import Encoder, Decoder

file_name = os.path.join(
    os.path.dirname(__file__),
    '../resources',
    sys.argv[1])

rate = 48000
channels = 2
chunk = 960

enc = Encoder(rate, channels, 'audio')
dec = Decoder(rate, channels)

wf = wave.open(file_name, 'rb')

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
	data = wf.readframes(frame_count)
	opus_audio = enc.encode(data, 960)
	print(len(data))
	print(len(opus_audio))
	decoded = dec.decode(opus_audio, 960)
	return (decoded, pyaudio.paContinue)

stream = p.open(format= p.get_format_from_width(wf.getsampwidth()), 
	channels = wf.getnchannels(), 
	rate = wf.getframerate(), 
	output = True,
	stream_callback = callback)

stream.start_stream()

while stream.is_active():
	time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()
