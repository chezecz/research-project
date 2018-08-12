import json
import requests
from flask import jsonify
from flask import request

from flask import Flask

from apikey import api_key

base_URL = "https://speech.googleapis.com"
request_URL = f"{base_URL}/v1/speech:recognize?key={api_key}"

def get_transcription(data):
	return jsonify(requests.post(request_URL, json = data).json())

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/request/", methods = ['POST'])
def get_request():
	return (get_transcription(json.loads(request.get_json())))

if __name__ == '__main__':
    app.env = "development"
    app.run(debug = True)