import re
import sys
import random as rand
import numpy as np
import pandas as pd

if ".txt" not in sys.argv[1]:
	print("please enter a valid .txt file")
	sys.exit(0)
	
with open("./"+sys.argv[1], "r", encoding="utf-8") as f:
    text = f.read()


print("cleaning text...")
text = re.sub(r"\n"," ",text)
text = re.sub(r"\.\.\.",".",text)
text = re.sub(r"[.!?]"," </s> <s> ",text)
text = re.sub(r","," ",text)
text = re.sub(r"\W+--\W+"," ",text)
text = re.sub(r"\W+-\W+"," ",text)
text = "<s> " +text.lower()

words = text.split()

wordsClean = []
print("seperating text...")
for word in words:
	word = word.strip()
	if(word != ""):
		wordsClean.append(word)


kSMOOTH = 1
numWords = len(wordsClean)

unigrams = {}
print("building unigrams...")
for word in wordsClean:
	if word in unigrams.keys():
		unigrams[word]= unigrams.get(word)+1
	else:
		unigrams[word] = 1

numUnigrams = len(unigrams.keys())

bigrams = {}
i = 0
print("building bigrams...")
while i < len(wordsClean)-1:
	biStr = wordsClean[i] + " " + wordsClean[i+1]
	if biStr in bigrams.keys():
		bigrams[biStr]= bigrams.get(biStr)+1
	else:
		bigrams[biStr] = 1
	i+=1
	
trigrams = {}
i = 0
print("building trigrams...")
while i < len(wordsClean)-2:
	triStr = wordsClean[i] + " " + wordsClean[i+1] + " " +wordsClean[i+2]
	if triStr in trigrams.keys():
		trigrams[triStr]= trigrams.get(triStr)+1
	else:
		trigrams[triStr] = 1
	i+=1
#for word in trigrams.keys():
#print(f"{word} : {trigrams.get(word)}")
print("--done modeling--")
		
while(True):
	usrIn = input("Enter a sentence (or \"random\", or \"done\"): ")
	usrIn = usrIn.lower()
	if usrIn == "done":
		print("bye bye")
		break
	elif usrIn == "random":
		#unigram random
		w = []
		p = []
		for word in unigrams.keys():
			if word == "<s>":
				continue
			w.append(word)
			p.append(unigrams.get(word)/(numWords-unigrams.get("<s>")))
		print(f"unigram sentence: ",end="")
		while(True):
			word = np.random.choice(w,p=p)
			if word == "</s>":
				break
			else:
				print(f"{word} ",end="")
		print("\n")
		#bigram random

		prevWord = "<s>"
		print("bigram sentence: ", end="")

		while True:
			w = []
			p = []
			for bis in bigrams.keys():
				if bis.startswith(prevWord + " "):
					nextWord = bis.split()[1]  
					w.append(nextWord)
					p.append(bigrams[bis] / unigrams[prevWord])

            # normalize just in case
			p = np.array(p, dtype=float)
			p = p / p.sum()

			word = np.random.choice(w, p=p)
			if word == "</s>":
				break

			print(f"{word} ", end="")
			prevWord = word   # now it's just the last token

		print("\n")
		#trigram random

		prevWord = "<s>"
		print("trigram sentence: ", end="")
		#start with a bigram prob
		w = []
		p = []
		for bis in bigrams.keys():
			if bis.startswith(prevWord + " "):
				nextWord = bis.split()[1]  
				w.append(nextWord)
				p.append(bigrams[bis] / unigrams[prevWord])

		p = np.array(p, dtype=float)
		p = p / p.sum()

		word = np.random.choice(w, p=p)
		print(f"{word} ", end="")
		prevWord = word

		given = "<s> " + prevWord
		while True:
			w = []
			p = []
			for tris in trigrams.keys():
				if tris.startswith(given + " "):
					nextWord = tris.split()[2]  
					w.append(nextWord)
					p.append(trigrams[tris] / bigrams[given])

			p = np.array(p, dtype=float)
			p = p / p.sum()

			word = np.random.choice(w, p=p)
			if word == "</s>":
				break

			print(f"{word} ", end="")
			given = prevWord + " " + word
			prevWord = word

		print("\n")
			
		
	else:
		usrInWords = usrIn.split()
		usrInLen = len(usrInWords)
		startToken = "<s>"
		endToken = "</s>"
	#unigram probability
		print("unigram prob: ")
		uniProb = 1
		for word in usrInWords:
			uniProb = (uniProb) * ((unigrams.get(word,0)+kSMOOTH)/numWords)	
			print(f"{unigrams.get(word,0)+kSMOOTH}/{numWords} * ",end="")
		endSentence = unigrams.get("</s>")
		uniProb = uniProb * ((endSentence+kSMOOTH)/numWords)
		print(f"{endSentence+kSMOOTH}/{numWords} ",end="")
		print(f"= {uniProb} (k = {kSMOOTH})")

	#bigram probability
		print("bigram prob: ")
		start = "<s> " + usrInWords[0]
		biProb = (bigrams.get(start,0)+kSMOOTH)/(unigrams.get("<s>",0) + (numUnigrams * kSMOOTH)) 
		i = 0
		print(f"{bigrams.get(start,0)+kSMOOTH}/{(unigrams.get(startToken,0) + (numUnigrams * kSMOOTH))} * ",end="")
		while(i<len(usrInWords)-1):
			curBi = usrInWords[i]+ " " + usrInWords[i+1]
			biProb = biProb * ((bigrams.get(curBi,0)+kSMOOTH)/(unigrams.get(usrInWords[i],0) + (numUnigrams * kSMOOTH)))
			print(f"{bigrams.get(curBi,0)+kSMOOTH}/{(unigrams.get(usrInWords[i],0) + (numUnigrams * kSMOOTH))} * ",end="")
			i+=1
		endBi = usrInWords[-1] + " </s>"
		biProb *= (bigrams.get(endBi,0)+kSMOOTH) / (unigrams.get(usrInWords[-1],0) + (numUnigrams * kSMOOTH))
		print(f"{bigrams.get(usrInWords[i]+endToken,0)+kSMOOTH}/{(unigrams.get(usrInWords[i],0) + (numUnigrams * kSMOOTH))} ",end="")
		print(f"= {biProb} (k = {kSMOOTH})")

	#trigram
		print("trigram prob: ")
		start = "<s> " + usrInWords[0]
		#start with a bigram, there aren't enough tokens behind the first word
		triProb = (bigrams.get(start,0)+kSMOOTH)/(unigrams.get("<s>",0) + (numUnigrams * kSMOOTH)) 
		print(f"{bigrams.get(start,0)+kSMOOTH}/{(unigrams.get(startToken,0) + (numUnigrams * kSMOOTH))} * ",end="")

		fTri = start + " " + usrInWords[1]
		triProb *= (trigrams.get(fTri,0)+kSMOOTH)/(bigrams.get(start,0) + (numUnigrams * kSMOOTH)) 
		print(f"{trigrams.get(fTri,0)+kSMOOTH}/{(bigrams.get(start,0) + (numUnigrams * kSMOOTH))} * ",end="")

		i = 0
		while (i<len(usrInWords)-2):
			given = usrInWords[i]+" "+usrInWords[i+1]
			curTri =(usrInWords[i]+" "+usrInWords[i+1]+" " +usrInWords[i+2])
			triProb *= (trigrams.get(curTri,0)+kSMOOTH)/(bigrams.get(given,0) + (numUnigrams * kSMOOTH)) 
			print(f"{trigrams.get(curTri,0)+kSMOOTH}/{(bigrams.get(given,0) + (numUnigrams * kSMOOTH))} * ",end="")
			i+=1
		given = usrInWords[-2] + " " + usrInWords[-1]
		endTri = usrInWords[-2] + " " + usrInWords[-1] + " </s>"
		triProb *= (trigrams.get(endTri,0)+kSMOOTH)/(bigrams.get(given,0) + (numUnigrams * kSMOOTH)) 
		print(f"{trigrams.get(endTri,0)+kSMOOTH}/{(bigrams.get(given,0) + (numUnigrams * kSMOOTH))} * ",end="")
		print(f"= {triProb} (k = {kSMOOTH})")

		
			
		








