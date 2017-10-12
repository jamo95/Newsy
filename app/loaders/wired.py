import requests
import re

from bs4 import BeautifulSoup

from app.loaders.helpers import clean_html

BASE_URL = 'https://www.wired.com/'


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
    title = html.find('h1', {'class': 'title'})
    return clean_html(str(title))


def _get_content(html):
    articleText = html.find('article')
    articleText = str(articleText)

    articleSoup = BeautifulSoup(articleText, 'lxml')
    articleSoup = articleSoup.find('div')
    articleSoup = articleSoup.findAll('p')

    raw_content_str = map(str, articleSoup)

    return clean_html(' '.join(raw_content_str))


def _get_date(html):
    date = html.find('time', {'class': 'date-mdy'})
    #format is mm.dd.yy
    dates = str(date).split('.')
    #reformat
    month = dates[0]
    day = dates[1]
    year = "20"+dates[2]
    publish_date = year+"-"+month+"-"+day
    return clean_html(str(publish_date))
