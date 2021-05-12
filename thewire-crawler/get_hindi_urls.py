# this script is used to get the all hindi urls in  specific topic
# for every new topic you need to change the url lin 


from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import tqdm
import pandas as pd



def get_urls():
    
    all_links=[]
    all_dates=[]


    #  here 'range(60)'  is the number of pages that available in specific topic 
    # we have to change this number for evrey new topic , based on the pages available in that topic.
    for pages_numbers in tqdm.tqdm(range(60)):
        # change this  ' lin ' variable for every new topic urls scraping 
        lin='http://thewirehindi.com/category/%E0%A4%AD%E0%A4%BE%E0%A4%B0%E0%A4%A4/page/'+str(pages_numbers)+'/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url =lin
        req = Request(url=reg_url, headers=headers) 
        content = urlopen(req).read()

        soup = BeautifulSoup(content, 'lxml')


        table = soup.findAll('div',attrs={"class":"main"})

        articles=table[0].find_all('article')

        for art in range(len(articles)):

            all_dates.append(articles[art].time.text)
            all_links.append(articles[art].a['href'])

            
    return all_links,all_dates


if __name__=='__main__':
    urls,dates=get_urls()
    df=pd.DataFrame()
    df['date']=dates
    df['link']=urls
    print(df)
