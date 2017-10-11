import math

from newspaper import Article
from flask import render_template, request, jsonify
from sqlalchemy import desc

from .forms import SummaryForm

from app import app, db, dao
from app.textrank.sentences import rank as rank_sentences
from app.textrank.node import Node
from app.textrank.helpers import tokenize_sentences, normalize_url
from app.loaders import techcrunch, cricketau
import operator

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


@app.route('/sites', methods=['GET'])
@app.route('/sites/<string:site>', methods=['GET'])
@app.route('/sites/<string:site>/<int:page>', methods=['GET'])
def sites(site=None, page=1):
    page_size = 20
    ctx = {
        'title': 'Sites', 'site': None, 'sites': _get_urls(), 'page': page
    }

    if site and site in ctx['sites']:
        dl_articles, dl_articles_count = _get_articles(
            url_prefix=site, offset=page * page_size, limit=page_size)
        ctx['max_page'] = math.ceil(dl_articles_count / page_size)

        articles = {}   # Key = Published date.
        for article in dl_articles:
            if not article.published_at:
                continue
            if article.published_at not in articles:
                articles[article.published_at] = []
            articles[article.published_at].append(article)

        ctx['site'] = site
        ctx['articles'] = articles

    return render_template('sites.html', **ctx)

@app.route('/feed', methods=['GET'])
@app.route('/feed/<string:category>', methods=['GET'])
def feed(category=None):
    ctx={'title': 'Categorized Feed','category':None}
    if category:
        feed_articles = _get_articles_category(category)
    else:
        feed_articles = _get_all_articles()
    articles = {}
    keywords_dict = {}	#keywords -> repetition count
    for article in feed_articles:
        if article.published_at not in articles:
            articles[article.published_at] = []
        articles[article.published_at].append(article)
        #repetition count
        for keyword in article.keywords:
            kw = keyword.data
            if kw in keywords_dict:
                keywords_dict[kw] += 1
            else:
                keywords_dict[kw] = 1
    #get top 10 keywords
    keywords = sorted(keywords_dict, key=keywords_dict.__getitem__, reverse=True)
    keywords = keywords[0:9]
    ctx['articles'] = articles
    ctx['keywords'] = keywords

    return render_template('feed.html', **ctx)

@app.route('/summarised', methods=['GET', 'POST'])
def summarised():
    form = SummaryForm()
    ctx = {
        'title': 'Summarizer',
        'form': form, 'form_error': '',
        'article_sentences': '', 'article_keywords': '', 'article_title': '',
    }

    url = request.args.get('url')
    if form.validate_on_submit() and form.is_text() or url:
        if url:
            if not url.startswith('http'):
                url = 'http://' + url
            form.url.data = url

        summary = _summarize(
            form.text.data, form.title.data, form.url.data, form.count.data)

        ctx['article_title'] = summary.get('title')
        ctx['article_sentences'] = summary.get('sentences')
        ctx['article_keywords'] = summary.get('keywords')
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
    article.nlp()

    return article


def _summarize(text='', title='', url='', count=DEFAULT_SENTENCE_COUNT):
    article_data = {'title': title, 'text': text, 'url': url}

    if url:
        article = _get_summary(normalize_url(url))
        if article:
            return {
                'title': article.title,
                'text': article.text,
                'sentences': [s.data for s in article.sentences][:count],
                'keywords': [w.data for w in article.keywords],
            }

        article = _get_article_from_url(url)
        article_data['text'] = article.text

        if 'techcrunch' in url:
            tc_article = techcrunch.ArticleLoader.load(url)
            article_data['title'] = tc_article['title']
            article_data['published_at'] = tc_article['timestamp']
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

    #TODO Richard
    """
    Add own function for keyword extraction
    """
    keywords = [Node(w) for w in article.keywords]
    ranked_sentences = sorted(
        rank_sentences(sentence_nodes), key=lambda n: n.score, reverse=True)

    if url:
        _insert_summary(
            title=article_data['title'],
            text=article_data['text'],
            url=normalize_url(url),
            keywords=keywords,
            sentences=ranked_sentences,
            published_at=article_data.get('published_at')
        )

    return {
        'title': article_data['title'],
        'text': article_data['text'],
        'sentences': [node.data for node in ranked_sentences][:count],
        'keywords': [node.data for node in keywords]
    }


def _get_summary(url):
    return db.session.query(dao.article.Article).filter(
        dao.article.Article.url == url).first()


def _get_urls():
    all_urls = db.session.query(dao.article.Article).with_entities(
        dao.article.Article.url).distinct().all()

    distinct_urls = []
    for url in all_urls:
        base_url = url[0].split('/')[0]
        if base_url not in distinct_urls:
            distinct_urls.append(base_url)

    return distinct_urls


def _get_articles(url_prefix, offset=0, limit=20):
    articles = db.session.query(dao.article.Article).filter(
        dao.article.Article.url.like('{}%'.format(url_prefix))
    ).order_by(
        desc(dao.article.Article.published_at)
    ).offset(offset).limit(limit).all()

    articles_count = db.session.query(dao.article.Article).filter(
        dao.article.Article.url.like('{}%'.format(url_prefix))).count()

    return articles, articles_count

def _get_all_articles():
    return db.session.query(dao.article.Article).filter(
        dao.article.Article.url.like('{}%'.format("news.com.au"))
    ).order_by(
        desc(dao.article.Article.published_at)
    ).all()

def _get_articles_category(category):
    all_articles = db.session.query(dao.article.Article).filter(
        dao.article.Article.url.like('{}%'.format("news.com.au"))
    ).order_by(
        desc(dao.article.Article.published_at)
    ).all()

    categorized_articles = []    
    for article in all_articles:
        for keyword in article.keywords:
            if keyword.data == category:
                categorized_articles.append(article)
                break

    return categorized_articles

def _insert_summary(title, url, text, sentences, keywords, published_at=None):
    dao.article.insert(
        db.session, text, title, url, keywords, sentences, published_at)
