#!/usr/bin/env python3
# based on joshleeb's techcrunch loader: https://github.com/joshleeb/pylonproto/blob/64123cc982f48d65abb7f666b5602d92d6e9a05d/pylonproto/pylons/argon/argon/loaders/techcrunch.py
import dateutil.parser
import grequests
import requests
import re

from bs4 import BeautifulSoup
from datetime import datetime


BASE_URL = 'https://techcrunch.com/'


def clean_html(html):
    # Remove header tags including content.
    html = re.sub(r'<h(\d).*?</h\1>', '', html)
    # Strip surrounding tags.
    text = re.sub(r'<.*?>', '', html)
    # Strip surrounding whitespace.
    return text.strip()

class Archive:
    def __init__(self, site_name):
        self.site = site_name
        self.articles = []
        self.timestamp = None
        self.url = None

class Article:
    def __init__(self, url):
        self.url = url.strip('\n')

        self.links = None
        self.tags = None
        self.text = None
        self.timestamp = None
        self.title = None

class ArchiveLoader():
    @staticmethod
    def load(year, month, day):
        date_path = '{}/{:02d}/{:02d}'.format(year, month, day)
        archive = Archive('TechCrunch')
        archive.url = BASE_URL + date_path
        archive.timestamp = datetime.strptime(date_path, '%Y/%m/%d')
        archive.articles = _get_articles(archive.url)
        return archive


def _get_articles(url):
        articles = []

        response = requests.get(url)
        if not 200 <= response.status_code < 300:
            return None

        html = BeautifulSoup(response.text, 'html.parser')
        post_titles = html.select('.post-title')

        article_links = []
        for post_title in post_titles:
            link = post_title.select('a')[0].attrs['href']
            if link.replace('www.', '').startswith(BASE_URL):
                article_links.append(link)
        responses = (grequests.get(u) for u in article_links)
        for response in grequests.map(responses):
            if response:
                articles.append(
                    ArticleLoader.load(response.url, response.text))
        return articles


class ArticleLoader():
    TAGS = ['tech']
    @staticmethod
    def load(url, content):
        html = BeautifulSoup(content, 'html.parser')
        article = Article(url)
        article.title =  re.findall(r'<title.*?>(.*?)</title>',content)[0]
        article.text = ""
        content_section = False
        for line in content.splitlines():
            if "<!-- End: Wordpress Article Content -->" in line:
                content_section = False
            if content_section:
                article.text += str(line)
            elif "<!-- Begin: Wordpress Article Content -->" in line :
                content_section = True
        tag_remover = re.compile(r'<[^>]+>')
        article.text = tag_remover.sub(' ', article.text)
        article.timestamp = _get_article_timestamp(html)
        article.tags = _get_article_tags(html)
        article.links = _get_article_links(html)
        return article


def _get_article_timestamp(html):
    title_left = html.select('div.title-left')
    if title_left:
        dates = title_left[0].select('time.timestamp')
        if dates:
            date = dates[0].attrs['datetime']
            return dateutil.parser.parse(date)


def _get_article_tags(html):
    tags = []
    for item in html.select('div.acc-handle'):
        text = item.select('a')[0].text
        for tag in text.split(' '):
            tag = tag.replace('\t', '').replace('\n', '').strip().lower()
            if tag not in tags:
                tags.append(tag)
    if 'popular posts' in tags:
        tags.remove('popular posts')
    article_tags = list(filter(lambda t: len(t) > 0, tags))
    for site_tag in ArticleLoader.TAGS:
        if site_tag not in article_tags:
            article_tags.append(site_tag)
    return article_tags


def _get_article_links(html):
    links = []
    for text in html.select('div.text'):
        anchor_tags = text.select('a')

        for anchor in anchor_tags:
            if anchor and anchor.text:
                links.append((anchor.text.strip(), anchor.attrs.get('href')))
    return links
