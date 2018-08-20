# Google API Key
# export GOOGLE_APPLICATION_CREDENTIALS=/Users/cheze/python-XXXXXXXXXXXX.json

import io
import json
import zlib
from flask import request
from google.cloud import speech
from flask import Flask
from flask import Response
from flask import copy_current_request_context

import time

delimeter = '=' * 20

def get_transcription(content):
    client = speech.SpeechClient()
    config = speech.types.RecognitionConfig(
        encoding='LINEAR16',
        language_code='en-US',
        sample_rate_hertz=44100,
    )

    requests = [speech.types.StreamingRecognizeRequest(audio_content=content)]

    config = speech.types.StreamingRecognitionConfig(config=config, interim_results = True)

    results = client.streaming_recognize(config, requests)

    for result in results:
        for data in result.results:
            for parts in data.alternatives:
                # time.sleep(2)
                yield f"{delimeter}\n {parts.transcript}\n"

app = Flask(__name__)

@app.route("/")
def hello():
    return "Research Project"

@app.route("/request/", methods = ['POST'])
def get_request():
    return Response(get_transcription(zlib.decompress(request.data)), mimetype='text/plain')

if __name__ == '__main__':
    app.env = "development"
    app.run(debug = True)