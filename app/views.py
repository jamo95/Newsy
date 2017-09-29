from newspaper import Article
from flask import render_template, request

from app import app
from app.textrank.sentences import rank as rank_sentences
from app.textrank.node import Node
from app.textrank.helpers import tokenize_sentences


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarised', methods=['GET', 'POST'])
def summarised():
    ctx = {
        'title': 'Summariser', 'keywords': '', 'sentences': ''
    }

    # TODO: Sanitize URL.
    url = request.args.get('url', None)

    if url is not None:
        article = _get_article_from_url(url)
        ctx['title'] = article.title

        sentences = tokenize_sentences(article.text)
        sentence_nodes = sorted(
            rank_sentences([Node(s) for s in sentences]),
            key=lambda n: n.score, reverse=True
        )

        sorted_sentences = [node.data for node in sentence_nodes]
        ctx['sentences'] = sorted_sentences[:10]

    return render_template('summarised.html', **ctx)


def _get_article_from_url(url):
    article = Article(url)

    article.download()
    article.parse()

    return article
