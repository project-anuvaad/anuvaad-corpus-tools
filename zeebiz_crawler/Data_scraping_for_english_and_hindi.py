# this script is used for get the english and hindi data from urls in ZEEBIZ
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import pandas as pd
import tqdm
from urllib.request import urlopen, Request
import pandas as pd
from csv import writer
import pandas as pd



def get_data_from_urls(df):

    link_list=list(df['link'])

    problem_urls=[]
    problem_dates=[]

    for url_link_num in tqdm.tqdm(range(len(link_list))):
        try:

            news_article=[]
            lin=link_list[url_link_num]
            new_date=df.iloc[url_link_num,0]
            news_article=[]

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            reg_url =lin
            req = Request(url=reg_url, headers=headers) 
            content = urlopen(req).read()

            soup = BeautifulSoup(content, 'lxml')

            table = soup.findAll('div',attrs={"class":"article-section article-section-new"}) 
            x=table[0].find_all('p')

            y=table[0].find_all('h1')

            z=table[0].find_all('h3')

            for i in x:  
                    news_article.append(i.text)
            for i in y:  
                    news_article.append(i.text)

            for i in z:  
                    news_article.append(i.text)

            List=[new_date,lin,news_article]
            with open('zeebiz_en_text.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()
        except:

            problem_urls.append(link_list[url_link_num])
            problem_dates.append(df.iloc[url_link_num,0])
            print('this url has  problem :  ' + link_list[url_link_num])

        
        

if __name__=='__main__':
    #  give path where you stored the english urls csv file , 
    # for english data crawling you have to give the english urls csv file path
    df=pd.read_csv('URLS/zeebiz_en.csv')
    
    # it will automatically stores into csv file 
    get_data_from_urls(df)

