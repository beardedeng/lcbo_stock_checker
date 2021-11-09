import pandas as pd
import numpy as np
from datetime import datetime

#requests imports
import pprint
import bs4
import requests

df = pd.read_csv(r"C:\Users\bRIKO\Google Drive\Learning\Programming\Python\Scripts\MyPythonScripts\LCBO Stock Checker\productid.csv")
print(df.head())

base_url = 'https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId='

def get_soup(url):
    # define headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    # converts requests into bs4
    return bs4.BeautifulSoup(res.text, "html.parser")

# soup = get_soup(base_url + str(df['ProductID'][0]))

for x in range(len(df)):

    # print search query
    print(str(df['Name'][x]) + " (" + str(df['ProductID'][x]) + ")")

    # get soup object from link
    soup = get_soup(base_url + str(df['ProductID'][x]))

    print(soup.prettify())

    #confirm stock
    try:
        # search_item = soup.find_all("div",class_="no-results")
        search_item = soup.find_all("div",class_="col-xs-4")
        print("No Stock")
    except:
        print("Stock!!!")

# Create dataframe
df = pd.DataFrame.from_dict(x,orient='index')
print(df.head())

# Format Dates Correctly
df['date_temp'] = df['date_monthyear'] + " " + df['date_day']
df['date'] = pd.to_datetime(df['date_temp'],format='%B %Y %d')

#drop old date columns
df.drop(['date_monthyear','date_day','date_temp'],axis=1,inplace=True)

#reorder dataframe
df = df[['date','event','link']]

#reset index starting from 1
df.index = np.arange(1, len(df) + 1)

print(df.head())