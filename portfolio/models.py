from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.urls import url_fix

from portfolio.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(20))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'{self.username}'


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    name_url = Column(String(40), unique=True)
    hidden = Column(Boolean, default=True)
    pictures = relationship('Picture', back_populates='category')

    def __init__(self, name=None, name_url=None, hidden=None):
        self.name = name
        self.name_url = name_url
        self.hidden = hidden

    def __repr__(self):
        return f'{self.name}'

    def set_name_url(self):
        self.name_url = url_fix(self.name).replace('%20', '-').lower()


class Picture(Base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True)
    title = Column(String(40), unique=True)
    description = Column(String(500))
    filename = Column(String(200), unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='pictures')

    def __init__(self, title, description, category_id, filename):
        self.title = title
        self.description = description
        self.category_id = category_id
        self.filename = filename

    @property
    def url(self):
        return f'static/uploads/{self.filename}'
