from flask import render_template

from app import app

# Other things
from flask import flash,request
from .forms import ArticleForm
from newspaper import Article


@app.route('/', methods=['GET', 'POST'])
def index():
    article_text = "no article loaded"

    form = ArticleForm()
    #print(form.article.data)
    #print(request.args.get('url', None))
    if form.validate_on_submit():
        url = form.article.data
        article = Article(url)
        article.download()
        article.parse()
        article_text = article.text

    return render_template('index.html',
                            title='Summariser',
                            article=article_text,
                            form=form)

    
