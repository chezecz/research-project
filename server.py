# Google API Key
# export GOOGLE_APPLICATION_CREDENTIALS=/Users/cheze/python-XXXXXXXXXXXX.json

import zlib
import queue
import threading
from flask import request
from google.cloud import speech
from flask import Flask
from flask import Response
from flask import stream_with_context

from config import Config

delimeter = '=' * 20

buffer = queue.Queue()

buffer_response = queue.Queue()

def chunks():
    # while there is no silence:
    # while we have regular buffer samples:
    while True:
        try:
            yield buffer.get(timeout = 10)
        except queue.Empty:
            print('break')
            break

app = Flask(__name__)

def get_transcription():
    print("check")
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

    for result in results:
        for data in result.results:
            for parts in data.alternatives:
                print(parts)
                buffer_response.put(parts.transcript)
                # yield f"{delimeter}\n {parts.transcript}\n"


def return_response():
    generator = chunks_response()
    for result in generator:
        yield result

def background_response():
    thread = threading.Thread(target=return_response, args=())
    thread.daemon = True
    thread.start()

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
    if buffer_response.empty():
        return ""
    else:
        return Response(buffer_response.get())

if __name__ == '__main__':
    app.env = "development"
    app.run(debug = True)