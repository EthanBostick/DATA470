import re

with open("clnPrimeCorpus.txt", "r", encoding="utf-8") as f:
    text = f.read()

lis = re.findall(r"\W+object\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'object' appears {len(lis)}")

lis = re.findall(r"\W+game\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'game' appears {len(lis)}")

lis = re.findall(r"\W+oh\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'oh' appears {len(lis)}")

lis = re.findall(r"\W+uh+\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'uh' appears {len(lis)}")

lis = re.findall(r"\W+um+\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'um' appears {len(lis)}")

lis = re.findall(r"\W+ah+\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'ah' appears {len(lis)}")

lis = re.findall(r"\W+design\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'design' appears {len(lis)}")

lis = re.findall(r"\W+(?:develop|development)\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'develop/development' appears {len(lis)}")

lis = re.findall(r"\.[^.]*\buh\b[^.]*\buh\b[^.]*\.",text,flags=re.I)
#print(f"{lis}\n")
print(f"'uh' appears twice in a line {len(lis)} times")

lis = re.findall(r"\.[^.]*\bum\b[^.]*\bum\b[^.]*\.",text,flags=re.I)
#print(f"{lis}\n")
print(f"'um' appears twice in a line {len(lis)} times")

lis = re.findall(r"\W+fun\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'fun' appears {len(lis)}")

lis = re.findall(r"\W+the\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'the' appears {len(lis)}")

lis = re.findall(r"\W+of\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'of' appears {len(lis)}")


lis = re.findall(r"\W+oop\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'oop' appears {len(lis)}")

lis = re.findall(r"\W+ecs\W+",text,flags=re.I)
#print(f"{lis}")
print(f"the word 'ecs' appears {len(lis)}")

lis = re.findall(r"(\.[^.]*\bfun\b[^.]*\bgame\b[^.]*)\.|\.([^.]*\bgame\b[^.]*\bfun\b[^.]*\.)",text,flags=re.I)
#print(f"{lis}\n")
print(f"'fun' and 'game' appear {len(lis)} times in a sentence")

lis = re.findall(r"\.[^.]*\W+pajamas\W+[^.]*\.",text,flags=re.I)
print(f"{lis}")
print(f"the word 'pajamas' appears {len(lis)}")

lis = re.findall(r"[.?!][^.?!]+[.?!]",text,flags=re.I)
print(f"{len(lis)} sentences")
words =[]
for sentence in lis:
	spaceNum= re.findall(r" ",sentence)
	words.append(len(spaceNum))
#find mean
nsum = 0
for num in words:
	nsum += num	
mean = nsum/len(words)
print(f"{mean} average num of words")

words.sort()
#print(f"{words} words, words")






