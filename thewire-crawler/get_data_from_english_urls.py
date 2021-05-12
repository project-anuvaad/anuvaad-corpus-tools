# this script is used to  crawl the data from english urls  and store it as list format

# necessary imports 
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import tqdm
import pandas as pd
from csv import writer




def get_data(df):
    link_list=list(df['link'])

    problem_urls=[]
    problem_dates=[]

    for url_link_num in tqdm.tqdm(range(len(link_list))):
        try : 

            news_article=[]
            lin=link_list[url_link_num]
            new_date=df.iloc[url_link_num,0]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            reg_url =lin
            req = Request(url=reg_url, headers=headers) 
            content = urlopen(req).read()

            soup = BeautifulSoup(content, 'lxml')

            table = soup.findAll('div',attrs={"class":"grey-text"})
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
            with open('thewire_english.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()
        except:
            print('link has problem please check it '+ link_list[url_link_num])
            problem_urls.append(link_list[url_link_num])
            problem_dates.append(df.iloc[url_link_num])

            
            
if __name__=='__main__':
    
    # should provide the   url path where you stored your hindi url csv file
    df=pd.read_csv('HI URLS/thewire_total_english_urls.csv')
    
    get_data(df)

