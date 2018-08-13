import base64
import json
import os
import io
import requests
import sys
import time

start_time = time.time()

file_name = os.path.join(
    os.path.dirname(__file__),
    'resources',
    sys.argv[1])

with io.open(file_name, 'rb') as audio:
    audio_content = audio.read()
    content = base64.b64encode(audio_content)



res = requests.post('http://127.0.0.1:5000/request/', data=audio_content)
for result in res['results']:
    for alternative in result:
        print(result[alternative][0]['transcript'])

elapsed_time = time.time() - start_time
print(elapsed_time)