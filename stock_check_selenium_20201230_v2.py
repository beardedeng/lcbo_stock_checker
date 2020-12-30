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

# import pandas
import pandas as pd

# ipmort sqlalchemy integration
from get_product_list import (
    get_all_spirits,
    Session,
    update_stock,
    try_commmit,
    get_all_spirits_and_stock,
)

base_url = "https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId="


def run_timeout(timer=None):

    if timer is None:
        while True:
            start_selenium_instance()
    else:
        datetime_now = datetime.datetime.now()
        while datetime.timedelta(hours=timer) + datetime_now > datetime.datetime.now():
            start_selenium_instance()


def start_selenium_instance():
    """Persists an instance of selenium. For a specific time if timer is given

    Args:
        timer ([type], optional): [time in hours]. Defaults to None.
    """

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

    return driver


def get_pagesource(url, counter, driver):

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

        store_id = int(
            (
                soupey.find_all("div", {"class": "col-xs-12"})[3]
                .contents[2]
                .contents[1]
                .contents[0]["data-store-id"]
            )
        )

        stock_level = int(
            (
                soupey.find_all("div", {"class": "col-xs-12"})[3]
                .contents[2]
                .contents[0]
                .get_text()
            )
        )

    else:
        city = "N/A"
        store_address = "N/A"
        store_phone_number = "N/A"
        store_id = 0
        stock_level = 0

    elems_dict_temp = {
        "in_stock": in_stock,
        "city": city,
        "store_address": store_address,
        "store_phone_number": store_phone_number,
        "store_id": store_id,
        "stock_level": stock_level,
    }

    return elems_dict_temp


def get_stock_level_info(page_source, all_spirits):
    # define empty list for stock_level information list of dictionaries
    elems_list = []

    for x in range(len(page_source)):

        soup = get_soup(page_source[x])

        dict1 = {"product_name": all_spirits[x][1], "product_id": all_spirits[x][0]}

        stock_level_info = get_soup_information(soup)

        dict1.update(stock_level_info)
        dictionary_copy = dict1.copy()
        elems_list.append(dictionary_copy)

    return elems_list


def update_stock_level_pandas(elems_list):
    df = pd.DataFrame(elems_list)

    current_date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    df["last_updated"] = current_date_time

    # df.to_csv("Supporting_Files\stock_level.csv", index=False)
    df.to_csv("Supporting_Files\stock_level1.csv", index=False)

    print(f"\nSuccessfully finished running at {current_date_time}")

    df_in_stock_yes = df[df["in_stock"] == "Yes"]

    df_length = len(df_in_stock_yes["in_stock"])

    print(f"\n{df_length} products are in stock:")

    for row in range(df_length):
        print(
            f"{df_in_stock_yes['product_name'][row]} {df_in_stock_yes['product_id'][row]} - Stock Level: {df_in_stock_yes['stock_level'][row]}"
        )


def udpate_stock_level_postgresql(elems_list):
    # return stock objects that match product_ids
    pass


def has_stock_changed(original_stock, current_stock):
    tup1 = original_stock

    productid2 = [sub["product_id"] for sub in current_stock]
    stock_level2 = [sub["stock_level"] for sub in current_stock]

    tup2 = []

    for x in range(len(productid2)):
        tup2.append((productid2[x], stock_level2[x]))

    tup3 = []

    # check if tuples are the same
    for y in range(len(tup1)):
        if tup1[y][1] != tup2[y][1] and tup2[y][1] == 0:
            print(f"{tup1[y]} is now out of stock.")

            # marks update as out of stock
            tup3.append((tup1[y][0], "OOS"))

        elif tup1[y][1] != tup2[y][1] and tup1[y][1] == 0:
            print(f"{tup1[y][0]} is now in stock!!!")
            print(f"{tup1[y][0]} is now in stock!!!")
            print(f"{tup1[y][0]} is now in stock!!!")

            # marks update as in stock
            tup3.append((tup1[y][0], "IS"))

        else:
            # print(f"{tup1[y][0]} stock status hasn't changed.")

            # marks update as no change
            tup3.append((tup1[y][0], "NC"))

    return tup3


def main():

    # get listof tuples of spirits from PostgresSQL
    all_spirits = get_all_spirits()

    # translates all_spirits to list of product ids
    all_spirits_productids = [value1 for value1, value2 in all_spirits]

    # open driver
    driver = start_selenium_instance()

    while True:

        # gets most recent stock levels
        existing_stock_levels = get_all_spirits_and_stock()

        # gets the page source from all all_spirits_productids
        page_source = get_pagesource(base_url, all_spirits_productids, driver)

        # gets relevant stock_level information and stores it in a list of dictionaries
        elems_list = get_stock_level_info(page_source, all_spirits)

        # # use pandas to create .csv of gathered information
        # update_stock_level_pandas(elems_list)

        # update postgresql stock table with elems_list
        update_stock(elems_list)

        elems_list[0]["stock_level"] = 0
        elems_list[5]["stock_level"] = 1

        # check to see if stock has increased from 0 or fallen to 0
        has_it_changed = has_stock_changed(existing_stock_levels, elems_list)

        # commit but if errors, rollback
        try_commmit()

        # sleep timer for scraper
        time.sleep(30)


if __name__ == "__main__":
    main()
