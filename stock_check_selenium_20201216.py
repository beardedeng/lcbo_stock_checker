# make necessary imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import shutil
from datetime import datetime

# requests imports
import pprint
import bs4
import requests

# import database
import pandas as pd


base_url = "https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId="


def get_pagesource(url, counter):
    options = webdriver.ChromeOptions()

    # only log fatal errors
    options.add_argument("log-level=3")

    # base options
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ingognito")
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        options=options,
        executable_path=r"C:\Users\bRIKO\Python Resources\Version 87\chromedriver.exe",
    )

    page_source_list = []

    for item in counter:

        # print(driver.execute_script("return navigator.userAgent;"))
        driver.get(url + str(item))

        page_source_list.append(driver.page_source)

    return page_source_list


def get_soup(x):
    soup = bs4.BeautifulSoup(x, "html.parser")
    # print(soup.prettify())

    return soup


def get_soup_information(soupey):

    # find if item is in stock. If more than 5 found, then item is in stock in at least one location.
    if len(soupey.find_all("div", {"class": "col-xs-4"})) > 5:
        in_stock = "Yes"
    else:
        in_stock = "No"

    # location with highest stock
    if in_stock == "Yes":
        city = (
            soupey.find_all("div", {"class": "col-xs-12"})[3]
            .contents[0]
            .get_text()
            .capitalize()
        )

        store_address = (
            soupey.find_all("div", {"class": "col-xs-12"})[3]
            .contents[1]
            .contents[2]
            .title()
        )
        store_phone_number = (
            soupey.find_all("div", {"class": "col-xs-12"})[3]
            .contents[1]
            .contents[4]
            .strip()
        )

        store_id = (
            soupey.find_all("div", {"class": "col-xs-12"})[3]
            .contents[2]
            .contents[1]
            .contents[0]["data-store-id"]
        )

        stock_level = (
            soupey.find_all("div", {"class": "col-xs-12"})[3]
            .contents[2]
            .contents[0]
            .get_text()
        )

    else:
        city = "N/A"
        store_address = "N/A"
        store_phone_number = "N/A"
        store_id = "N/A"
        stock_level = "N/A"

    elems_dict_temp = {
        "in_stock": in_stock,
        "city": city,
        "store_address": store_address,
        "store_phone_number": store_phone_number,
        "store_id": store_id,
        "stock_level": stock_level,
    }

    return elems_dict_temp


def main():

    while True:

        df = pd.read_csv("productid.csv")

        y = get_pagesource(base_url, df["ProductID"])

        elems_list = []

        for x in range(len(y)):

            z = get_soup(y[x])

            dict1 = {"product_name": df["Name"][x], "product_id": df["ProductID"][x]}

            z = get_soup_information(z)

            dict1.update(z)
            dictionary_copy = dict1.copy()
            elems_list.append(dictionary_copy)

            # # print search query
            # print("\n" + str(df["Name"][x]) + " (" + str(df["ProductID"][x]) + ")")

        df = pd.DataFrame(elems_list)

        current_date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        df["last updated"] = current_date_time

        df.to_csv("Supporting_Files\stock_level.csv", index=False)

        print(f"\nSuccessfully finished running at {current_date_time}")

        time.sleep(30)


if __name__ == "__main__":
    main()
