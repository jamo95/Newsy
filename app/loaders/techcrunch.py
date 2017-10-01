import requests

from bs4 import BeautifulSoup

from helpers import clean_html


BASE_URL = 'https://techcrunch.com/'


class ArticleLoader():
    @staticmethod
    def load(url):
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')

        return {
            'content': _get_content(html),
            'title': _get_title(html),
            'tags': _get_tags(html),
            'url': url,
        }


def _get_title(html):
    return html.select('.tweet-title')[0].contents[0]


def _get_content(html):
    raw_content_str = map(str, html.select('.text')[0].contents)
    return clean_html(' '.join(raw_content_str))


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
