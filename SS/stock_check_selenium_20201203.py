# make necessary imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import shutil
from datetime import datetime

#requests imports
import pprint
import bs4
import requests

#import database
import pandas as pd
df = pd.read_csv(r"C:\Users\bRIKO\Google Drive\Learning\Programming\Python\Scripts\MyPythonScripts\LCBO Stock Checker\productid.csv")
print(df.head())

base_url = 'https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId='


def get_pagesource(url,counter):
    options = webdriver.ChromeOptions()

    # non headless browser
    # options.add_argument("start-maximized")
    # options.add_argument("--disable-blink-features")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)

    # only log fatal errors
    options.add_argument('log-level=3')

    # base options
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ingognito")
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        options=options,
        executable_path=r"C:\Users\bRIKO\Python Resources\Version 87\chromedriver.exe",
    )

    # print(driver.execute_script("return navigator.userAgent;"))
    driver.get(
        url + str(df['ProductID'][counter])
    )

    return driver.page_source

def get_soup(x):
    soup = bs4.BeautifulSoup(x,"html.parser")
    # print(soup.prettify())

    return len(soup.find_all("div",{"class":"col-xs-4"}))

for x in range(len(df)):

    y = get_pagesource(base_url,x)
    z = get_soup(y)

    # print search query
    print(str(df['Name'][x]) + " (" + str(df['ProductID'][x]) + ")")
    if z > 5:
        print("In Stock!")
    else:
        print("Out of Stock :(")

print("\nDone!")