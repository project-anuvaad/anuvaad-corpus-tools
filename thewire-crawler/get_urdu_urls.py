# this script is used to get all urls in  adbistan category in urdu .


from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
import tqdm





def get_urls():
    all_links=[]
    all_dates=[]

    # here range(10) is the number of pages available in  adbistan category .
    for pages_numbers in tqdm.tqdm(range(10)):
        # we should change this lin variable for every new topic (category) in urdu.
        lin='http://thewireurdu.com/category/adbistan/page/'+str(pages_numbers)+'/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url =lin
        req = Request(url=reg_url, headers=headers) 
        content = urlopen(req).read()

        #res = requests.get('https://www.sakshi.com/telugu-news/andhra-pradesh/cm-ys-jagan-making-dreams-poor-people-come-true-1335752')
        #soup = BeautifulSoup(res.text,"lxml")


        #url = urlopen('http://hindi.catchnews.com/cricket-news-in-hindi/ind-vs-aus-despite-fractured-thumb-i-was-ready-to-bat-against-australia-ravindra-jadeja-209288.html')
        #content = url.read()

        soup = BeautifulSoup(content, 'lxml')


        table = soup.findAll('div',attrs={"class":"main"})

        articles=table[0].find_all('article')

        for art in range(len(articles)):

            all_dates.append(articles[art].time.text)
            all_links.append(articles[art].a['href'])
    return all_links,all_dates

if __name__=='__main__':
    
    links,dates=get_urls()
    
    df=pd.DataFrame()
    df['date']=dates
    df['link']=links
    print(df)


