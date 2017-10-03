from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    word = Column(String(), index=True)
    score = Column(Float)
    article_hash = Column(
        String(64), ForeignKey('articles.hash', ondelete='CASCADE'))

    variations = relationship('Word')

    def __init__(self, data, score):
        self.data = data
        self.score = score

        self.variations = []
