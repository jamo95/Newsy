#!/usr/bin/env python

# Downloads files from the archive pages of supported sites.

import hashlib
import re
import requests
import sys

from bs4 import BeautifulSoup

from newspaper import Article

from nltk.stem.snowball import SnowballStemmer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import dao
from app.textrank.node import Node
from app.textrank.helpers import tokenize_sentences, normalize_url

config = {
    'db': {
        'host': 'ec2-13-55-222-175.ap-southeast-2.compute.amazonaws.com',
        # 'host': 'localhost',
        'name': 'newsydb',
        'user': 'postgres',
        'password': 'password'
    }
}


def db_connect():
    # Make connection to the DB.
    engine = create_engine(
        'postgres://{user}:{password}@{host}/{name}'.format(**config['db']))

    # Setup DB. It is most likely setup but this is just as a precaution.
    dao.Base.metadata.create_all(engine)

    return engine, sessionmaker(bind=engine)()


def dl_techcrunch(session, stemmer, year, month, day):
    base_url = 'https://techcrunch.com/'
    archive_url = '{}{}/{}/{}'.format(base_url, year, month, day)

    # Download links for the articles.
    response = requests.get(archive_url)
    if not 200 <= response.status_code < 300:
        print('techcrunch failed to download archive page: status {}'.format(
            response.status_code))
        return False

    html = BeautifulSoup(response.text, 'html.parser')
    post_titles = html.select('.post-title')

    article_urls = []
    for post_title in post_titles:
        url = post_title.select('a')[0].attrs['href']
        if url.replace('www.', '').startswith(base_url):
            article_urls.append(url)

    # Download, summarise and store articles.
    for url in article_urls:
        # Check if we already have the article in the DB.
        if _get_article(session, normalize_url(url)):
            print('~ {}'.format(normalize_url(url)))
            continue

        # Download the article content.
        article = _download_article(url)
        article.nlp()   # Use for now until summaries and loaders are better.

        # Normalise and hash all the sentences to make finding the index more
        # accurate.
        text_sentences = [
            _hash_text(s) for s in tokenize_sentences(article.text)]

        # Conform data for entry into DB.
        summary_sentences = []
        keywords = [Node(w) for w in article.keywords]

        for sentence in article.summary.split('\n'):
            index = text_sentences.index(_hash_text(sentence))
            summary_sentences.append(Node(sentence, index=index))

        # Insert article and summary into DB.
        dao.article.insert(
            session=session,
            text=article.text,
            url=normalize_url(url),
            title=article.title,
            keywords=keywords,
            sentences=summary_sentences
        )
        print('+ {}'.format(url))
    return True


def dl_venturebeat(session, stemmer, year, month, day):
    base_url = 'https://venturebeat.com/'
    archive_url = '{}{}/{}/{}'.format(base_url, year, month, day)

    # Download links for the articles.
    response = requests.get(archive_url)
    if not 200 <= response.status_code < 300:
        print('venturebeat failed to download archive page: status {}'.format(
            response.status_code))
        return False

    html = BeautifulSoup(response.text, 'html.parser')
    post_titles = html.select('.article-title')

    article_urls = []
    for post_title in post_titles:
        url = post_title.select('a')[0].attrs['href']
        if url.replace('www.', '').startswith(base_url):
            article_urls.append(url)

    # Download, summarise and store articles.
    for url in article_urls:
        # Check if we already have the article in the DB.
        if _get_article(session, normalize_url(url)):
            print('~ {}'.format(normalize_url(url)))
            continue

        # Download the article content.
        article = _download_article(url)
        article.nlp()   # Use for now until summaries and loaders are better.

        # Normalise and hash all the sentences to make finding the index more
        # accurate.
        text_sentences = [
            _hash_text(s) for s in tokenize_sentences(article.text)]

        # Conform data for entry into DB.
        summary_sentences = []
        keywords = [Node(w) for w in article.keywords]

        for sentence in article.summary.split('\n'):
            index = text_sentences.index(_hash_text(sentence))
            summary_sentences.append(Node(sentence, index=index))

        # Insert article and summary into DB.
        dao.article.insert(
            session=session,
            text=article.text,
            url=normalize_url(url),
            title=article.title,
            keywords=keywords,
            sentences=summary_sentences
        )
        print('+ {}'.format(url))
    return True


def dl_wired(session, stemmer, year, month, day):
    base_url = 'https://wired.com/'
    archive_url = '{}{}/{}/{}'.format(base_url, year, month, day)

    # Download links for the articles.
    response = requests.get(archive_url)
    if not 200 <= response.status_code < 300:
        print('wired failed to download archive page: status {}'.format(
            response.status_code))
        return False

    html = BeautifulSoup(response.text, 'html.parser')
    post_title_list = html.select('ul.no-marg.border-micro')

    article_urls = []
    if post_title_list:
        for anchor in post_title_list[0].select('a.clearfix.pad'):
            url = anchor.attrs['href']
            if url.replace('www.', '').startswith(base_url):
                article_urls.append(url)

    # Download, summarise and store articles.
    for url in article_urls:
        # Check if we already have the article in the DB.
        if _get_article(session, normalize_url(url)):
            print('~ {}'.format(normalize_url(url)))
            continue

        # Download the article content.
        article = _download_article(url)
        article.nlp()   # Use for now until summaries and loaders are better.

        # Normalise and hash all the sentences to make finding the index more
        # accurate.
        text_sentences = [
            _hash_text(s) for s in tokenize_sentences(article.text)]

        # Conform data for entry into DB.
        summary_sentences = []
        keywords = [Node(w) for w in article.keywords]

        for sentence in article.summary.split('\n'):
            index = text_sentences.index(_hash_text(sentence))
            summary_sentences.append(Node(sentence, index=index))

        # Insert article and summary into DB.
        dao.article.insert(
            session=session,
            text=article.text,
            url=normalize_url(url),
            title=article.title,
            keywords=keywords,
            sentences=summary_sentences
        )
        print('+ {}'.format(url))
    return True


def dl_newscomau(session, stemmer, year, month, day):
    base_url = 'http://www.news.com.au/'
    archive_url = '{}{}/{}/{}'.format(base_url, year, month, day)

    # Download links for the articles.
    response = requests.get(archive_url)
    if not 200 <= response.status_code < 300:
        print('news.com.au failed to download archive page: status {}'.format(
            response.status_code))
        return False

    html = BeautifulSoup(response.text, 'html.parser')
    post_title_list = html.select('div.module-content')

    article_urls = []
    if post_title_list:
        for post_title in post_title_list:
            for heading in post_title.select('h4.heading'):
                url = heading.select('a')[0].attrs['href']
                if url.startswith(base_url):
                    article_urls.append(url)

    # Download, summarise and store articles.
    for url in article_urls:
        # Check if we already have the article in the DB.
        if _get_article(session, normalize_url(url)):
            print('~ {}'.format(normalize_url(url)))
            continue

        # Download the article content.
        article = _download_article(url)
        article.nlp()   # Use for now until summaries and loaders are better.

        # Normalise and hash all the sentences to make finding the index more
        # accurate.
        text_sentences = [
            _hash_text(s) for s in tokenize_sentences(article.text)]

        # Conform data for entry into DB.
        summary_sentences = []
        keywords = [Node(w) for w in article.keywords]

        for sentence in article.summary.split('\n'):
            index = text_sentences.index(_hash_text(sentence))
            summary_sentences.append(Node(sentence, index=index))

        # Insert article and summary into DB.
        dao.article.insert(
            session=session,
            text=article.text,
            url=normalize_url(url),
            title=article.title,
            keywords=keywords,
            sentences=summary_sentences
        )
        print('+ {}'.format(url))
    return True


def _hash_text(text):
    text = re.sub(r'\W+', '', text)
    text = text.lower()

    text = text.encode('utf-8')
    return hashlib.md5(text).hexdigest()


def _download_article(url):
    article = Article(url)

    article.download()
    article.parse()

    return article


def _get_article(session, url):
    return session.query(dao.article.Article).filter(
        dao.article.Article.url == url).first()


if __name__ == '__main__':
    '''The best way to run this script is:
            $ python dl.py `date +"%Y %m %d"`
    '''

    print('starting dl.py with args: {}'.format(' '.join(sys.argv[1:])))

    year, month, day = sys.argv[1:]
    archives = {
        # 'techcrunch': dl_techcrunch,
        # 'venturebeat': dl_venturebeat,
        # 'wired': dl_wired,
        'news.com.au': dl_newscomau,
    }

    stemmer = SnowballStemmer('english')
    print('setup snowball english stemmer')

    db_engine, db_session = db_connect()
    print('connected to database at {}'.format(config['db']['host']))

    for name, download in archives.items():
        print('----- {}'.format(name))
        result = download(db_session, stemmer, year, month, day)
        print('----- {} {}'.format(name, 'pass' if result else 'fail'))
