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

import re
import random
from bs4 import BeautifulSoup
from random import shuffle
from urllib.request import urlopen

from datetime import datetime

engine = create_engine(
    "postgresql://pythonTest:postgres@localhost:5432/Wikipedia", echo=True
)

Base = declarative_base()

class Pages(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True,nullable=False)
    url = Column(String(255),nullable=False)
    created = Column(DateTime,default=datetime.now(),nullable=False)

class Links(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True,nullable=False)
    fromPageID = Column(Integer)
    toPageID = Column(Integer)
    created = Column(DateTime,default=datetime.now(),nullable=False)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

random.seed(datetime.now())

def try_commit():
    try:
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()

def add_page(urls):
    entry = Pages(url = urls)
    session.add(entry)
    try_commit()
    return entry

def add_link(fromPageIDs,toPageIDs):
    entry = Links(fromPageID = fromPageIDs,toPageID = toPageIDs)
    session.add(entry)
    try_commit()
    return entry    

def insertPageIfNotExists(url):
    if session.query(Pages).filter(Pages.url == url).count() == 0:
        add_page(url)
        return session.query(Pages).order_by(Pages.id.desc()).first().id
    else:
        return session.query(Pages).filter(Pages.url == url).first().id

def loadPages():
    all_pages = session.query(Pages).all()
    paged = [row.url for row in all_pages]
    return paged

def insertLink(fromPageIDs,toPageIDs):
   if session.query(Links).filter(and_(Links.fromPageID == int(fromPageIDs),Links.toPageID == int(toPageIDs))).count() == 0:
       add_link(int(fromPageIDs),int(toPageIDs))

def getLinks(pageUrl,recursionLevel,pages):
    if recursionLevel > 4:
        return

    pageId = insertPageIfNotExists(pageUrl)
    html = urlopen(f'http://en.wikipedia.org{pageUrl}')
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find_all('a',href=re.compile('^(/wiki/)((?!:).)*$'))
    links = [link.attrs['href'] for link in links]

    for link in links:
        insertLink(pageId,insertPageIfNotExists(link))
        if link not in pages:
            #we have encountered a new page, add it and search it for Links
            pages.append(link)
            getLinks(link,recursionLevel+1,pages)

getLinks('/wiki/Kevin_Bacon',0,loadPages())

try:
    while len(links)>0:
        newArticle = links[random.randint(0,len(links)-1)].attrs['href']
        print(newArticle)
        links = getlinks(newArticle)
finally:
    try_commit()
