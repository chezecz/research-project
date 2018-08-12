import json
import requests
from flask import jsonify
from flask import request

from flask import Flask

from apikey import apiKey

baseURL = "https://speech.googleapis.com"
requestURL = f"{baseURL}/v1/speech:recognize?key={apiKey}"

def getTranscription(data):
	return jsonify(requests.post(requestURL, json = data).json())

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/request/", methods = ['POST'])
def getRequest():
	return (getTranscription(json.loads(request.get_json())))

if __name__ == '__main__':
    app.env = "development"
    app.run(debug = True)