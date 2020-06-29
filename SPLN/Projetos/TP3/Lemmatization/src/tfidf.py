import re
import math
import fileinput
import sys
import json
import uuid 
from collections import Counter
import numpy as np
import spacy
nlp = spacy.load("pt_core_news_sm")

# tf_idf = term frequency * inverse document frequency

docs = {}
tf   = {}
df   = {}

# titulo + subtitulo + sinopse + corpo = 1
titulo = 0.4
subtitulo =  0.3
sinopse = 0.2
corpo = 0.1

# Converter um texto para uma listagem de apenas palavras, sem separadores, tudo em minusculas
def text_to_words(text):
    return re.split(r'\s+', re.sub(r'[^\w\s-]', '', text).lower())

def count_words(words, uniq_words):
    parsed = []
    for word in words:
        # Remoção de possíveis espaços
        word = word.strip()
        # Caso a palavra não seja vazia
        if word:
            parsed.append(word)
            uniq_words.add(word)

    return Counter(parsed)

# Adicionar um documento aos dicionarios
def add_doc(doc):
    # Cálculo da lista de palavras no corpo
    words = text_to_words(doc['lemmatized']['text'])
    # Cálculo da lista de palavras no título
    words_title = text_to_words(doc['lemmatized']['title'])
    # Cálculo da lista de palavras no subtítulo
    words_subtitle = text_to_words(doc['lemmatized']['subtitle'])
    # Cálculo da lista de palavras na sinopse
    words_synopsis = text_to_words(doc['lemmatized']['synopsis'])
    
    # Cada documento é indexado com um identfificador único
    file_id = str(uuid.uuid4()) 

    # Armanezar os dados textuais e contadores de totais de palavras
    docs[file_id] = {
        'image': doc['image'],
        'link': doc['link'],
        'score': doc['score'],
        'date': doc['date'],
        'title': doc['title'],
        'synopsis': doc['synopsis'],
        'subtitle': doc['subtitle'],
        'text': doc['text'],
        'lemmatized' : {
            'title' : doc['lemmatized']['title'], 
            'subtitle' : doc['lemmatized']['subtitle'], 
            'synopsis' : doc['lemmatized']['synopsis'],
            'text' : doc['lemmatized']['text']
        },
        'total_words': len(words) + len(words_title) + len(words_subtitle) + len(words_synopsis),
        'title_words': len(words_title),
        'subtitle_words': len(words_subtitle),
        'synopsis_words': len(words_synopsis),
        'text_words': len(words)
    }

    # Não repetir palavras - apenas um cálculo
    uniq_words = set()
    
    # Cálculo dos dicionários de ocorrências de cada parte do documento
    counter_text = count_words(words, uniq_words)
    counter_synopsis = count_words(words_synopsis, uniq_words)
    counter_subtitle = count_words(words_subtitle, uniq_words)
    counter_title = count_words(words_title, uniq_words)

    # Entrada de TF no documento é composta por vários dicionários
    tf[file_id] = {
        'title' : counter_title,
        'subtitle' : counter_subtitle,
        'synopsis' : counter_synopsis,
        'text' : counter_text
    }

    #print(json.dumps(tf[file_id]['title'].get('devils', 0), indent = 4, ensure_ascii = False))



    #for word in words:
        # Remoção de possíveis espaços
    #    word = word.strip()
        # Caso a palavra não seja vazia
    #    if word:
            # Incrementar o valor no dicionario de TF da palavra para o documento em questão
    #        tf[(word, file_id)] = tf.get((word, file_id), 0) + 1
            #tf[(word, file_id)]['text'] = tf.get((word, file_id), {}).get('text',0) + 1
            # Adicionar a palavra ao SET
    #        uniq_words.add(word)
    
    # Percorrer as palavras no SET
    for word in uniq_words:
        # Incrementar o valor no dicionario de DF da palavra
        # df(t) = occurrence of t in documents
        df[word] = df.get(word, 0) + 1

# Calcular o valor de TF com base no termo e no documento
# tf(t,d) = count of t in d / number of words in d
def calc_tf(term, file_id, context):
    # Caso o termo nao exista no dicionario de TF, o valor é 0
    count = tf.get(file_id, {}).get(context, {}).get(term, 0)
    # Retorna contagem do termo no documento a dividir pelo total de palavras do documento
    return count / docs[file_id]['total_words']

# Calcular o valor de IDF do termo
# idf(t) = N/df
def calc_idf(term):
    # Retorna 1 / valor do termo no dicionario de DF -> 1 caso não exista
    #return 1 / df.get(term, 1)
    
    # Retorna log da divisão do total de documentos pelo valor do termo no dicionario de DF -> 1 caso não exista
    return np.log(len(docs) / df.get(term, 1))

# Calcular métrica de TF IDF do termo
def calc_tf_idf(term):
    res = {}
    # Cálculo do IDF do termo
    idf = calc_idf(term)
    # Cálculo de TF IDF por todos os documentos
    for file_id in docs:
        # Cálculo do TF para o termo e documento
        tf = calc_tf(term, file_id, 'text')
        tf_title = calc_tf(term, file_id, 'title')
        tf_subtitle = calc_tf(term, file_id, 'subtitle')
        tf_synopsis = calc_tf(term, file_id, 'synopsis')
        # TD IDF do documento para o termo é a multiplicação da métrica TF por IDF
        res[file_id] = tf * idf * corpo + tf_title * idf * titulo + tf_subtitle * idf * subtitulo + tf_synopsis * idf * sinopse
    # Retorna dicionário com os identificadores dos documentos e o valor da métrica 
    return res

# Pesquisar vários termos nos documentos
def search_terms(terms):
    scores = {}
    res = {}
    for term in terms:
        # Calcular o dicionário de score de TF IDF do termo 
        scores[term] = calc_tf_idf(term) #calc_tf_idf(term, 'title') * titulo + calc_tf_idf(term, 'subtitle') * subtitulo + calc_tf_idf(term, 'synopsis') * sinopse + calc_tf_idf(term, 'text') * corpo
        # Por cada documento no dicionário de scores
        for file_id in scores[term]:
            # O resultado é a soma dos vários scores do termo nos documentos
            res[file_id] = res.get(file_id, 0) + scores[term][file_id]
    # Retorna uma lista ordenada dos items do dicionario
    return sorted(res.items(), key=lambda x: x[1], reverse=True)

# Função para imprimir os resultados da pesquisa
def print_search(term, scores):
    print('Search term: '+term)
    for s in scores:
        print('  '+s[0]+': '+docs[s[0]]['title']+' ('+str(s[1])+')')
    print('\n')

# Filtrar os documentos com valor de TF IDF maior do que 0
def filter_not_zero(scores):
    return list(filter(lambda entrada: entrada[1] > 0, scores))

# Função de pesquisa dos vários termos
def search(terms):
    # Colocar termos em minusculas
    terms = map(str.lower, terms)
    # Lemmatizar os termos
    terms = list(terms)
    for i in range(0,len(terms)):
        terms[i] = nlp(terms[i])[0].lemma_
    # Calcular Scores
    scores = search_terms(terms)
    filtered = filter_not_zero(scores)
    #print_search(' '.join(terms), scores)
    #print_search(' '.join(terms), filtered)
    return filtered

# Carregamento dos dados vindos do ficheiro JSON
def get_from_file(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def get_review_from_id(id):
    return docs.get(id, {})

#def main():
#    reviews = get_from_file()
#    for review in reviews:
#        add_doc(review)
#    valores = search(sys.argv[1:])
#    print_search(' '.join(sys.argv[1:]), valores)

#if __name__ == '__main__':
#    main()

try:
    reviews = get_from_file('dados/reviews_lemmatized.json')
    for review in reviews:
        add_doc(review)
except Exception:
    pass
