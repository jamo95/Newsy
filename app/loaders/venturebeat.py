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
    title = html.find('h1', {'class': 'article-title'})
    title = clean_html(str(title))

    return title


def _get_content(html):
    articleText = html.find('div', {'class': 'article-content'})
    articleText = str(articleText)

    articleSoup = BeautifulSoup(articleText, 'lxml')
    articleSoup = articleSoup.findAll('p')
    #print(str(articleSoup))
    raw_content_str = map(str, articleSoup)

    finalReturn = clean_html(' '.join(raw_content_str))

    return finalReturn


def _get_date(html):
    date = html.find('time', {'class': 'the-time'})
    date = clean_html(str(date))
    return date
