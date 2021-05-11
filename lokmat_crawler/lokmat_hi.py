import requests
import time
import os
import sys
import numpy as np
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
headings_list = []
dates_list = []
link_list = []
lang = str(sys.argv[1])
section = str(sys.argv[2])
nos = int(sys.argv[3])
for count in tqdm(range(nos),total=nos):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    link = f"https://www.lokmatnews.in/{section}/page/{count}/"
    markup_string = requests.get(link, headers=headers, stream=True).content
    soup = BeautifulSoup(markup_string, "html.parser")

    for div in soup.find_all("section", {"class":"multiple-story"}):
        for heading in div.find('h3'):
            headings_list.append(heading.text)
            link_list.append(f"https://www.lokmatnews.in{heading.get('href')}")
            #for date in soup.find("span", {"class":"bd-hour"}):
            dates_list.append(np.nan)

df = pd.DataFrame({'Headings': headings_list, 'Date': dates_list, 'Link': link_list}) 
print ("Complete")
df.to_csv(f"{lang}_lokmat_{section}.csv",
            mode='w',
            encoding='utf-16',
            index=False,
        )

