# Apanhar pares de entidades - nomes que aparecam na mm frase -> contador 
# Marcação dos amigos com quem coesistem mais 

import fileinput
import re
import itertools

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

def split_frases(texto):
    periodos = texto.split('@')
    return periodos

def pair_everyone(periodos):
    res = []
    for lista in periodos:    
        res.append(re.findall(r'{.*?}', lista))
    return res

def contagem(listas):
    dic = {}
    for lista in listas:
        if len(lista) > 1:
            for pair in itertools.combinations(lista, r=2):
                s = pair[0] + pair[1]
                dic[s] = dic.get(s,0) + 1
    return dic
    #my_list = [1,2,3,4]
    #for pair in itertools.combinations(my_list, r=2):
    #    print(*pair)


def main():
    txt = gettexto()
    fr = frases(txt)
    ents = entidades(fr)
    periodos = split_frases(ents)
    pares = pair_everyone(periodos)
    counter = contagem(pares)
    for key, val in sorted(counter.items(), key=lambda x : x[1], reverse=False):
        print(key, ' - ', val)


if __name__ == "__main__":
    main()

