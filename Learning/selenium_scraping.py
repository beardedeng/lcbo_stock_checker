from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


options = webdriver.ChromeOptions()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=options,executable_path=r"C:/Users/bRIKO/Google Drive/Learning/Programming/ChromeDriver/chromedriver_win32 (1)/chromedriver.exe")

# # utilize sleep to grab information after page load (inefficient)
# driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
# time.sleep(3)
# print(driver.find_element_by_id('content').text)
# driver.close()

# check for a specific element to have loaded before grabbing page information (efficient)
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,    'loadedButton')))
finally:
    print(driver.find_element_by_id('content').text)
    driver.close()