#!/usr/bin/python3

# TPC2 -> Em vez de split usar re.findall() 
import fileinput
import re
	
counter = {}	

for text in fileinput.input():
	text = text.strip()
	
	lista = re.findall(r"\w+",text)

	for i in lista:
		if len(i) > 0:
			counter[i] = counter.get(i,0) + 1

for key, val in sorted(counter.items(), key=lambda x : x[1], reverse=True):
	print(key, ' - ', val)