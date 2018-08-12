import json
import requests
from flask import jsonify
from flask import request

from flask import Flask

from apikey import apiKey

baseURL = "https://speech.googleapis.com"
requestURL = f"{baseURL}/v1/speech:recognize?key={apiKey}"

def getTranscription(data):
	req = requests.post(requestURL, json = data).json()
	print(req)
	return jsonify(req)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/request/", methods = ['POST'])
def getRequest():
	# jsondata = request.get_json()
	# data = json.loads(jsondata)
	print(request.get_json())
	print(getTranscription(request.get_json()))
	return "Test"

if __name__ == '__main__':
    app.env = "development"
    app.run(debug = True)