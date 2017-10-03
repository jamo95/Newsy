import datetime

from sqlalchemy import Column, Integer, Text, String, Date, Boolean

from . import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    status = Column(Boolean)
    text = Column(Text, nullable=True)
    title = Column(String(200), nullable=True)
    url = Column(String(2083), nullable=True)
    count = Column(Integer, nullable=True)
    created_at = Column(Date, default=datetime.datetime.now)

    def __init__(self, status, text=None, title=None, url=None, count=None):
        self.status = status
        self.text = text
        self.title = title
        self.url = url
        self.count = count


def insert(session, review):
    session.add(review)
    session.commit()
