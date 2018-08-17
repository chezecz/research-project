import io
import sys
import os
import base64
from google.cloud import speech

file_name = os.path.join(
    os.path.dirname(__file__),
    'resources',
    sys.argv[1])

with io.open(file_name, 'rb') as audio:
    audio_content = audio.read()
    content = base64.b64encode(audio_content)

client = speech.SpeechClient()
config = speech.types.RecognitionConfig(
	encoding='LINEAR16',
	language_code='en-US',
	sample_rate_hertz=44100,
	)

config = speech.types.StreamingRecognitionConfig(config=config)
requests = [speech.types.StreamingRecognizeRequest(audio_content=content,)]

responses = client.streaming_recognize(config, requests)
print(dir(responses))
for response in responses:
	for result in response:
		for alternative in result.alternative:
			print('=' * 20)
			print('transcript: ' + alternative.transcript)
			print('is final: ' + str(result.is_final))