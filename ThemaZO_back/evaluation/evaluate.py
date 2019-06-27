import sys
sys.path.append('../')
import codecs
from themaParse import ThemParser
import spacy

def process(text, en_nlp):
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

	return textConll

def special_process(text, en_nlp):
	doc = en_nlp(text)

	textConll = ""
	for sent in doc.sents:
		s = []
		sentConll = ""
		for token in sent:
			if token.text.strip():
				s.append(token.text)
				lineConll = str(token.i - sent.start + 1)+"\t"+token.text+"\t"+token.lemma_+"\t"+token.lemma_+"\t"+token.tag_+"\t"+token.tag_+"\t"+"_"+"\t"+"_"+"\t"+str(token.head.i - sent.start + 1)+"\t"+str(token.head.i - sent.start + 1)+"\t"+token.dep_+"\t"+token.dep_+"\t"+"_"+"\t"+"_"+"\n"
				sentConll+=lineConll

		textConll+=sentConll+"\n"

	return textConll

def conllToPlain(conll):
	resultStr = ""
	tokens = conll.strip().split("\n")
	for token in tokens:
		them = token.split("\t")[13]
		form = token.split("\t")[1]

		if "[]" in them:
			pre = them.split("[")[0]
			if pre == "{":
				resultStr += pre + "["+form+"]"+them.split("]")[1] +" "
			else:
				resultStr += "["+form+"]"+them.split("]")[1] +" "
		else:
			if "[" in them or "{" in them:
				resultStr += them+form+" "
			elif "]" in them or "}" in them:
				resultStr += form+them+" "
			else:
				resultStr+=form + " "

		resultStr.strip()

	return resultStr

en_nlp = spacy.load('en_core_web_sm') 
'''
goldC = open("./data/tale01en_comm_RAW.txt","r").read().split("\n\n")

test = open("./data/tale01en_comm_TESTBERND.txt","w")

for idx, sentence in enumerate(goldC):	
	conll = special_process(sentence, en_nlp)
	#iT = ThemParser(raw_conll=conll)
	#print(conll)
	#strR = conllToPlain(iT.conll)
	test.write(conll)

test.close()
'''

test = open("./data/tale01en_comm_TESTBERND.txt","r").read().split("\n\n")
for idx, sentence in enumerate(test):
	print(conllToPlain(sentence))
