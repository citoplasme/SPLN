#!/usr/local/bin/python3
import fileinput
import re
import matplotlib.pyplot as plt

polarities = {}
for line in fileinput.input(['sentilex.txt']):
    word = re.split(',', line)[0]
    aux = re.search(r'N0=(\-?\d+)', line)
    if aux:
    	polarity = aux.group(1)
    	polarities[word] = int(polarity)

total_pos = 0
total_neg = 0
pos = 0
neg = 0
chapter = 0
palavras = 0
negatives = []
positives = []
chapters = []
for line in fileinput.input():
	word = line.split()
	if len(word) == 3:
		if word[0] == 'Capítulo':
			print('Capítulo', chapter)
			print(neg)
			negatives.append(neg)
			print(pos)
			positives.append(pos)
			print(palavras)
			chapters.append(chapter)
			neg = 0
			pos = 0
			chapter += 1
			palavras = 0
		else:
			lower_case = word[0].lower()
			x = polarities.get(lower_case, 0)
			if x == -1:
				neg += 1
				total_neg += 1
			elif x == 1:
				pos += 1
				total_pos += 1
			palavras += 1
print('Capítulo', chapter)
print(neg)
negatives.append(neg)
print(pos)
positives.append(pos)
print(palavras)
chapters.append(chapter)

n = [item / total_neg for item in negatives]
p = [item / total_pos for item in positives]

res = list(-x+y for x, y in list(zip(n, p)))

plt.plot(chapters, res, drawstyle='steps-mid')
plt.ylabel('Density')
plt.xlabel('Polarity')
plt.show()
