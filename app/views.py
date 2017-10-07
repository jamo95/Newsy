from newspaper import Article
from flask import render_template, request, jsonify

from .forms import SummaryForm

from app import app, db, dao
from app.textrank.sentences import rank as rank_sentences
from app.textrank.node import Node
from app.textrank.helpers import tokenize_sentences
from app.loaders import techcrunch, cricketau


DEFAULT_SENTENCE_COUNT = 4


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/review', methods=['POST'])
def review():
    review = request.get_json()

    if not review:
        return jsonify({
            'success': False, 'error': 'Missing json structure'
        }), 400

    if not ('url' in review and 'text' in review and 'review' in review):
        return jsonify({
            'success': False, 'error': 'Missing URL or TEXT or REVIEW'
        }), 400

    dao.review.insert(db.session, dao.review.Review(
        review['review'] == 'positive',
        review['text'],
        review['title'],
        review['url'],
        review['sentences']
    ))

    return jsonify({'success': True})


@app.route('/summarised', methods=['GET', 'POST'])
def summarised():
    form = SummaryForm()
    ctx = {
        'title': 'Summarizer',
        'form': form, 'form_error': '',
        'article_sentences': '', 'article_keywords': '', 'article_title': '',
    }

    if form.validate_on_submit() and form.is_text():
        summary = _summarize(
            form.text.data, form.title.data, form.url.data, form.count.data)

        ctx['article_title'] = summary.get('title')
        ctx['article_sentences'] = summary.get('sentences')
        ctx['article_url'] = form.url.data

    if request.method == 'POST':
        if form.errors:
            ctx['form_error'] = list(form.errors.values())[0][0]
        if not form.is_text():
            ctx['form_error'] = 'Must include either text or a URL.'

    return render_template('summarised.html', **ctx)


def _get_article_from_url(url):
    article = Article(url)

    article.download()
    article.parse()

    return article


def _summarize(text='', title='', url='', count=DEFAULT_SENTENCE_COUNT):
    url = url.rstrip('/')
    article_data = {'title': title, 'text': text, 'url': url}

    if url:
        article = _get_summary(url)
        if article:
            return {
                'title': article.title,
                'text': article.text,
                'sentences': [s.data for s in article.sentences][:count],
            }

        article = _get_article_from_url(url)
        article_data['text'] = article.text

        if 'techcrunch' in url:
            tc_article = techcrunch.ArticleLoader.load(url)
            article_data['title'] = tc_article['title']
        elif 'cricket' in url:
            ca_article = cricketau.ArticleLoader.load(url)
            article_data['title'] = ca_article['title']
            article_data['text'] = ca_article['content']
        else:
            article_data['title'] = article.title

    sentences = tokenize_sentences(article_data['text'])
    sentence_nodes = []
    for i, data in enumerate(sentences):
        sentence_nodes.append(Node(data, index=i))

    ranked_sentences = sorted(
        rank_sentences(sentence_nodes), key=lambda n: n.score, reverse=True)

    if url:
        _insert_summary(
            title=article_data['title'],
            text=article_data['text'],
            url=url,
            keywords=[],
            sentences=ranked_sentences
        )

    return {
        'title': article_data['title'],
        'text': article_data['text'],
        'sentences': [node.data for node in ranked_sentences][:count]
    }


def _get_summary(url):
    return db.session.query(dao.article.Article).filter(
        dao.article.Article.url == url).first()


def _insert_summary(title, url, text, sentences, keywords):
    dao.article.insert(db.session, text, title, url, keywords, sentences)
