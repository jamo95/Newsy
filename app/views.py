from flask import render_template

from app import app

# Other things
from flask import request
from newspaper import Article
import nltk


@app.route('/', methods=['GET', 'POST'])
def index():
    article_title = ""
    article_summary = ""
    article_original = ""

    #FIXME sanitize url
    url = request.args.get('url', None)
    if url != None:
        article = Article(url)
        article.download()
        article.parse()
        article_title = article.title
        article_text = article.text
        # Comment out if you have not installed nlpt
        article.nlp()
        article_summary = article.summary





    return render_template('index.html',
                            title='Summariser',
                            article_title=article_title,
                            article_summary=article_summary,
                            article_original=article_text)

    
