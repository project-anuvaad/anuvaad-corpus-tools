
# this script is used to get all hindi urls in ' Business standard' website

from lxml import html
#import requests

import pandas as pd
import argparse
import numpy as np
import re
import tqdm
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time
import argparse
import os
import time



#driver = webdriver.Chrome(ChromeDriverManager().install())
options = webdriver.chrome.options.Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--log-level=3")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
prefs = {"profile.password_manager_enabled" : False, "credentials_enable_service" : False}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option('excludeSwitches', ['disable-popup-blocking','load-extension', 'enable-automation', 'enable-logging'])
driver = webdriver.Chrome('/home/test/Downloads/chromedriver_linux64 (1)/chromedriver',options=options)

def get_hindi_urls():

    all_links=[]
    date_time=[]
    # here 11713 is  number of pages available for hindi website 
    for page_num in tqdm.tqdm(range(11713)):

        link_name = 'https://hindi.business-standard.com/search.php?id=&pgno='+str(page_num)

        driver.get(link_name)
        for num in range(1,16):
            try :

                buyers = driver.find_elements_by_xpath('/html/body/center/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[7]/td/table/tbody/tr['+str(num)+']/td/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td[2]/a')
                prices = driver.find_elements_by_xpath('/html/body/center/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[7]/td/table/tbody/tr['+str(num)+']/td/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td[3]')


                date_time.append(prices[0].text)
                all_links.append(buyers[0].get_attribute("href"))
            except:
                pass
                #print('got one link problem')
    return all_links,date_time


if __name__=='__main__':
    
    all_links,date_time=get_hindi_urls()
    
    df=pd.DataFrame()
    df['date']=date_time
    df['link']=all_links
    print(df)
