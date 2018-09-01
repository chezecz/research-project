# Google API Key
# export GOOGLE_APPLICATION_CREDENTIALS=/Users/cheze/python-XXXXXXXXXXXX.json

import zlib
import queue
import threading
import time
from flask import request
from google.cloud import speech
from flask import Flask
from flask import Response

from config import Config

delimeter = '=' * 20

buffer = queue.Queue()

def chunks():
    data = []
    while True:
        yield buffer.get()

app = Flask(__name__)

def get_transcription():
    generator = chunks()
    client = speech.SpeechClient()
    config = speech.types.RecognitionConfig(
        encoding=Config.encoding,
        language_code=Config.language,
        sample_rate_hertz=Config.rate
    )
    config = speech.types.StreamingRecognitionConfig(config=config, interim_results = True)
    requests = (speech.types.StreamingRecognizeRequest(audio_content=chunk) for chunk in generator)
    results = client.streaming_recognize(config, requests)

    print('here')
    for result in results:
        print(result)
        for data in result.results:
            for parts in data.alternatives:
                yield f"{delimeter}\n {parts.transcript}\n"

@app.before_first_request
def activate_job():
    background = threading.Thread(target=get_transcription, args=())
    background.daemon = True
    background.start()

@app.route("/")
def hello():
    return "Research Project"

@app.route("/request/", methods = ['POST'])
def get_request():
    buffer.put(zlib.decompress(request.data))
    return Response('ok')

if __name__ == '__main__':
    app.env = "development"
    app.run(debug = True)