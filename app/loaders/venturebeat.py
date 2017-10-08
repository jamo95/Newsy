import requests
import re

from bs4 import BeautifulSoup

from app.loaders.helpers import clean_html

BASE_URL = 'https://venturebeat.com'


class ArticleLoader:
    @staticmethod
    def load(url):
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'lxml')

        return {
            'content': _get_content(html),
            'title': _get_title(html),
            'date': _get_date(html),
            'url': url,
        }


def _get_title(html):
    title = html.findAll('h1', {'class': 'article-title'})
    return clean_html(str(title))


def _get_content(html):
    articleText = html.findAll('div', {'class': 'article-content'})
    articleText = str(articleText)

    articleSoup = BeautifulSoup(articleText, 'lxml')
    articleSoup = articleSoup.findAll('p')

    raw_content_str = map(str, articleSoup)

    return clean_html(' '.join(raw_content_str))


def _get_date(html):
    date = html.findAll('time', {'class': 'the-time'})
    return clean_html(str(date))
