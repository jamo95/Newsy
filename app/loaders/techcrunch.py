import dateutil.parser
import requests

from bs4 import BeautifulSoup
from datetime import datetime

from app.loaders.helpers import clean_html


BASE_URL = 'https://techcrunch.com/'


class ArchiveLoader():
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


class ArticleLoader():
    @staticmethod
    def load(url):
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')

        return {
            'content': _get_content(html),
            'title': _get_title(html),
            'timestamp': _get_timestamp(html),
            'tags': _get_tags(html),
            'url': url,
        }


def _get_title(html):
    return html.select('.tweet-title')[0].contents[0]


def _get_content(html):
    raw_content_str = map(str, html.select('.text')[0].contents)
    return clean_html(' '.join(raw_content_str))


def _get_timestamp(html):
    title_left = html.select('div.title-left')
    if title_left:
        dates = title_left[0].select('time.timestamp')
        if dates:
            date = dates[0].attrs['datetime']
            return dateutil.parser.parse(date)


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
