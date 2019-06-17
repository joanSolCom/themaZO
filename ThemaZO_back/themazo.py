from flask import Flask
from flask_jsonpify import jsonify
import json

app = Flask(__name__)


@app.route('/getConll')
def hello():
	raw = open("output.conll").read()
	sentences = raw.split("\n\n")
	dictJson = {}
	dictJson["raw"] = raw
	dictJson["sentences"] = []
	for sentence in sentences:
		dictS = {}
		dictS["sentence"] = sentence
		dictS["tokens"] = []
		for token in sentence.split("\n"):
			dictS["tokens"].append(token)

		dictJson["sentences"].append(dictS)

	jsonStr = json.dumps(dictJson)
	return jsonify(jsonStr)

if __name__ == '__main__':
    app.run()