#!/usr/bin/python3

# Retangulo de * com 10x20
#print((s * 20 + '\n') * 10)

def retangulo(l, a, s = '*'):
	return (s * l + '\n' +
		(s + ' '*(l-2) + s + '\n') * (a-2) + 
		s * l + '\n')

print(retangulo(5,15,'.'))