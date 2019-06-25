from sqlEmbeddings import SQLEmbeddings
from pprint import pprint

class ThematicProgression():

	def __init__(self, iT, corefs):
		self.iT = iT
		self.corefs = corefs
		self.iSQL = SQLEmbeddings()
		dist, components = self.computeProgression()

		self.distances = dist
		self.components = components

	def computeProgression(self):
		levels = self.iT.levels
		previousTheme = None
		previousRheme = None
		previousThemeStr = None
		previousPron = False

		nTokens = len(self.iT.iCS.sentences[0])
		hyperTheme, _ = self.getSpan(0 ,1, nTokens)
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
			pron = False

			for start, end, label in firstLevel:

				if label.startswith("T"):
					spantheme = (start, end)
					theme, pron = self.getSpan(idS ,start, end)
					themeVector = self.iSQL.getMsgVector(theme)
				if label.startswith("R"):
					spanrheme = (start, end)
					rheme, _ = self.getSpan(idS, start, end)
					rhemeVector = self.iSQL.getMsgVector(rheme)
			
			dTheme = -1
			dRheme = -1
			dHyper = -1
			
			print(theme, previousThemeStr, pron)

			if theme:
				if previousTheme:
					if previousPron:
						print("IM HERE", theme, previousThemeStr)
						dHyper = -10
						dTheme = -10
						if self.isCoref(theme, previousThemeStr):
							dTheme="coref"
					else:
						if not pron:
							dTheme = self.iSQL.distance(themeVector, previousTheme)[0][0]
							dHyper = self.iSQL.distance(themeVector, hyperThemeVector)[0][0]
						else:
							print("IM HERE", theme, previousThemeStr)
							dHyper = -10
							dTheme = -10
							if self.isCoref(theme, previousThemeStr):
								dTheme="coref"

							
				if previousRheme:
					if not pron:
						dRheme = self.iSQL.distance(themeVector, previousRheme)[0][0]
					else:
						dRheme = -10

				distances.append([dTheme, dRheme, dHyper])

				previousThemeStr = theme
				previousTheme = themeVector
				previousPron = pron
				previousRheme = rhemeVector
				components.append([theme, rheme])


		return distances, components

	def isCoref(self, theme, prevTheme):
		for chain in self.corefs:
			if theme in chain and prevTheme in chain:
				return True

		return False



	def getSpan(self, idSentence, start, end):
		sent = self.iT.iCS.sentences[idSentence]
		posTag = None
		pron = False
		if start == end:
			span = sent.tokens[str(start)].form
			posTag = sent.tokens[str(start)].pos

		else:
			i = start
			span = ""
			while i <= end:
				span += sent.tokens[str(i)].form + " "
				i+=1

		if posTag and posTag in ["PRP","DT"]:
			pron = True

		return span.strip().lower(), pron
