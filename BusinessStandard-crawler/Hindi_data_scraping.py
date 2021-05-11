from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from lxml import html
from csv import writer
import tqdm
import pandas as pd

import pandas as pd



def get_data():
    all_l=list(df[1])

    for ln in tqdm.tqdm(range(len(all_l))):
        try:

            news_article=[]

            url_link=df.iloc[ln,1]
            date_time=df.iloc[ln,0]
            lin=all_l[ln]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            reg_url =lin
            req = Request(url=reg_url, headers=headers) 
            content = urlopen(req).read()

            soup = BeautifulSoup(content, 'lxml')

            gdp_table = soup.find_all("table")
            for i in gdp_table[7].find_all('h1') :
                news_article.append(i.text)

            for i in gdp_table[7].find_all('p'):
                news_article.append(i.text)
            for i in gdp_table[7].find_all('font'):
                news_article.append(i.text)
            for i in gdp_table[7].find_all('div'):
                news_article.append(i.text)


            news_article=list(set(news_article))


            try:
                gdp_table = soup.find_all("table", attrs={"class": "TableClas"})
                gdp_table_data = gdp_table[1].text

                news_article.append(gdp_table_data)
                for  td in gdp_table[0].find_all('td'):
                    news_article.append(td.text)
            except:

                pass
        except : 
            try:
                gdp_table = soup.find_all("table", attrs={"class": "TableClas"})
                gdp_table_data = gdp_table[1].text

                news_article.append(gdp_table_data)
                for  td in gdp_table[0].find_all('td'):
                    news_article.append(td.text)   
            except:
                List1=[date_time,lin]
                with open('BS_hindi_problem_urls.csv', 'a') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(List1)
                    f_object.close()
                print('1 link got problem')



        news_article=list(set(news_article))
        List=[date_time,lin,news_article]
        with open('BS_hindi_prob.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(List)
            f_object.close()

if __name__=='__main__':
    
    df=pd.read_csv('BS_hindi_urls.csv',header=None)
    
