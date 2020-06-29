import fileinput
import re
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import sys
import pygraphviz as pgv

def gettexto():
    texto = ""
    for line in fileinput.input():
        texto += line
    return texto

def trim_text(text):
    return re.sub(r"Page \| \d+ Harry Potter and the Philosophers Stone - J\.K\. Rowling", "", text) 

def entidades(texto):
    maius = r'(?:[A-Z]\w+(?:[-\']\w+)*|(?:[A-Z]\.)+|[IVXLCDM]+)'
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

def clear_list(lista):
    pronomes = [r"{I}", r"{You}", r"{He}", r"{She}", r"{It}", 
                r"{Oh}", r"{What}", r"{We}", r"{Yes}",r"{That}", 
                r"{So}", r"{They}", r"{And}", r"{There}"]
    # Remover duplicados
    lista = list(dict.fromkeys(lista))
    # Remover pronomes
    for item in lista:
        if item in pronomes:
            lista.remove(item)
    return lista

def contagem(listas):
    dic = {}
    for lista in listas:
        lista = clear_list(lista)
        if len(lista) > 1:
            for pair in itertools.combinations(lista, r=2):
                l = [pair[0], pair[1]]
                l.sort()
                s = l[0] + l[1]
                dic[s] = dic.get(s,0) + 1
    return dic
    
def dictionary_to_graph(counter):
    G = nx.Graph()
    seen = set()
    for key, val in sorted(counter.items(), key=lambda x : x[1], reverse=False):
        l = re.findall(r'{.*?}', key)
        for item in l:   
            if item not in seen:
                G.add_node(item)
                seen.add(item)
        G.add_edge(l[0], l[1], label=val)
    return G

def print_graph(G):
    A = nx.nx_agraph.to_agraph(G)
    print(A)
    A.layout('dot')
    #A.draw('output/grafo.png')
    A.draw('output/grafo.png', prog='circo')
    #A.draw('output/grafo_dot.png', prog='dot')

def print_dic(counter):
    total = 0
    for key, val in sorted(counter.items(), key=lambda x : x[1], reverse=False):
        print(key, ' - ', val)
        total += val
    print(total)

def trim_dic(counter, threshold):
    for key, val in sorted(counter.items(), key=lambda x : x[1], reverse=False):
        if val < threshold:
            del counter[key]
    return counter

def trim_grafo(G):
    pronomes = [r"{I}", r"{You}", r"{He}", r"{She}", r"{It}", 
                r"{Oh}", r"{What}", r"{We}", r"{Yes}",r"{That}", 
                r"{So}", r"{They}", r"{And}", r"{There}", r"{But}"
                r"{Well}", r"{No}", r"{Why}", r"{How}", r"{The}"]
    for pronome in pronomes:
        try:
            G.remove_node(pronome)
        except:
            pass 
    return G

def interpretador(G, person):
    try:
        return list(G.neighbors("{" + person + "}"))
    except:
        #print("A pessoa em questão não se encontra no grafo.")
        #return []
        return "A pessoa em questão não se encontra no grafo."

def loop_inter(G):
    for line in sys.stdin:
        if(line.rstrip() == 'quit'):
            break
        else:
            print(interpretador(G,line.rstrip()))
            print("Indique a personagem:")

            
def main():
    txt = gettexto()
    txt = trim_text(txt)
    fr = frases(txt)
    ents = entidades(fr)
    periodos = split_frases(ents)
    pares = pair_everyone(periodos)
    counter = contagem(pares)
    #print_dic(counter)
    counter = trim_dic(counter, 12)
    print_dic(counter)
    G = dictionary_to_graph(counter)
    G = trim_grafo(G)
    #print(interpretador(G,"Nicolas Flamel"))
    print_graph(G)
    print("Indique a personagem:")
    loop_inter(G)
    
if __name__ == "__main__":
    main()

