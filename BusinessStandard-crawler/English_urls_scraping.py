# this script is used to get all english urls in specific date range
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import pandas as pd
import tqdm
from urllib.request import urlopen, Request
import pandas as pd
import datetime
import pandas as pd
import pandas as pd
from csv import writer


def get_english_urls():
    all_years=[]
    # metion the satrt and end date to scrap urls in range
    start_date = datetime.date(2008, 1, 1)
    end_date = datetime.date(2021, 3,31)
    delta = datetime.timedelta(days=1)

    while start_date <= end_date:
        #print(start_date)
        d = datetime.datetime.strptime(str(start_date), '%Y-%m-%d')
        all_years.append(datetime.date.strftime(d, "%d-%m-%Y"))
        start_date += delta


    for  real_dat in tqdm.tqdm(all_years):

        for number in range(1,10):

            link='https://www.business-standard.com/advance-search?advance=Y&type=print-media&print_date='+real_dat+'&itemsPerPage=19&page='+str(number)+'#gsc.tab=0'

            url = urlopen(link)
            content = url.read()


            soup = BeautifulSoup(content, 'lxml')

            table = soup.findAll('div',attrs={"class":"listing-main topB mT10"}) 

            all_dates=[tab.text.split('|')[0]  for tab in table[0].find_all('p')[::2]]

            all_links=['https://www.business-standard.com'+tab.a['href']   for  tab in   table[0].find_all('h2')]

            List=[all_dates,all_links]
            with open('BS_english_urls_withdat.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()
                
if __name__=='__main__':
    get_english_urls()
    

