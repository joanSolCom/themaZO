from flask_jsonpify import jsonify
import json
from flask import Flask, app, request, url_for, Response
from logging.handlers import RotatingFileHandler
from logging import Formatter, INFO
import spacy
from themaParse import ThemParser
from themaProg import ThematicProgression

from flask import g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cache = {}

def load_spacy():
	print("loading spacy")
	en_nlp = spacy.load('en_core_web_sm')
	print("loaded")
	return en_nlp

en_nlp = load_spacy()

def process(text):
	doc = en_nlp(text)

	textConll = ""
	for sent in doc.sents:
		s = []
		sentConll = ""
		for token in sent:
			if token.text.strip():
				s.append(token.text)
				lineConll = str(token.i - sent.start + 1)+"\t"+token.text+"\t"+token.lemma_+"\t"+token.tag_+"\t"+token.dep_+"\t"+str(token.head.i - sent.start + 1)+"\n"
				sentConll+=lineConll

		textConll+=sentConll+"\n"


	sentences = textConll.strip().split("\n\n")
	dictJson = {}
	dictJson["raw"] = textConll
	dictJson["sentences"] = []
	for sentence in sentences:
		dictS = {}
		dictS["sentence"] = sentence
		dictS["tokens"] = []
		for token in sentence.split("\n"):
			dictS["tokens"].append(token)

		dictJson["sentences"].append(dictS)

	jsonStr = json.dumps(dictJson)
	return jsonify(jsonStr), textConll


@app.route('/getConll', methods=['POST'])
def getConll():
	arguments = request.form
	text = arguments["text"].strip().replace('"',"").replace("'","")
	jsonStr, textConll = process(text);
	cache["conll"] = textConll
	return jsonStr

@app.route("/getThematicity" , methods=['POST'])
def getThematicity():
	iT = ThemParser(raw_conll=cache["conll"])
	cache["iT"] = iT

	levels = iT.levels
	print("LEVELSSSS",levels, len(levels))
	sentences = cache["conll"].strip().split("\n\n")
	dictJson = {}
	dictJson["sentences"] = []

	for idS, sentence in enumerate(sentences):
		dictS = {}
		dictS["text"] = ""
		dictS["tokens"] = []
		for token in sentence.split("\n"):
			tokenComponents = token.split("\t")
			if len(tokenComponents) > 1:
				dictS["text"] += tokenComponents[1] + " "
				dictS["tokens"].append(tokenComponents[1])

		dictS["text"] = dictS["text"].strip()
		dictS["components"] = levels[idS]
		dictJson["sentences"].append(dictS)

	jsonStr = json.dumps(dictJson)
	return jsonify(jsonStr)

@app.route('/getThematicProgression', methods=["POST"])
def getThematicProgression():
	iTP = ThematicProgression(cache["iT"])
	dictJSON = {}
	dictJSON["distances"] = iTP.distances
	dictJSON["components"] = iTP.components
	dictJSON["hypernode"] = iTP.hypernode
	jsonStr = json.dumps(dictJSON)
	return jsonify(jsonStr)


@app.route('/getTestConll')
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

@app.route('/getTestThematicity')
def getTestThematicity():
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