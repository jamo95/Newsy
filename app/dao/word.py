from sqlalchemy import Column, ForeignKey, Integer, String

from . import Base


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String(), index=True)
    tag = Column(String(10))
    keyword_id = Column(
        Integer, ForeignKey('keywords.id', ondelete='CASCADE'))

    # For compatability with Helium module.
    data = None

    def __init__(self, word, tag):
        self.word = word
        self.data = word
        self.tag = tag
