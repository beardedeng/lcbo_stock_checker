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

def getURL(pageId):
    entry = session.query(Pages).filter(Pages.id == int(pageId)).first().url
    return entry

def getLinks(fromPageId):
    entries = session.query(Links).filter(Links.fromPageID == int(fromPageId)).all()
    if len(entries) == 0:
        return[]
    return [entry.toPageID for entry in entries]  

def searchBreadth(targetPageId, paths=[[1]]):
    newPaths = []
    for path in paths:
        links = getLinks(path[-1])
        for link in links:
            if link == targetPageId:
                return path + [link]
            else:
                newPaths.append(path+[link])
    return searchBreadth(targetPageId, newPaths)

nodes = getLinks(1)
targetPageId = 28624
pageIds = searchBreadth(targetPageId)
for pageId in pageIds:
    print(getUrl(pageId))
