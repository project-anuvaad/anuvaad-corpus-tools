#this script is used to get all english urls in THEWIRE Website 
#imports
import requests
import json
import tqdm
import pandas as pd



def get_urls():
    links=[]
    dates=[]
    # here 5 represents number of pages available , and  here  each has 1000 urls 
    for i in tqdm.tqdm(range(5)):
        try:
            link="https://thewire.in/wp-json/thewire/v2/posts/opinion/all/recent-stories/?orderedpost=100&page="+str(i)+"&recentpost=1000"
            markup_string = requests.get(link, stream=True)
            print(len(json.loads(markup_string.text)))

            index_range=999
            for index in range(index_range):
                try:
                    link_end_text = (json.loads(markup_string.text)[index]['post_name'])
                    link_category = (json.loads(markup_string.text)[index]['prime_category'][0]['slug'])
                    link = 'https://thewire.in/'+link_category + '/' + link_end_text
                    date= (json.loads(markup_string.text)[index]['post_date'])
                    links.append(link)
                    dates.append(date)
                    #print(date , link)
                except :
                    print(str(index) + 'got error ')
        except:
            print(str(i) +'page not found')
    return links,dates


if __name__=='__main__':
    links,dates=get_urls()
    dates1=[dat.split()[0] for dat in dates]
    df=pd.DataFrame()
    df['date']=dates1
    df['link']=links
    print(df)
