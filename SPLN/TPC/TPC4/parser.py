#!/usr/bin/python3

import re 
import sys
import random

def parseGrammar(g):
	axioma = ""
	gram = {}
	t = set()
	g = re.sub(r'#.*','',g)
	for p in re.split(r';',g):
		if re.search(r'->', p):
			lhs, rhss = re.split(r'->',p)
			lhs = lhs.strip()
			if not gram: axioma = lhs
			gram[lhs] = []
			for rhs in re.split(r'\|',rhss):
				rhs_sep = re.findall(r"(?:\w+|\"\"\"(?:.|\n)*?\"\"\"|\".*?\"|\{.*?\})", rhs)
				gram[lhs].append(rhs_sep)
				t |= set(rhs_sep)
	t = t - gram.keys()
	return (gram, axioma, t)


def generator(g, s, t):
	if s.startswith('"""'):
		a = re.sub(r'\{(.*?)\}', lambda gr : generator(g,gr[1],t), s)
		return re.sub(r'"', '',a)
	if s == '_N':
		return str(random.randint(0,100))
	if s.startswith('__'):
		s = s.replace('_','')
		lines = open(s + '.txt').read().splitlines()
		myline =random.choice(lines)
		return myline
	if s.startswith('{'):
		acao = s.replace('{','').replace('}','')
		return str(eval(acao))
	if s in t:
		return s.replace('"','')
	else:
		rhs = random.choice(g[s])
		return " ".join([generator(g, sim, t) for sim in rhs])

def main():
	ficheiro = open(sys.argv[1]).read()
	prods, defs = ficheiro.split('%%')
	exec(defs, globals())
	
	g, ax, t = parseGrammar(prods)
	print('Gramática:',g,'\nAxioma:',ax, '\nTerminais:', t)
	print('Gerador:', generator(g, ax, t))

if __name__ == "__main__":
    main()


