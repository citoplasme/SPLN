from flask import Flask, escape, request, render_template, url_for
from tfidf import search, get_review_from_id
import json

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def get_movie():
	termos = request.form['termos']
	termos = termos.split()

	reviews = search(termos)
	#return str(json.dumps(reviews, indent = 4, ensure_ascii = False))
	return render_template('results.html', reviews = reviews)

@app.route('/<id>')
def avaliacao(id):
	review = get_review_from_id(id)
	#return str(json.dumps(review, indent = 4, ensure_ascii = False))
	return render_template('review.html', review = review)

