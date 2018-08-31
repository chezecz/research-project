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
    while True:
        yield buffer.get()

app = Flask(__name__)

asdf = None

background = None

@app.before_first_request
def activate_job():
    global background, asdf

    generator = chunks()

    def do_transcription():
        global asdf
        asdf = 'run!2!!'
        app.logger.info('do_222transcription log')
        client = speech.SpeechClient()
        config = speech.types.RecognitionConfig(
            encoding=Config.encoding,
            language_code=Config.language,
            sample_rate_hertz=Config.rate
        )
        requests = (speech.types.StreamingRecognizeRequest(audio_content=chunk) for chunk in generator)
        config = speech.types.StreamingRecognitionConfig(config=config, interim_results = True)
        print("starte2d")
        results = client.streaming_recognize(config, requests)

        for result in results:
            print(result)
            for data in result.results:
                for parts in data.alternatives:
                    yield f"{delimeter}\n {parts.transcript}\n"

    def do_transcription2():
        global asdf
        asdf = 'run!!!'
        app.logger.info('do_transcription log')
        print("started")
        client = speech.SpeechClient()
        config = speech.types.RecognitionConfig(
            encoding=Config.encoding,
            language_code=Config.language,
            sample_rate_hertz=Config.rate
        )

        requests = [speech.types.StreamingRecognizeRequest(audio_content=chunk) for chunk in chunks()]

        config = speech.types.StreamingRecognitionConfig(config=config, interim_results = True)

        results = client.streaming_recognize(config, requests)

        for result in results:
            print(result)
            for data in result.results:
                for parts in data.alternatives:
                    yield f"{delimeter}\n {parts.transcript}\n"



    print("thread started")
    app.logger.info('thread started log')
    print(do_transcription)
    background = threading.Thread(target=do_transcription, args=())
    print(background)
    background.start()
    app.logger.info('thread started log2')
    print("thread")
    time.sleep(1.0)

    print(background)
    print('asdf = ' + str(asdf))
    do_transcription2()


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