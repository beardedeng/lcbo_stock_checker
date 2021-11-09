from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    BigInteger,
    DateTime,
    or_,
    and_,
    not_,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from bs4 import BeautifulSoup
import re
import random
from urllib.request import urlopen

from datetime import datetime

engine = create_engine(
    "postgresql://pythonTest:postgres@localhost:5432/Wikipedia", echo=True
)

Base = declarative_base()

class Pages(Base):
    __tablename__ = "pages"

    id = Column(BigInteger, primary_key=True,nullable=False)
    title = Column(String(200))
    content = Column(String(10000))
    created = Column(DateTime,default=datetime.now(),nullable=False)

class Links(Base):
    __tablename__ = "links"

    id = Column(BigInteger, primary_key=True,nullable=False)
    title = Column(String(200))
    content = Column(String(10000))
    created = Column(DateTime,default=datetime.now(),nullable=False)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

random.seed(datetime.now())

def add_page(title_entry, content_entry):
    entry = Pages(title=title_entry, content=content_entry)
    session.add(entry)
    try_commit()
    return entry

def show_entries():
    """Get all Spirits' product ids and product names

    Returns:
        [list]: [list of tuples of all product ids and product names]
    """

    all_entries = session.query(Pages.title, Pages.content).all()

    # product_ids = [value for value, in all_spirits]

    return all_entries

def getlinks(articleURL):
    html = urlopen('http://en.wikipedia.org'+articleURL)
    bs = BeautifulSoup(html, 'html.parser')
    title = bs.find('h1').get_text()
    content = bs.find('div',{'id':'mw-content-text'}).find('p').get_text()
    add_page(title,content)
    return bs.find('div',{'id':'bodyContent'}).find('a',href=re.compile('^(/wiki/)((?!:).)*$'))

def try_commit():
    try:
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()

links = getlinks('/wiki/Kevin_Bacon')

try:
    while len(links)>0:
        newArticle = links[random.randint(0,len(links)-1)].attrs['href']
        print(newArticle)
        links = getlinks(newArticle)
finally:
    try_commit()

# add_page("Test page title", "This is some test page content. It can be up to 10,000 characters long.")
