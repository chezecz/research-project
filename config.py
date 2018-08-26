import pyaudio

class Config:
	encoding = 'LINEAR16'
	language = 'en-US' # language_code
	rate = 44100 # sample_rate_hertz

class Audio:
	a_format = pyaudio.paInt16
	chunk = 4096
	width = 2
	channels = 1
	rate = 44100
	record_seconds = 2