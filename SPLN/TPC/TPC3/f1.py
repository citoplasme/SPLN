# TPC -> Harry Potter -> Entidades (Algumas entidades falham por existirem aspas a começar frases por exemplo)
import fileinput
import re

def gettexto():
    texto = ""
    for line in fileinput.input():
        texto += line
    return texto

def entidades(texto):
    maius = r'(?:[A-Z]\w+(?:[-\']\w+)*|[A-Z]\.|[IVXLCDM]+)'
    de = r'(?:de|da|dos|das)' 
    s = r'\s+'
    arroba = r'[^@\w]'
    ent = f"({arroba})({maius}(?:{s}{maius}|{s}{de}{s}{maius})*)"
    texto = re.sub(ent, r'\1{\2}', texto)
    return texto

def frases(texto):
    e1 = r'(\n\n+\s*)([A-Z])'
    e2 = r'([a-z][.?!]+[\s]*)([A-Z])'
    texto = re.sub(e1,r'\1@\2',texto)
    texto = re.sub(e2,r'\1@\2',texto)
    return texto

def main():
	print(entidades(frases(gettexto())))

if __name__ == "__main__":
    main()


# Apanhar pares de entidades - nomes que aparecam na mm frase -> contador 
# Marcação dos amigos com quem coesistem mais 
