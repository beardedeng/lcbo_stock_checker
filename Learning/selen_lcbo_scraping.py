from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


options = webdriver.ChromeOptions()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
# options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=options,executable_path=r"C:/Users/bRIKO/Google Drive/Learning/Programming/ChromeDriver/chromedriver_win32 (1)/chromedriver.exe")

# utilize sleep to grab information after page load (inefficient)
driver.get('https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId=62231')
time.sleep(3)
pageSource = driver.page_source

bs = BeautifulSoup(pageSource, 'html.parser')
print(bs.find(id='content').get_text())

driver.close()