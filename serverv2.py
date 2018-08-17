import json
import requests
from flask import jsonify
from flask import request

from flask import Flask

from apikey import api_key

base_URL = "https://speech.googleapis.com"
request_URL = f"{base_URL}/v1/speech:recognize?key={api_key}"

def get_transcription(data):
	json_query = ({
                'config': 
                    {
                        'encoding':'LINEAR16',
                        'sampleRateHertz':'44100',
                        'languageCode':'en-US'
                    }, 
                'audio':
                    {
                    'content':data.decode('utf-8')
                    }
            })

	return jsonify(requests.post(request_URL, json = json_query).json())

app = Flask(__name__)

@app.route("/")
def hello():
    return "Research Project"

@app.route("/request/", methods = ['POST'])
def get_request():
    return get_transcription(request.data)

if __name__ == '__main__':
    app.env = "development"
    app.run(debug = True)