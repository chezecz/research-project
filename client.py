import base64
import sys
import json
import os
import io
import requests

file_name = os.path.join(
    os.path.dirname(__file__),
    'resources',
    'audio.wav')

with io.open(file_name, 'rb') as audio:
    audio_content = audio.read()
    content = base64.b64encode(audio_content)

jsonQuery = {'config': {'encoding':'LINEAR16','sampleRateHertz':'16000','languageCode':'en-US'}}, {'audio':{'content':content.decode("utf-8")}}
s = json.dumps(jsonQuery)

res = requests.post('http://127.0.0.1:5000/request/', json=s)
print(res)