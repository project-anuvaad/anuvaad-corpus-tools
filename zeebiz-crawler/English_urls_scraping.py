# this script is used to get the english urls of  ZEEBIZ website  for   specific topic ('WORLD')
# in this website specially english  for each topic we can get max 200 urls only .
 

from lxml import html
import requests
import tqdm
import pandas as pd




def get_english_urls():

    all_links=[]
    date_time=[]
    for page_num in tqdm.tqdm(range(20)):
        # we need to change the url link for 'page ' variable to get other topic urls
        page = requests.get('https://www.zeebiz.com/world?page='+str(page_num))
        tree = html.fromstring(page.content)
        #This will create a list of buyers:

        for num in range(1,21):

            buyers = tree.xpath('//*[@id="mostrecent"]/div/div[1]/div[1]/div['+str(num)+']/h5')
            #This will create a list of prices
            prices = tree.xpath('//*[@id="mostrecent"]/div/div[1]/div[1]/div['+str(num)+']/h3/a')


            date_time.append(buyers[0].text)
            all_links.append('https://www.zeebiz.com'+prices[0].get("href"))
    return all_links,date_time

if __name__=='__main__':
    links1,dates1=get_english_urls()
    df=pd.DataFrame()
    df['date']=dates1
    df['link']=links1
    df.drop_duplicates(inplace=True)
    print(df)
    
