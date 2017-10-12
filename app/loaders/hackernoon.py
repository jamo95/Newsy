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

    title = html.find('h1', {'class': 'graf graf--h3 graf--leading graf--title'})

    #looks messy but hackernoon sucks
    title = re.sub(r'<h(\d).*?>', '', str(title))
    title = re.sub(r'<stron.*?>', '', title)
    title = re.sub(r'</strong>', '', title)
    title = re.sub(r'</h(\d).*?>', '', title)


    return title


def _get_content(html):
    articleText = html.findAll('div', {'class' : 'section-content'})
    cleanText = clean_html(' '.join(map(str,articleText)))
    return cleanText

def _get_date(html):
    date = html.find('time')
    return clean_html(str(date))
