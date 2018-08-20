import pyaudio

class Config:
	encoding = 'LINEAR16'
	language = 'en-US' # language_code
	rate = 44100 # sample_rate_hertz

class Audio:
	a_format = pyaudio.paInt16
	chunk = 1024
	width = 2
	channels = 2
	rate = 44100
	record_seconds = 2