# requests imports
import pprint
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json
import random

html = urlopen('http://www.pythonscraping.com/pages/page3.html')

bs = BeautifulSoup(html,'html.parser')

print(bs.find('img',{'src':'../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())
