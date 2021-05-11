# this code is used to get the  'World '  topic   hindi urls and dates  in    'ZEEBIZ' website 

# we have to change the ' lin ' variable (URL) for every topic in hindi ZEEBIZ 

# some  list of  topics in hindi ZEEBIZ : 

   #  world , small-business , technology , banking , india etc...


# we should have these libraries pre-installed  in system 
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import tqdm
import pandas as pd

def get_hind_urls():
    

    all_links=[]
    date_time=[]

    # we need to change this 'range(35)' every  new topic based on number of pages available  for that perticular topic 

    for page_num in tqdm.tqdm(range(35)): 
        try:
            lin='https://www.zeebiz.com/hindi/small-business?page='+str(page_num)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            reg_url =lin
            req = Request(url=reg_url, headers=headers) 
            content = urlopen(req).read()
            soup = BeautifulSoup(content, 'lxml')


            table = soup.findAll('div',attrs={"class":"views-element-container"})
            one=table[2].find_all('div', {'class': 'mostrecent12'})
            for i in range(10):
                all_links.append('https://www.zeebiz.com'+one[i].a['href'])
                date_time.append(one[i].text.split('\n')[-3].strip())
        except:
            print('some thing went wrong with this page number : '+ str(page_num))
    return all_links , date_time

if __name__=='__main__':
    links,dates=get_hind_urls()
    df=pd.DataFrame()
    df['date']=dates
    df['link']=links
    print(df)
    #df.to_csv('ZEEBIZ_hindi_urls_world.csv',index=None)
    
