# Google API Key
# export GOOGLE_APPLICATION_CREDENTIALS="/Users/cheze/python-XXXXXXXXXX.json"

import base64
import sys
import json
import os
import io
import requests

file_name = os.path.join(
    os.path.dirname(__file__),
    'resources',
    'audio.mp3')

with io.open(file_name, 'rb') as audio:
    audio_content = audio.read()
    print(base64.b64encode(audio_content))
    # return base64.b64encode(audio_content)

# def encode_audio(audio):
#     audio_content = audio.read()
#     return base64.b64encode(audio_content)