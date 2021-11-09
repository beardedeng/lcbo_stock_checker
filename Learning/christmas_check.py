from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

bs = BeautifulSoup(urlopen('https://isitchristmas.com/'),'html.parser')

while(bs.find('a', {'id':'answer'}).attrs['title'] == 'NO/NON'):
    print('It is not Christmas yet.')
    time.sleep(3600)
    bs = BeautifulSoup(urlopen('https://isitchristmas.com/'),'html.parser')