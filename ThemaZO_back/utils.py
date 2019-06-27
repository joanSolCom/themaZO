#!/usr/bin/env python
# -*- coding: utf-8 -*-

import constants

def writeLabel(word, label, level = 0):
	#print word.them
	if word.them == constants.EMPTY:
		word.them = label
	elif label == word.them:
		word.them = word.them
	#elif level and word.them != constants.EMPTY:
	#	word.them = label + word.them
	elif word.them[0] in (constants.OPEN_T, constants.OPEN_P):
		word.them += label
	else:
		word.them = label + word.them
	#elif word.them[0] == constants.CLOSE_P:
	#	word.them = label + word.them

def buildLabel(word, span, oneword = 0, count = 1, level = 0):
	if oneword:
		label = constants.OPEN_T + constants.CLOSE_T + span + str(count) 
		writeLabel(word, label)

		if span == constants.SPEC:
			count += 1

	elif span in ("[", "{"):
		writeLabel(word, span)

	elif span == "R" and level:
		labelsplitR = constants.CLOSE_T + span + str(count) + constants.DASH + str(level)
		writeLabel(word, labelsplitR)

	elif span != "P":
		labelT = constants.CLOSE_T + span + str(count)
		writeLabel(word, labelT)

	elif level:
		labelP = constants.CLOSE_P + span + str(count) + constants.DOT + str(level)
		writeLabel(word, labelP, level)

	else:
		labelP = constants.CLOSE_P + span + str(count)
		writeLabel(word, labelP)
		count += 1
	
	return count

def writeThem(sentence, end, start = 1, rheme = 0, spcount = 0, prop = 0, level = 0):
	#print "writing thematicity"
	# single thematicity T or SP
	if rheme:
		buildLabel(sentence.tokens[str(start)], constants.OPEN_T)
		if level:
			buildLabel(sentence.tokens[str(end)], constants.RHEME, 0, 1, level)
		else:
			buildLabel(sentence.tokens[str(end)], constants.RHEME)

	elif end == start and prop == 0:
		if spcount == 0:
			buildLabel(sentence.tokens[str(end)], constants.THEME, 1)
		else:
			spcount = buildLabel(sentence.tokens[str(end)], constants.SPEC, 1, spcount)

	# multi word T or SP
	elif end != start and prop == 0 and rheme == 0:
		buildLabel(sentence.tokens[str(start)], constants.OPEN_T)
		if spcount == 0:
			buildLabel(sentence.tokens[str(end)], constants.THEME)

		else:
			spcount = buildLabel(sentence.tokens[str(end)], constants.SPEC, 0, spcount)

	elif level:
		buildLabel(sentence.tokens[str(start)], constants.OPEN_P)
		buildLabel(sentence.tokens[str(end)], constants.PROP, 0, prop, level)

	elif prop:
		buildLabel(sentence.tokens[str(start)], constants.OPEN_P)
		prop = buildLabel(sentence.tokens[str(end)], constants.PROP, 0, prop)

	return prop, spcount
