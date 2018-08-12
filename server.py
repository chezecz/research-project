import json
import requests
from flask import jsonify
from flask import request

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/request/", methods = ['POST'])
def getRequest():
	jsondata = request.get_json()
	data = json.loads(jsondata)
	print(data)
	return jsonify(data)

if __name__ == '__main__':
    app.env = "development"
    app.run(debug = True)