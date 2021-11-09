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


def LCBOselenium(url):
    options = webdriver.ChromeOptions()
    
    # options.add_argument("start-maximized")
    # options.add_argument("--disable-blink-features")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)

    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ingognito")
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        options=options,
        executable_path=r"C:\Users\bRIKO\Python Resources\chromedriver.exe",
    )

    # driver.execute_cdp_cmd(
    #     "Page.addScriptToEvaluateOnNewDocument",
    #     {
    #         "source": """
    #     Object.defineProperty(navigator, 'webdriver', {
    #     get: () => undefined
    #     })
    # """
    #     },
    # )

    # driver.execute_cdp_cmd(
    #     "Network.setUserAgentOverride",
    #     {
    #         "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"
    #     },
    # )

    # print(driver.execute_script("return navigator.userAgent;"))
    driver.get(
        url + str(df['ProductID'][0])
    )

    page_source = driver.page_source

    soup = bs4.BeautifulSoup(driver.page_source,"html.parser")
    # print(soup.prettify())

    search_item = soup.find_all("div",class_="col-xs-4")

    # time.sleep(5)
    driver.find_element_by_css_selector("#language-selector > div > div > div > div.modal-footer > a:nth-child(1)").click()
    
    username = driver.find_element_by_css_selector("#ius-userid")
    username.send_keys(user_temp)

if __name__ == "__main__":
    # Mint Usernames/Passwords
    mint_username = os.environ.get("MINT_USER")
    mint_password = os.environ.get("MINT_PASS")

    LCBOselenium(base_url)