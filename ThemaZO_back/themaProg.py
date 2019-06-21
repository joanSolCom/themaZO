from sqlEmbeddings import SQLEmbeddings
from pprint import pprint

class ThematicProgression():

	def __init__(self, iT):
		self.iT = iT
		self.iSQL = SQLEmbeddings()
		dist, components = self.computeProgression()
		pprint(dist)
		pprint(components)
		self.distances = dist
		self.components = components

	def computeProgression(self):
		levels = self.iT.levels
		previousTheme = None
		previousRheme = None

		nTokens = len(self.iT.iCS.sentences[0])
		hyperTheme = self.getSpan(0 ,1, nTokens)
		self.hypernode = hyperTheme
		hyperThemeVector = self.iSQL.getMsgVector(hyperTheme)

		distances = []
		components = []

		for idS, sentenceLevel in enumerate(levels):
			firstLevel = sentenceLevel[0]
			spantheme = None
			spanrheme = None
			theme = None
			rheme = None
			themeVector = None
			rhemeVector = None

			for start, end, label in firstLevel:
				if label.startswith("T"):
					spantheme = (start, end)
					theme = self.getSpan(idS ,start, end)
					themeVector = self.iSQL.getMsgVector(theme)
				if label.startswith("R"):
					spanrheme = (start, end)
					rheme = self.getSpan(idS, start, end)
					rhemeVector = self.iSQL.getMsgVector(rheme)
			
			dTheme = -1
			dRheme = -1
			dHyper = -1

			if theme:
				if previousTheme:
					dTheme = self.iSQL.distance(themeVector, previousTheme)[0][0]
					dHyper = self.iSQL.distance(themeVector, hyperThemeVector)[0][0]

				if previousRheme:
					dRheme = self.iSQL.distance(themeVector, previousRheme)[0][0]

				distances.append([dTheme, dRheme, dHyper])

				previousTheme = themeVector
				previousRheme = rhemeVector
				components.append([theme, rheme])


		return distances, components

	def getSpan(self, idSentence, start, end):
		sent = self.iT.iCS.sentences[idSentence]
		if start == end:
			span = sent.tokens[str(start)].form
		else:
			i = start
			span = ""
			while i <= end:
				span += sent.tokens[str(i)].form + " "
				i+=1

		return span.strip()
