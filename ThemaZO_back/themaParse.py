#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from itertools import tee, islice, chain, izip
import sys
from conll import ConllStruct
#from syntaxStr import SyntaxStr
from utils import writeThem
from treeOperations import SyntacticTreeOperations

class ThemParser:

	def __init__(self, path, pathIn):
		fd = codecs.open(pathIn,"r",encoding="utf-8")
		raw_conll = fd.read()

		self.iCS = ConllStruct(raw_conll.encode("utf-8"))
		self.conllParse()

	def propAnalyze(self, sentence):
		#print "Enter propAnalyze"
		#print sentence
		endsent = len(sentence.tokens)

		root = []
		i=1
		while i < endsent:
			token = sentence.tokens[str(i)]
			if token.deprel == "ROOT":
				root.append(int(token.id))
				root.append(token)
			if i == endsent - 1:
				endsent = int(token.id)

			i+=1

		return root, endsent

	def thematicity(self, sentence, iTree, idnode, endsent):
		spcount = 1
		splitR1 = 0
		endT = 0
		endSP = 0
		array4level = []

		nodesParent = iTree.get_children_by_parent_id(idnode)
		for n in nodesParent:
			if n.id < idnode and n.arcLabel != "punct":
				subj = 0
				# Theme
				if n.arcLabel in ("nsubj", "nsubjpass"):
					minId, maxId = iTree.get_subtree_span(n)
					writeThem(sentence, maxId, minId)
					array4level = self.form_array(array4level, minId,maxId, "T1")

					endT = maxId
					subj = minId 

				# Frontal Spec
				if n.arcLabel in ("cc", "prep", "advmod", "mark"):
					minId, maxId = iTree.get_subtree_span(n)
					pprop, spcount = writeThem(sentence, maxId, minId, 0, spcount)
					labelsp = "SP"+ str(int(spcount) - 1)
					array4level = self.form_array(array4level, minId,maxId, labelsp)

					endSP = maxId
				# Frontal Rheme
				elif n.arcLabel != "nsubj" and n.pos[0] != "V" and n.id < subj:
					minId2, maxId2 = iTree.get_subtree_span(n)
					writeThem(sentence, maxId2, minId2, 1, 0, 0, 1)
					array4level = self.form_array(array4level, minId2,maxId2, "R1-1")

					splitR1 += 1
					endSP = maxId2
		# Rheme
		endR = endsent
		begR = 1

		if endT > endSP:
			begR = endT + begR
		else:
			begR = endSP + begR

		if splitR1:
			writeThem(sentence, endR, begR, 1, 0, 0, 2)
			array4level = self.form_array(array4level, begR, endR, "R1-2")
		else: 
			writeThem(sentence, endR, begR, 1)
			array4level = self.form_array(array4level, begR, endR, "R1")

		return array4level

	def annot_L2_prop(self,sentence, iTree, node, proposition = 1, level = 0):
		arrayL2P = []
		arrayL2T = []
		array = []

		minId, maxId = iTree.get_subtree_span(node)
		# Write P1.1
		proposition, spc = writeThem(sentence, maxId, minId, 0, 0, proposition, level)
		if level:
			labelP = "P" + str(proposition) + "." + str(level)
		else:
			labelP = "P" + str(proposition)
		arrayL2P = self.form_array(arrayL2P, minId, maxId, labelP)

		arrayL2T = self.thematicity(sentence, iTree, int(node.id), maxId)

		array.append(arrayL2P)
		array.append(arrayL2T)

		return proposition, array

	def themeL2(self, sentence, iTree, idnode):
		nodesParent = iTree.get_children_by_parent_id(idnode)
		array4level = []
		maxId = 1
		for n in nodesParent:
			if n.id < idnode and n.arcLabel != "punct":
				# Theme
				if n.arcLabel == "nsubj":
					minId, maxId = iTree.get_subtree_span(n)
					writeThem(sentence, maxId, minId)
					array4level = self.form_array(array4level, minId, maxId, "T1")
					maxId += 1

		return maxId, array4level

	def annot_L1_prop(self, sentence, iTree, nodeStr, root, proposition):
		#print "Entering L1 prop annot"
		nodetype = nodeStr[0]
		node = nodeStr[3]
		minId, maxId = iTree.get_subtree_span(node)
		arrayL1T = []
		arrayL1 = []
		arrayL2T = []

		# Theme. Check here in case there is a frontal SP for P1
		startT = 1
		endT = len(sentence.tokens) - 1
		if minId and maxId and int(node.id) > int(root.id):
			#print "Entering frontal Theme"
			endT = minId -1
			# Theme L1
			if nodetype == "causal":
				writeThem(sentence, endT, startT)
				arrayL1T = self.form_array(arrayL1T, startT, endT, "T1")
			proposition += 1
			proposition, sp = writeThem(sentence, endT, startT, 0, 0, proposition)
			arrayL1 = self.form_array(arrayL1, startT, endT, "P" + str(proposition - 1))
			# Theme L2
			maxId2, arrayL2T = self.themeL2(sentence, iTree, int(root.id))
			# Rheme L2
			writeThem(sentence, endT, maxId2, 1)
			arrayL2T = self.form_array(arrayL2T, maxId2, endT, "R1")

			# Rheme L1
			if nodetype == "causal":
				writeThem(sentence, maxId, minId, 1)
				arrayL1T = self.form_array(arrayL1T, minId, maxId, "R1")
			proposition, sp = writeThem(sentence, maxId, minId, 0, 0, proposition)
			arrayL1 = self.form_array(arrayL1, minId, maxId, "P" + str(proposition - 1))
			# SP L2
			writeThem(sentence, minId, minId, 0, 1)
			arrayL2T = self.form_array(arrayL2T, minId, minId, "SP1")
			# Theme L2
			maxId3, arrayT = self.themeL2(sentence, iTree, int(node.id))
			if arrayT:
				arrayL2T.append(arrayT[0])
			# Rheme L2
			if maxId3 < minId:
				maxId3 = minId + 1
			writeThem(sentence, maxId, maxId3, 1)
			arrayL2T = self.form_array(arrayL2T, maxId3, maxId, "R1")

		elif minId and maxId and int(node.id) < int(root.id):
			#print "Entering Frontal Rheme"
			startT = maxId + 1

			# Rheme L1
			writeThem(sentence, maxId, minId, 1)
			proposition += 1
			proposition, sp = writeThem(sentence, maxId, minId, 0, 0, proposition)
			# SP L2
			writeThem(sentence, minId, minId, 0, 1)
			arrayL2T = self.form_array(arrayL2T, minId, minId, "SP1")

			# Theme L2
			maxId2, arrayT = self.themeL2(sentence, iTree, int(n.id))
			arrayL2T.append(arrayT[0])

			if maxId2 < minId:
				maxId2 = minId + 1
			# Rheme L2
			writeThem(sentence, maxID, maxId2, 1)
			arrayL2T = self.form_array(arrayL2T, maxId2, maxId, "R1")

			# Theme L1
			writeThem(sentence, endT, startT)
			proposition, sp = writeThem(sentence, endT, startT, 0, 0, proposition)
			# Theme L2
			maxId3, arrayT2 = self.themeL2(sentence, iTree, int(root.id))
			arrayL2T.append(arrayT2[0])
			# Rheme L2
			writeThem(sentence, endT, maxId3, 1)
			arrayL2T = self.form_array(arrayL2T, maxId3, endT, "R1")

		array1 = []
		if arrayL1T:
			array1.append(arrayL1T)
			array1.append(arrayL1)
			array1.append(arrayL2T)
		else:
			array1.append(arrayL1)
			array1.append(arrayL2T)

		return proposition, array1

	def get_type_struc(self, iTree, root):
		typeStr = []

		nodes = iTree.get_children_by_parent_id(root)
		cause = 0
		coord = 0
		#print nodes
		for n in nodes: 
			if n.arcLabel == "cc":
				coord = int(n.id)

			if n.arcLabel == "advcl":
				nodes2 = iTree.get_children_by_parent_id(int(n.id))
				for n2 in nodes2:
					if n2.lemma in ("because", "porque", "weil", "if", "si", "wenn"):
						cause = int(n2.id)
				if cause:
					typeStr.append("causal")
					typeStr.append(cause)
					typeStr.append(int(n.id))
					typeStr.append(n)
				else:
					typeStr.append("subord")
					typeStr.append(int(n.id))
					typeStr.append(n)
			elif n.arcLabel in ("csubj","ccomp", "xcomp", "relcl"):
				typeStr.append("subord")
				typeStr.append(int(n.id))
				typeStr.append(n)
			elif n.pos == "VBN" and n.arcLabel == "conj" and coord:
				typeStr.append("coord")
				typeStr.append(coord)
				typeStr.append(int(n.id))
				typeStr.append(n)	
			# Falta yuxtaposicion

		if typeStr == []:
			typeStr.append("simple")

		return typeStr

	def form_array(self, array, start, end, label):
		span = (start, end, label)
		array.append(span)

		return array

	def conllParse(self):
		new_sent = []
		array4web = []
		sentCount = 0
		for sentence in self.iCS.sentences:
			array4sent = []
			sentCount += 1
			levelcount = 1
			propcount = 1

			endsent = len(sentence.tokens)

			root, endsent = self.propAnalyze(sentence)

			print "################"
			print sentCount
			print "\n"
			iTree = SyntacticTreeOperations(sentence.raw_sentence)

			typeStr = self.get_type_struc(iTree, root[0])

			# Causal sentence
			if typeStr[0] == "causal":
				#print "Causal sentence found"
				propcount, arrayL1 = self.annot_L1_prop(sentence, iTree, typeStr, root[1], propcount)
				for l in arrayL1:
					#print l
					array4sent.append(l)

			# Coordination
			if typeStr[0] == "coord":
				#print "Coordination found"
				propcount, arrayL1 = self.annot_L1_prop(sentence, iTree, typeStr, root[1], propcount)
				for l in arrayL1:
					#print l
					array4sent.append(l)

			# Subordination
			if typeStr[0] == "subord":
				#print "Subordinated sentence found"
				# Level 1 them
				arrayL1 = self.thematicity(sentence, iTree, root[0], endsent)
				array4sent.append(arrayL1)

				subord = typeStr[2]
				propcount, arrayL2 = self.annot_L2_prop(sentence, iTree, subord, propcount, levelcount)
				
				for a in arrayL2:
					array4sent.append(a)
				#print sentence

			# Thematicity annotation Level 1
			else:
				array4level = self.thematicity(sentence, iTree, root[0], endsent)
				array4sent.append(array4level)

			for s in array4sent:
				array4web.append(s)

		#print array4web
			print sentence
			print array4sent
'''
			# Code for printing CONLL output
			for token in sentence:
				tokens.append(str(token))

			tokens= "\n".join(tokens)
			new_sent.append(tokens)

		new_conll = "\n\n".join(new_sent)
#		print new_conll
		result = open(path + "output.conll", "w")
		result.write(new_conll)
		result.close()
		print "New conll has been printed"
'''

if __name__ == '__main__':
	path = "/home/upf/Desktop/docs/themaParse/"
	pathIn = path + "them/selection1.conll"
	# cd Desktop/de && python mod1_synt2them.py out_eval.conll eval_them.conll
	#path = sys.argv[1]

	iT = ThemParser(path, pathIn)
