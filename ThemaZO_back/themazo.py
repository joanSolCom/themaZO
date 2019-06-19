from flask_jsonpify import jsonify
import json
from flask import Flask, app, request, url_for, Response
from logging.handlers import RotatingFileHandler
from logging import Formatter, INFO
app = Flask(__name__)


@app.route('/getConll')
def test():
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

@app.route('/getThematicity')
def getThematicity():
	raw = open("output.conll").read()
	sentences = raw.split("\n\n")
	dictJson = {}
	dictJson["sentences"] = []

	for sentence in sentences:
		dictS = {}
		dictS["text"] = ""
		dictS["tokens"] = []
		for token in sentence.split("\n"):
			tokenComponents = token.split("\t")
			if len(tokenComponents) > 1:
				dictS["text"] += tokenComponents[1] + " "
				dictS["tokens"].append(tokenComponents[1])

		dictS["text"] = dictS["text"].strip()
		dictS["components"] = [[(1,9,"T1"),(10,20,"R1")],[(1,9,"P2"),(10,20,"P3")],[(1,1,"SP"),(2,2,"T1"),(3,9,"R1"),(10,10,"SP1"),(11,20,"R1")]]
		dictJson["sentences"].append(dictS)

	jsonStr = json.dumps(dictJson)
	return jsonify(jsonStr)


if __name__ == '__main__':
    app.debug = True
    app.config['PROPAGATE_EXCEPTIONS'] = True

    LOG_FILEPATH = "/home/joan/repository/PhD/FLASKVersion/logs/log.txt"

    formatter = Formatter("[%(asctime)s]\t%(message)s")
    handler = RotatingFileHandler(LOG_FILEPATH, maxBytes=10000000, backupCount=1)
    handler.setLevel(INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.run(port=5000, debug=True)