import re;

with open("emily.txt", "r", encoding="utf-8") as f:
    text = f.read()

lis = re.findall(r"\W?storm\W?",text,flags=re.I)
#print(f"{lis}\n")
print(f"1) Emily uses the word 'storm' {len(lis)} times")

lis = re.findall(r"\W?live[sd]*\W?",text,flags=re.I)
#print(f"{lis}\n")
print(f"2) Emily uses the word 'live/lives/lived' {len(lis)} times")

lis = re.findall(r"\W?die[sd]?\W?",text,flags=re.I)
#print(f"{lis}\n")
print(f"3) Emily uses the word 'dies/die/died' {len(lis)} times")

lis = re.findall(r"\W?(?:housewives|housewife)\W?",text,flags=re.I)
#print(f"{lis}\n")
print(f"4) Emily uses the word 'housewife/housewives' {len(lis)} times")

lis = re.findall(r"\boh\b.*\boh\b.*",text,flags=re.I)
#print(f"{lis}\n")
print(f"5) {lis[0]}")

lis = re.findall(r"\n.*\benough\b.*\benough\b.*\n",text,flags=re.I)
#print(f"{lis}\n")
print(f"6) 'enough' appears twice in a line {len(lis)} times")

lis = re.findall(r"\W?((mon|tues|wednes|thurs|fri|satur|sun)day)\W?",text,flags=re.I)
#print(f"{lis}\n")
print("7) Emily only refers to saturday and sunday, once respectively")

lis = re.findall(r"\W?(january|febuary|march|april|may|june|july|august|semptember|october|november|december)\W?",text,flags=re.I)
#print(f"{lis}\n")
lis = re.findall(r"\W?june\W?",text,flags=re.I)
#print(f"{lis}\n{len(lis)}")
lis = re.findall(r"\W?may\W?",text,flags=re.I)
#print(f"{lis}\n{len(lis)}")

print(f"8) Emily references the month 'may' the most and {len(lis)} times")

lis = re.findall(r"\W?a?sleep[s]?\W*\n",text,flags=re.I)
#print(f"{lis}\n")
print(f"9) Emily says sleep/asleep/sleeps {len(lis)} times")

lis1 = re.findall(r".*\bbe\b.*\bbee\b.*",text,flags=re.I)
lis2 = re.findall(r".*\bbee\b.*\bbe\b.*",text,flags=re.I)
if(len(lis1)!=0):
	print(f"10) {lis1[0]}")
else:
	print(f"10) {lis2[0]}")


lis = re.findall(r"\n[a-z']+[^\na-z]+[a-z']+[^\na-z]+[a-z']+\W*\n",text,flags=re.I)
#print(f"{lis}\n")
print(f"11) {len(lis)} sentences are exactly 3 words long")

lis = re.findall(r"\W?lip[s]?\W*\n",text,flags=re.I)
#print(f"{lis}\n")
print(f"12) Emily says lip/lips at the end of a line {len(lis)} times")

lis = re.findall(r".*\blove\b.*\blove\b.*\n",text,flags=re.I)
print(f"13) {lis}")

lis = re.findall(r"\W+\w*[^e0-9]ath\W+",text,flags=re.I)
#print(f"{lis}\n")
print(f"14) {len(lis)} lines end with ath but no eath")


lis = re.findall(r".*\b(\w+)\b.*\b\1+\b.*\n+",text,flags=re.I)
print(f"15) lines had the same word atleast twice {len(lis)}")

lis = re.findall(r"\n[a-z']+[^\na-z]+[a-z']+\W*\n",text,flags=re.I)
#print(f"{lis}\n")
print(f"16) {len(lis)} sentences are exactly 2 words long")


print("17) lines with same word 3 times:")
pattern = r".*\b(?P<word>\w+)\b.*\b(?P=word)\b.*\b(?P=word)\b.*"
for m in re.finditer(pattern, text, flags=re.I):
    print( m.group(0))






