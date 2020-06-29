import re
import math
import fileinput
import sys
import json
import uuid 
from collections import Counter
import numpy as np
from num2words import num2words
import spacy
nlp = spacy.load("pt_core_news_sm")

# Função para lemmatizar um texto, após converter para minúsculas as palavras só
# remove tudo o que não seja palavra
def pre_process(text):
    # Converte números para o seu formato textual
    text = re.sub(r'\d+(\.\d+)?', lambda x : num2words(x.group(), lang='pt'), text)
    # Remove tudo o que não sejam palavras e converte para minúsculas
    text = " ".join(re.split(r'\s+', re.sub(r'[^\w\s-]', '', text).lower()))
    # Aplica a lemmatização e retorna
    return " ".join([token.lemma_ for token in nlp(text)])

# Função para armazenar um array de objetos json em ficheiro
def save_to_file(data, name):
    f = open(name, "w")
    dados = json.dumps(data, indent = 4, ensure_ascii = False)
    f.write(dados)
    f.close()
    print("File saved.")

# Carregamento dos dados vindos do ficheiro JSON
def get_from_file():
    with open('dados/reviews_full.json') as json_file:
        data = json.load(json_file)
    return data

def main():
    reviews = get_from_file()
    for review in reviews:
        review['lemmatized'] = {}
        review['lemmatized']['title'] = pre_process(review['title'])
        review['lemmatized']['synopsis'] = pre_process(review['synopsis'])
        review['lemmatized']['subtitle'] = pre_process(review['subtitle'])
        review['lemmatized']['text'] = pre_process(review['text'])     
    save_to_file(reviews, "dados/reviews_lemmatized.json")  

if __name__ == '__main__':
    main()