from sqlalchemy import Column, Integer, Text, String, Float, ForeignKey

from . import Base


class Sentence(Base):
    __tablename__ = 'sentences'

    id = Column(Integer, primary_key=True)
    data = Column(Text, index=True)
    score = Column(Float)
    index = Column(Integer)
    article_hash = Column(
        String(64), ForeignKey('articles.hash', ondelete='CASCADE'))

    def __init__(self, data, score, index):
        self.data = data
        self.score = score
        self.index = index
