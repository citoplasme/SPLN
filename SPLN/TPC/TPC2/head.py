#!/usr/bin/python3

# TPC2 -> filtro head -> f1 f2 (nome ficheiro > 10 primeiras linhas)
import fileinput
import sys 
	
for file in sys.argv[1:]:
	print('-----------',file,'-----------')
	for text in fileinput.input(file):
		if fileinput.filelineno() < 10:
			print(text)
		else:
			fileinput.close()