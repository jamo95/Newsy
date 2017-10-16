import math
import sys, re
from newspaper import Article
from flask import render_template, request, jsonify, redirect
from sqlalchemy import desc

from .forms import SummaryForm

from app import app, db, dao
from app.textrank.sentences import rank as rank_sentences
from app.textrank.keywords import rank_words
from app.textrank.node import Node
from app.textrank.helpers import tokenize_sentences, tokenize_words, normalize_url
from app.loaders import techcrunch, wired, hackernoon, venturebeat, newsau
from app import sentiment

from app.dao.keyword import Keyword

DEFAULT_SENTENCE_COUNT = 4
DEFAULT_KEYWORD_COUNT = 20


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
        ctx['max_page'] = math.ceil(dl_articles_count / page_size) - 1

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


@app.route('/feed', methods=['GET', 'POST'])
@app.route('/feed/<string:category>', methods=['GET'])
@app.route('/feed/<string:category>/<int:page>', methods=['GET'])
def feed(category=None, page=1):
    page_size = 20
    ctx = {'title': 'Categorized Feed', 'category': None, 'page': page}

    if not category:
        category = request.values.get('category')
        if category:
            return redirect('/feed/{}'.format(category))
        #Put all keywords in a dictionary as key and number of times repeated as value
        '''all_articles = _get_all_articles()
        keywords_dict = {}	#keywords -> repetition count
        for article in all_articles:
            #repetition count
            for keyword in article.keywords:
                kw = keyword.data
                if kw in keywords_dict:
                    keywords_dict[kw] += 1
                else:
                    keywords_dict[kw] = 1
        #get top 10 keywords
        keywords = sorted(keywords_dict, key=keywords_dict.__getitem__, reverse=True)
        ctx['categories'] = keywords'''

        #I manually compile this list based on most popular keywords
        ctx['categories'] = ['google','technology','ai','car','security','facebook','amazon','startup','racing','software']

    if category:
        feed_articles, feed_articles_count = _get_articles_category(
            category=category, offset=page * page_size, limit=page_size)
        ctx['max_page'] = math.ceil(feed_articles_count / page_size) - 1

        articles = {}   # Key = Published date.
        for article in feed_articles:
            if not article.published_at:
                continue
            if article.published_at not in articles:
                articles[article.published_at] = []
            articles[article.published_at].append(article)

        ctx['category'] = category
        ctx['articles'] = articles

    return render_template('feed.html', **ctx)


@app.route('/summarised', methods=['GET', 'POST'])
def summarised():
    form = SummaryForm()
    ctx = {
        'title': 'Summarizer',
        'form': form, 'form_error': '',
        'article_sentences': '', 'article_keywords': '', 'article_title': '',
        'article_analysis': ''
    }

    url = request.args.get('url')
    suggestedKeywords=None
    if request.values.get('keywords') is not None:
        suggestedKeywords = request.values.get('keywords').split(" ")

    if form.validate_on_submit() and form.is_text() or url:
        if url:
            if not url.startswith('http'):
                url = 'http://' + url
            form.url.data = url
        summary = _summarize(
            form.text.data, form.title.data, form.url.data, form.count.data, suggestedKeywords)

        ctx['article_title'] = summary.get('title')
        ctx['article_sentences'] = summary.get('sentences')
        ctx['article_keywords'] = summary.get('keywords')
        ctx['article_analysis'] = summary.get('s_analysis')
        ctx['article_url'] = form.url.data
        if url:
            url = re.sub("http://", "", url)
            reviews = get_reviews(form.text.data, form.title.data, url, form.count.data)
        else:
            reviews = get_reviews(form.text.data, form.title.data, form.url.data, form.count.data)
        ctx['good_review'] = reviews[0]
        ctx['bad_review'] = reviews[1]

    if request.method == 'POST':
        if form.errors:
            ctx['form_error'] = list(form.errors.values())[0][0]
        if not form.is_text():
            ctx['form_error'] = 'Must include either text or a URL.'

    return render_template('summarised.html', **ctx)

def get_reviews(text, title, url, count):
    reviews = [0]*2
    total = db.session.query(dao.review.Review).all()
    if url :
        for review in total:
            if review.url == url and review.count == count:
                if review.status:
                    reviews[0] += 1
                else :
                    reviews[1] += 1
    else :
        for review in total:
            if review.title == title and review.text == text and review.count == count:
                if review.status:
                    reviews[0] += 1
                else :
                    reviews[1] += 1
    return reviews

def _get_article_from_url(url):
    article = Article(url)

    # TODO Need to throw exception in case article is not downloadable
    # Otherwise user is returned the exception page
    article.download()
    article.parse()
    article.nlp()

    return article


def _summarize(text='', title='', url='',
        sentence_count=DEFAULT_SENTENCE_COUNT,
        suggestedKeywords=None,
        keyword_count=DEFAULT_KEYWORD_COUNT):

    article_data = {'title': title, 'text': text, 'url': url}

    if url:
        # Check if article is cached
        article = _get_summary(normalize_url(url))
        if article:
            if suggestedKeywords is not None:
                for word in suggestedKeywords:
                    newKeyword = Keyword(word, 1)
                    article.keywords.insert(0,newKeyword)
                db.session.add(article)
                db.session.commit()

            if article.s_analysis is None:
                senti_analysis_data = sentiment.SentimentAnalysis.analyise(article.text)
                if senti_analysis_data is not None:
                    article.s_analysis = senti_analysis_data['label']
            return {
                'title': article.title,
                'text': article.text,
                'sentences': [s.data for s in article.sentences][:sentence_count],
                'keywords': [w.data for w in article.keywords][:keyword_count],
                's_analysis': article.s_analysis,
            }

        article = _get_article_from_url(url)
        article_data['text'] = article.text
        # elif 'cricket' in url:
        #     ca_article = cricketau.ArticleLoader.load(url)
        #     article_data['title'] = ca_article['title']
        #     article_data['text'] = ca_article['content']
        #     print(ca_article['content'])
        #     article_data['published_at'] = ca_article['date']
        #    senti_analysis_data = sentiment.SentimentAnalysis.analyise(ca_article['content'])
        #    if senti_analysis_data is not None:
        #        article_data['s_analysis'] = senti_analysis_data['label']
        if 'techcrunch' in url:
            tc_article = techcrunch.ArticleLoader.load(url)
            article_data['title'] = tc_article['title']
            article_data['text'] = tc_article['content']
            article_data['published_at'] = tc_article['timestamp']
            senti_analysis_data = sentiment.SentimentAnalysis.analyise(tc_article['content'])
            print(senti_analysis_data)
            if senti_analysis_data is not None:
                article_data['s_analysis'] = senti_analysis_data['label']
        elif 'wired' in url:
            wired_article = wired.ArticleLoader.load(url)
            article_data['title'] = wired_article['title']
            article_data['text'] = wired_article['content']
            article_data['published_at'] = wired_article['date']
            senti_analysis_data = sentiment.SentimentAnalysis.analyise(wired_article['content'])
            if senti_analysis_data is not None:
                article_data['s_analysis'] = senti_analysis_data['label']
        elif 'hackernoon' in url:
            hackernoon_article = hackernoon.ArticleLoader.load(url)
            article_data['title'] = hackernoon_article['title']
            article_data['text'] = hackernoon_article['content']
            article_data['published_at'] = hackernoon_article['date']
            senti_analysis_data = sentiment.SentimentAnalysis.analyise(hackernoon_article['content'])
            if senti_analysis_data is not None:
                article_data['s_analysis'] = senti_analysis_data['label']
        elif 'venturebeat' in url:
            venturebeat_article = venturebeat.ArticleLoader.load(url)
            article_data['title'] = venturebeat_article['title']
            article_data['text'] = venturebeat_article['content']
            article_data['published_at'] = venturebeat_article['date']
            senti_analysis_data = sentiment.SentimentAnalysis.analyise(venturebeat_article['content'])
            if senti_analysis_data is not None:
                article_data['s_analysis'] = senti_analysis_data['label']
        elif 'news.com.au' in url:
            newsau_article = newsau.ArticleLoader.load(url)
            article_data['title'] = newsau_article['title']
            article_data['text'] = newsau_article['content']
            article_data['published_at'] = newsau_article['date']
            senti_analysis_data = sentiment.SentimentAnalysis.analyise(newsau_article['content'])
            if senti_analysis_data is not None:
                article_data['s_analysis'] = senti_analysis_data['label']
        else:
            article_data['title'] = article.title
            senti_analysis_data = sentiment.SentimentAnalysis.analyise(article.text)
            if senti_analysis_data is not None:
                article_data['s_analysis'] = senti_analysis_data['label']
    else:
        article_data['title'] = title
        senti_analysis_data = sentiment.SentimentAnalysis.analyise(text)
        if senti_analysis_data is not None:
            article_data['s_analysis'] = senti_analysis_data['label']

    sentence_nodes = []
    sentences = tokenize_sentences(article_data['text'])
    for i, data in enumerate(sentences):
        sentence_nodes.append(Node(data, index=i))

    ranked_sentences = sorted(
        rank_sentences(sentence_nodes), key=lambda n: n.score, reverse=True)

    words = tokenize_words(article_data['text'])
    keywords = sorted(
            rank_words(words), key=lambda n: n.score, reverse=True)

    if suggestedKeywords is not None:
        for word in suggestedKeywords:
            newKeyword = Keyword(word, 1)
            keywords.insert(0,newKeyword)
    if url:
        _insert_summary(
            title=article_data['title'],
            text=article_data['text'],
            url=normalize_url(url),
            keywords=keywords,
            sentences=ranked_sentences,
            published_at=article_data.get('published_at'),
            s_analysis=article_data['s_analysis']
        )

    return {
        'title': article_data['title'],
        'text': article_data['text'],
        'sentences': [node.data for node in ranked_sentences][:sentence_count],
        'keywords': [node.data for node in keywords][:keyword_count],
        's_analysis': article_data['s_analysis']
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


def _get_articles_category(category, offset=0, limit=20):
    categorized_articles = db.session.query(dao.article.Article).filter(
        dao.article.Article.keywords.any(Keyword.data.like(category))
    ).order_by(
        desc(dao.article.Article.published_at)
    ).offset(offset).limit(limit).all()

    categorized_articles_count = db.session.query(dao.article.Article).filter(
        dao.article.Article.keywords.any(Keyword.data.like(category))
    ).count()

    return categorized_articles, categorized_articles_count

def _get_all_articles():

    return db.session.query(dao.article.Article).all()

def _insert_summary(title, url, text, sentences, keywords, s_analysis, published_at=None):
    dao.article.insert(
        db.session, text, title, url, keywords, sentences, s_analysis, published_at)
