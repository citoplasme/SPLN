import fileinput
import nltk
from owlready2 import *
import difflib
import pygraphviz as pgv
import networkx as nx
import sys

# Ontology load
onto = get_ontology("book.owl").load()

# Definition of the Character class (Ontology)
class Personagem(Thing):
    namespace = onto

# Definition of the Interaction class (Ontology)
class Interacao(Thing):
    namespace = onto

# Object Properties (Ontology)
class relacao(Personagem >> Interacao):
    namespace = onto

class relacao_inverse(Interacao >> Personagem):
    namespace = onto
    inverse_property = relacao

# Data Properties (Ontology)
class alias(DataProperty):
    namespace = onto
    range = [str]

class value(DataProperty, FunctionalProperty):
    namespace = onto
    range = [int]

# Definition of the Main Characters class (Ontology)
class PersonagemPrincipal(onto.Personagem):
    equivalent_to = [ 
        Personagem 
        #& relacao.some(Interacao)
        & relacao.min(6, Interacao)
    ]

    def info(self): 
        print(f"{self.name} Also known as: {self.alias}")
        for r in self.relacao:
            print(f"{set(r.relacao_inverse)} Interactions: {r.value}")

# Get text from the file
def gettexto():
    texto = ""
    for line in fileinput.input():
        texto += line
    return texto

# Get Named Entities from the file 
def entidades_nltk(text):
    parse_tree = nltk.ne_chunk(nltk.tag.pos_tag(text.split()), binary=True) 
    named_entities = set()
    for t in parse_tree.subtrees():
        if t.label() == 'NE':
            named_entities.add([ " ".join(w for w, t in list(t))][0])
    return named_entities

# Clustering of names and aliases
def clustering(word, lista, dictionary):
    for sentence in lista:
        words = sentence.split()
        l = difflib.get_close_matches(word, words, cutoff=0.8)
        if len(l) > 0:
            value = dictionary.get(word,[])
            value.append(sentence)
            dictionary[word] = value

# Load entities to ontology
def load_ontology(entities):
    for key, val in sorted(entities.items(), key=lambda x : x[1], reverse=False):
        p = Personagem(key)
        p.alias = val

def text_parsing(txt):
    sentences = nltk.sent_tokenize(txt)
    for sent in sentences:
        parse_tree = nltk.ne_chunk(nltk.tag.pos_tag(sent.split()), binary=True) 
        named_entities = set()
        for t in parse_tree.subtrees():
            if t.label() == 'NE':
                named_entities.add([ " ".join(w for w, t in list(t))][0])
        for pair in itertools.combinations(list(named_entities), r=2):
            # GET ID OF CHARACTERS BASED ON ONTOLOGY
            # alias contains Name1
            p1 = onto.search_one(is_a = onto.Personagem, alias = pair[0])
            # alias contains Name2
            p2 = onto.search_one(is_a = onto.Personagem, alias = pair[1])
            if p1 is not None:
                if p2 is not None:
                    # GET RELATIONSHIP OBJECT BETWEEN BOTH CHARACTERS
                    rel = onto.search_one(is_a = onto.Interacao, relacao_inverse = [p1, p2])
                    if rel is not None:
                        # Update the value
                        rel.value += 1
                    else:
                        # Create a new instance and associate it with the characters
                        interacao = Interacao()
                        interacao.value = 1
                        p1.relacao.append(interacao)
                        p2.relacao.append(interacao)
                        #interacao.relacao_inverse.append(p1)
                        #interacao.relacao_inverse.append(p2)

def getMainCharacters():
    sync_reasoner()
    return onto.search(is_a = onto.PersonagemPrincipal, relacao = onto.search(is_a = onto.Interacao))

def onto_to_graph():
    G = nx.Graph()
    seen = set()
    for personagem in onto.search(is_a = onto.Personagem):
        G.add_node(personagem.name)
        #G.add_edge(personagem.name,onto.Personagem.name,color='red',label="is_a")
        for interacao in onto.search(is_a = onto.Interacao, relacao_inverse = personagem):
            G.add_edge(interacao.relacao_inverse[0].name, interacao.relacao_inverse[1].name, label=interacao.value)
    for principal in onto.search(is_a = onto.PersonagemPrincipal):
        G.add_edge(principal.name, onto.PersonagemPrincipal.name, color='red', label="is_a")
    return G
'''
def mysort(s):
  return len(s.split())

def generate_remaining(conjunto, dictionary):
    lista = list(conjunto)
    for key, vals in dictionary.items():
        for val in vals:
            try:
                lista.remove(val)
                print('removi', val)
            except:
                pass 
    lista.sort(key=mysort)
    print(lista)
    for term in lista:
        clustering(term, lista, dictionary)
        #for val in dictionary[term]:
        #    try:
        #        lista.remove(val)
        #        print('removi', val)
        #    except:
        #        pass 
'''

def print_graph(G):
    A = nx.nx_agraph.to_agraph(G)
    #print(A)
    A.layout('dot')
    A.draw('output/grafo.png', prog='dot')
       
def main():
    txt = gettexto()
    ents = entidades_nltk(txt)

    # Dicionario Nome [Alias]
    dictionary = {}
    clustering("Harry", ents, dictionary)
    clustering("Ron", ents, dictionary)
    clustering("Hermione", ents, dictionary)
    clustering("Voldmort", ents, dictionary)
    clustering("Dumbledore", ents, dictionary)
    clustering("Hagrid", ents, dictionary)
    clustering("Draco", ents, dictionary)
    clustering("Snape", ents, dictionary)
    clustering("Keeper Wood", ents, dictionary)
    clustering("Terence Higgs", ents, dictionary)
    
    # Povoar ontologia com alias incluidos
    load_ontology(dictionary)
    #print(onto.Harry.alias)
    
    # Parse do texto com base na ontologia -> povoar relacoes
    text_parsing(txt)
    r = onto.search_one(is_a = onto.Interacao, relacao_inverse = [onto.Harry, onto.Ron])
    print(r, r.value)

    print(onto.search(is_a = onto.Interacao, relacao_inverse = onto.Harry))

    # Get personagens principais
    mcs = getMainCharacters()
    for mc in mcs:
        mc.info()
    #onto.save("book2.owl")
    G = onto_to_graph()
    print_graph(G)



    
if __name__ == "__main__":
    main()

