
cnt = 3

while cnt < 4:

	taleID = "0"+str(cnt)
	taleName = "tale"+taleID+"en_comm_aaaa.txt"

	gold = open("./data/tale"+taleID+"en_comm_GOLD.txt","r").read().split("\n\n")
	test = open("aaaa","r").read().split("\n\n")

	print("###########################")
	print("RESULTS FOR TALE "+taleName)

	i = 0

	nCorrect = 0 
	nTokens = 0
	while i < len(gold):
		sentenceGold = gold[i]
		sentenceTest = test[i]
		j = 0
		tokensGold = sentenceGold.split()
		tokensTest = sentenceTest.split()
		while j < len(tokensGold):
			print(tokensGold[j], tokensTest[j])
			if tokensGold[j] == tokensTest[j]:
				print("correct!")
				nCorrect+=1
			j+=1
			nTokens+=1

		i+=1

	print("AS")
	print(nCorrect / nTokens)

	nCorrect = 0 
	nBrackets = 0
	nTokens = 0
	i = 0

	while i < len(gold):
		sentenceGold = gold[i]
		sentenceTest = test[i]
		j = 0
		tokensGold = sentenceGold.split()
		tokensTest = sentenceTest.split()

		while j < len(tokensGold):
			if "[" in tokensGold[j] or "{" in tokensGold[j] or "}" in tokensGold[j] or "]" in tokensGold[j]:
				if tokensGold[j] == tokensTest[j]:
					nCorrect+=1
				nTokens+=1

			j+=1

		i+=1
	print("LBS")
	print(nCorrect / nTokens)

	
	

	nCorrect = 0 
	nBrackets = 0
	nTokens = 0
	i = 0

	while i < len(gold):
		sentenceGold = gold[i]
		sentenceTest = test[i]
		j = 0
		tokensGold = sentenceGold.split()
		tokensTest = sentenceTest.split()

		while j < len(tokensGold):
			if "[" in tokensGold[j] or "{" in tokensGold[j] or "}" in tokensGold[j] or "]" in tokensGold[j]:
				labelG = tokensGold[j].replace("P","").replace("R","").replace("T","").replace(".","").replace("S","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","")
				labelT = tokensTest[j].replace("P","").replace("R","").replace("T","").replace(".","").replace("S","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","")
				#print(labelG, labelT)
				if labelG == labelT:
					#print("correct")
					nCorrect+=1
				nTokens+=1

			j+=1

		i+=1

	print("UBS")
	print(nCorrect / nTokens)
	
	cnt+=1
	print("###########################")
	exit()