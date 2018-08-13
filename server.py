import json
import requests
import time
from flask import jsonify
from flask import request

from flask import Flask

from apikey import api_key

base_URL = "https://speech.googleapis.com"
request_URL = f"{base_URL}/v1/speech:recognize?key={api_key}"

def get_transcription(data):
	# start_time = time.time()
	return jsonify(requests.post(request_URL, json = data).json())
	# elapsed_time = time.time() - start_time
	# print(elapsed_time)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Research Project"

@app.route("/request/", methods = ['POST'])
def get_request():
	return (get_transcription(json.loads(request.get_json())))

if __name__ == '__main__':
    app.env = "development"
    app.run(debug = True)