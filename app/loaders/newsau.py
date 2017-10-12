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

    title = html.find('h1', {'class': 'story-headline'})

    return clean_html(str(title))


def _get_content(html):
    articleDescription = html.find('p', {'class' : 'description'})
    articleDescription = clean_html(str(articleDescription))

    articleContent = html.find('div',{'class' : 'story-content'})
    articleContent = clean_html(str(articleContent))

    return articleDescription + articleContent

def _get_date(html):
    date = html.find('span', {'class': 'datestamp'})
    date = str(date)

    date = re.sub(r'<span.*?>',' ', date)
    date = re.sub(r'</span>', '',date)
    return date.strip()
