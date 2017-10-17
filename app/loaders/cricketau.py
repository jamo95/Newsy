import requests
import re
import datetime
from bs4 import BeautifulSoup

from helpers import clean_html

BASE_URL = 'http://www.cricket.com.au'


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
    title = str(html.select('title')[0].contents[0])
    title = re.sub(r'\|.*$', '', title)
    return title


def _get_content(html):
    articleText = html.find('div', {'class': 'article-text-update'})

    if not articleText:
        articleText = html.find('div',{'class': 'article-text text-merri'})

    articleText = str(articleText)

    articleSoup = BeautifulSoup(articleText, 'lxml')
    articleSoup = articleSoup.findAll('p')

    raw_content_str = map(str, articleSoup)

    return clean_html(' '.join(raw_content_str))


def _get_date(html):
    # Finds the author and posted date class.
    authorName = html.findAll('p', {'class': 'author-name'})
    timestamp_resultset = str(authorName)

    # Converts to BS object to find span class where posted.
    # Date is present.
    tS = BeautifulSoup(timestamp_resultset, 'lxml')
    tS = tS.find_all('span')

    # Maps and converts to raw string data.
    raw_content_str = map(str, tS)
    date = clean_html(' '.join(raw_content_str))
    if not date:
        date = html.find('div', {'class': 'publishDate'})
        date = clean_html(' '.join(date))
    date = datetime.datetime.strptime(date, "%d %B %Y").strftime("%d/%m/%Y")
    return date
