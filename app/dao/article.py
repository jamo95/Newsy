import datetime
import hashlib
import re

from sqlalchemy import Column, Text, String, Date
from sqlalchemy.orm import relationship

from . import Base
from .keyword import Keyword
from .sentence import Sentence
from .word import Word


class Article(Base):
    __tablename__ = 'articles'

    hash = Column(String(64), primary_key=True)
    text = Column(Text)
    title = Column(String(200), nullable=True)
    url = Column(String(2083), nullable=True)
    published_at = Column(Date, nullable=True)
    created_at = Column(Date, default=datetime.datetime.now)

    keywords = relationship('Keyword')
    sentences = relationship('Sentence')

    def __init__(self, article_hash, text, title, url, published_at=None):
        self.hash = article_hash
        self.text = text
        self.title = title
        self.url = url
        self.published_at = published_at

        self.keywords = []
        self.sentences = []


def insert(session, text, title, url, keywords, sentences, published_at=None):
    article_hash = hash_article(text)
    article_exists = session.query(Article.hash).filter_by(
        hash=article_hash).scalar() is not None

    if article_exists:
        return

    article = Article(article_hash, text, title, url, published_at)
    article.sentences = [
        Sentence(s.data, s.score, s.index) for s in sentences]

    for kw in keywords:
        keyword = Keyword(kw.data, kw.score)
        keyword.variations = [Word(w.data, w.pos) for w in kw.variations]
        article.keywords.append(keyword)

    session.add(article)
    session.commit()


def hash_article(text):
    text = re.sub(r'\W+', '', text)
    text = text.lower()

    text = text.encode('utf-8')
    return hashlib.sha256(text).hexdigest()
