# Google API Key
# export GOOGLE_APPLICATION_CREDENTIALS="/Users/cheze/python-XXXXXXXXXX.json"

import base64
import sys
import json
import requests

def encode_audio(audio):
    audio_content = audio.read()
    return base64.b64encode(audio_content)