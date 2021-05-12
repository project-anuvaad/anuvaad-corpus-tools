
# this script is used to get  marathi urls in THEWIRE Website .
#   this script is only to get social category urls in marathi , we have to change link variable  to get other category urls.


from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import tqdm


chrome_path='/home/test/Downloads/chromedriver_linux64 (1)/chromedriver'
driver=webdriver.Chrome(chrome_path)

def get_urls():
    
    links=[]
    dates=[]

    # the number of pages available in the marathi  in  social  category  is 68  , we have to update this  as pages available on that date  in future . . 
    for page_num in tqdm.tqdm(range(1,68)): 
        # we should change this link variable for every new category .
        # this is only for social category .
        link='https://marathi.thewire.in/category/social/page/'+str(page_num)+'/'


        driver.get(link)
        for num in range(1,11):
            link_get=driver.find_element_by_xpath('//*[@id="widget-content-magone-archive-blog-rolls"]/div['+str(num)+']/div[1]/div[2]/a[3]')
            date_get=driver.find_element_by_xpath('//*[@id="widget-content-magone-archive-blog-rolls"]/div['+str(num)+']/div[1]/div[2]/a[3]/span')
            links.append(link_get.get_attribute("href"))
            dates.append(date_get.text)
    return links,dates
if __name__=='__main__':
    urls,dates=get_urls()
    df=pd.DataFrame()
    df['date']=dates
    df['url']=urls
    print(df)

