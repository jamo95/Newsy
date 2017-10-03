import dateutil.parser
import requests
import re

from bs4 import BeautifulSoup
from datetime import datetime

from helpers import clean_html

BASE_URL = 'www.cricket.com.au'

class ArchiveLoader:
    @staticmethod
    def load(year, month, day):
        date_path = '{}/{:02d}/{:02d}'.format(year, month, day)
        archive_url = BASE_URL + date_path

        return {
            'timestamp': datetime.strptime(date_path, '%Y/%m/%d'),
            'articles': _get_articles(archive_url)
        }

def _get_articles(url):
        response = requests.get(url)
        if not 200 <= response.status_code < 300:
            return []

        html = BeautifulSoup(response.text, 'html.parser')
        post_titles = html.select('.post-title')

        article_links = []
        for post_title in post_titles:
            link = post_title.select('a')[0].attrs['href']
            if link.replace('www.', '').startswith(BASE_URL):
                article_links.append(link)

        return article_links


class ArticleLoader:
    @staticmethod
    def load(url):
        response = requests.get(url)


        html = BeautifulSoup(response.text, 'lxml')

        return {
            'content': _get_content(html),
            'title': _get_title(html),
            'date': _get_date(html),
            #'tags': _get_tags(html),
            'url': url,
        }

def _get_title(html):
    title = str(html.select('title')[0].contents[0])
    title = re.sub(r'\|.*$','',title)
<<<<<<< HEAD

=======
>>>>>>> cricketau
    return title


def _get_content(html):
    string = html.findAll("div", { "class" : "article-text-update" })
    raw_content_str = map(str,string)
    return clean_html(' '.join(raw_content_str))


def _get_date(html):
    #finds the author and posted date class
    authorName = html.findAll("p", { "class" : "author-name" })
    timestamp_resultset = str(authorName)
    #converts to BS object to find span class where posted
    #date is present
    tS = BeautifulSoup(timestamp_resultset, "lxml")
    tS = tS.find_all("span")
    #maps and converts to raw string data
    raw_content_str = map(str,tS)
    date = clean_html(' '.join(raw_content_str))

    return date


def _get_tags(html):
    tags = []

    for item in html.select('div.acc-handle'):
        text = item.select('a')[0].text

        for tag in text.split(' '):
            tag = tag.replace('\t', '').replace('\n', '').strip()

            # Ignore if there is any upper case.
            if any(c.isupper() for c in tag):
                continue

            # Don't add duplicate tags
            if tag not in tags:
                tags.append(tag)

    return [t for t in tags if len(t) > 0]
