import io
import base64
from google.cloud import speech

client = speech.SpeechClient()
config = speech.types.RecognitionConfig(
        encoding='LINEAR16',
        language_code='en-US',
        sample_rate_hertz=44100,
    )

with io.open('./resources/audio.wav', 'rb') as audio:
    audio_content = audio.read()

requests = [speech.types.StreamingRecognizeRequest(audio_content=audio_content)]

config = speech.types.StreamingRecognitionConfig(config=config)

results = client.streaming_recognize(config, requests)

for result in results:
    print(result)