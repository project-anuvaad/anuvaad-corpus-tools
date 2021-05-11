# this script is used to crawl the english data from urls
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from lxml import html
from csv import writer
import tqdm



def get_data(df):

    all_l=list(df['link'])

    for ln in tqdm.tqdm(range(len(all_l))):
        try :

            lin=df.iloc[ln,0]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            reg_url =lin
            req = Request(url=reg_url, headers=headers) 
            content = urlopen(req).read()

            soup = BeautifulSoup(content, 'lxml')



            news_article=[]


            table2 = soup.findAll('span',attrs={"itemprop":"datePublished"})
            x=table2[0].text


            date_time=x


            table1 = soup.findAll('div',attrs={"class":"story-head pB0"})
            x=table1[0].find('h1')


            news_article.append(x.text)



            table = soup.findAll('span',attrs={"class":"p-content"})
            x=table[0].find_all('p')

            y=table[0].find_all('h1')

            z=table[0].find_all('td')

            for i in x:  
                    news_article.append(i.text)
            for i in y:  
                    news_article.append(i.text)

            for i in z:  
                    news_article.append(i.text)




            List=[date_time,lin,news_article]
            with open('BS_english5.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()
        except:
            print('some thing went wrong')


            
            
if __name__=='__main__':
    
    df=pd.read_csv('BS_en_total_urls.csv')
    get_data(df)
    
    
