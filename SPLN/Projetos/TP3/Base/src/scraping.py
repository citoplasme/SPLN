from bs4 import BeautifulSoup
import requests
import sys
import json

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pathlib

DRIVER_BIN = str(pathlib.Path().absolute()) + '/chromedriver'

# Retorna o HTML de uma página com base no URL que recebe
def get_page(url):
	html = requests.get(url).content
	return html

# Gera um array de objetos com os pontos de entrada para as reviews escritas
def get_reviews(html):
	soup = BeautifulSoup(html, 'html.parser')
	pages = soup.find_all('section', 'broll wrap')
	print(len(pages))
	response = []
	for page in pages:
		reviews = page.find('div', 'tbl').find_all('article', 'article REVIEW')
		for review in reviews:
			t = review.find('div', 't')
			m = review.find('div', 'm')
			image = t.find('a', 'thumb score-wrapper').find('img', 'thumb').attrs['src']
			link = t.find('a', 'thumb score-wrapper').attrs['href']
			score = t.find('a', 'thumb score-wrapper').find('figure').find('div').find('span').find('span').get_text()
			date = m.find('div', 'info').find('time').attrs['datetime']
			title = m.find('h3').get_text().replace(' - Análise', '')
			synopsis = m.find('p').get_text()  

			response.append({
				'image' : image,
				'link' : link,
				'score' : score,
				'date' : date, 
				'title' : title,
				'synopsis' : synopsis
				})
	return response
	
# Função para imprimir o output para o ecrã			 
def print_output(obj, out_format = None):
	if out_format == 'json':
		print(json.dumps(obj, indent = 4, ensure_ascii = False))
	else:
		print(obj)

# Permite dar scroll automático à página (existência de infinite scrolling)
def scroll_page(url):
	driver = webdriver.Chrome(executable_path = DRIVER_BIN)
	driver.get(url)
	elem = driver.find_element_by_tag_name('body')
	limit = 250
	while limit:
		try:
			elem.send_keys(Keys.PAGE_DOWN)
			time.sleep(0.2)
			limit -= 1
		except:
			break

	return get_reviews(driver.page_source)

# Adiciona o campo de texto ao objeto com a review associada ao URL
def add_text(json):
	for obj in json:
		obj['subtitle'] = get_review_subtitle(obj['link'])
		obj['text'] = get_review_text(obj['link'])
		print('DONE:', obj['title'])
	return json

# Obtenção do texto da review. Podem existir mais páginas, daí a necessidade de uma flag para não entrar em loop
def get_review(html, main = True):
	soup = BeautifulSoup(html, 'html.parser')
	subtitle = soup.find('div','article-sub-headline').find('h3', id = 'id_deck').get_text()
	
	pages = soup.find('section', 'side-by-side article-content')
	article = pages.find('article', 'article-section article-page').find('div', id = 'id_text').get_text()
	paginator = []
	# Caso existam mais páginas
	try:
		paginator = soup.find('div', 'paginator').find_all('a')
	except:
		pass
	# Para não duplicar texto
	hrefs = set()
	# Article são os 2 primeiros paragrafos da review
	txt = article
	# Resto da review
	for p in soup.find_all('p'):
		para = p.get_text()
		# Continua é a indicação que há mais texto numa outra página
		if para.lower() != 'continua...':
			txt += para
	# calcular texto das restantes páginas
	for pagin in paginator:
		try:
			hrefs.add(pagin.attrs['href'])
		except KeyError:
			pass	
	# Armazenar texto das restantes páginas
	if main == True:
		for link in hrefs:
			txt += get_review_text(link, False)
	return txt

# Devolve o subtitulo asscciado à review
def get_review_subtitle(url):
	html = get_page(url)
	soup = BeautifulSoup(html, 'html.parser')
	subtitle = soup.find('div','article-sub-headline').find('h3', id = 'id_deck').get_text()
	return subtitle

# Função para procurar o texto de uma review
def get_review_text(url, main = True):
	html = get_page(url)
	return get_review(html, main)

# Função para armazenar um array de objetos json em ficheiro
def save_to_file(data, name):
	f = open(name, "w")
	dados = json.dumps(data, indent = 4, ensure_ascii = False)
	f.write(dados)
	f.close()
	print("File saved.")

# Função para leitura de objetos json para cache
def get_from_file():
	with open('reviews.json') as json_file:
		data = json.load(json_file)
	return data

base_url = 'https://pt.ign.com/article/review'

def main():
	# Get the reviews without its textual content
	#revs = scroll_page(base_url)
	#save_to_file(revs, "dados/reviews.json")
	#print(len(revs))

	#Get the textual content of the reviews
	reviews = get_from_file()
	updated = add_text(reviews)
	save_to_file(updated, "dados/reviews_full.json")
	#print_output(updated, 'json')
	#print(get_review_text('https://pt.ign.com/man-eater/87513/review/maneater-analise'))
	#print(get_review_text('https://pt.ign.com/luigis-mansion-3/81362/review/luigis-mansion-3-analise'))

	
if __name__ == '__main__':
	main()
