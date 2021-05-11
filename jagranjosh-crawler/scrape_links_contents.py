# importing libraries

from bs4 import BeautifulSoup
import requests
import csv
from tqdm import tqdm
import pandas as pd
from datetime import datetime
import re
import os
from multiprocessing import Pool

# Scrape links

links = []
titles = []
url = "https://english.jagran.com"

def scrape(Link):
    req = requests.get(Link)
    soup = BeautifulSoup(req.text, "html.parser")
    file = soup.find_all('ul', class_ = 'topicList')
    
    for content in file:
        Links_new = content.find_all('a', href =True)
        
    for link in Links_new:
        dum = url + link['href']
        #print(dum)
        links.append(dum)
        titles.append(link.find('div', class_ = 'h3').text)

# Create DataFrame

df=pd.DataFrame(links,columns=["link"])

df["title"]=titles

df.to_csv('file_name.csv', encoding = 'utf-16', mode = 'w', index = False)

# Scrape dates

dates = list()
for i in tqdm(range(0,len(links))):
    req = requests.get(links[i])
    soup = BeautifulSoup(req.text, "html.parser")
    data = soup.find('span',class_="fl").text
    dates.append(data)
    
# append date to the required format

year = []
month = []
date = [] #yyyy-mm-dd nd time
for j in tqdm(dates):
    temp = j.split(' ')
    if (temp[0] == 'Publish'):
        month.append(temp[4])
        year.append(temp[5])
        holder = temp[5]+"-"+ temp[4]+"-"+temp[3]+" " + temp[6]
        date.append(holder)

  
    else:
        month.append(temp[3])
        year.append(temp[4])
        holder = temp[4]+"-"+ temp[3]+"-"+temp[2]+" " + temp[5]
        date.append(holder)  
  
df["Year"] = year
df["Month"] = month
df["date"] = date

df.to_csv('file_name_dates.csv', encoding = 'utf-16', mode = 'a', index = False)

# Content Scraping

data = pd.read_csv('/home/test/Jagran-Josh/business/english/file_name_dates.csv', encoding = 'utf-16')
data

all_urls = []
for i in range(0,len(data["link"])):
    all_urls.append(data["link"][i])
    
print(len(all_urls))

# multiprocessing for faster scraping for a large data

def scrapey(url):
    try:
        markup_string = requests.get(url)
        content = []          
        soup = BeautifulSoup(markup_string.text, "html.parser")
        title = soup.find('title').text
        title = title+"~"
        summary = soup.find_all('meta')[2]['content']
        summary = summary+"~"
        content_box = soup.find('div',{'id':'article-des'})
        p = content_box.find_all('p')[:-1:]
        for i in p:
            temp = i.text+"~"
            if(len(temp)>2):
                content.append(temp)
            else:
                continue
        myvar = [title,summary,content]

    except Exception as ex:
        myvar.append("Missing")
        print(str(ex))
    finally:
        if len(myvar) > 0:
            return myvar
        else:
            return None
            
with Pool(100) as p:
    records = list(tqdm(p.imap(scrapey, all_urls)))
    
data['content'] = records
data.to_csv('file_name_content.csv', encoding = 'utf-16')

path = pd.read_csv('/home/test/Jagran-Josh/business/english/file_name_content.csv', encoding = 'utf-16')
path.head()

#  write the contents to text files 

bad_chars = [';', ':', '!', '?', '|', '/', '"', '+', '<', '>', '.', "*"]

out_dir = "jagran_file_name"
file_names = []
for count in tqdm(range(0,len(path['link']))):
    filename = ''.join(i for i in path['title'][count] if not i in bad_chars)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(os.path.join(out_dir, f"{count}_{'_'.join(filename[:10].split())}.txt")):
        try:
            temp_name = f"{count}_{'_'.join(filename[:10].split())}.txt"
            file_names.append(temp_name)
            ddd = str(path['content'][count])
            cont = ddd.replace(u'\\xa0', ' ')
            cont = re.sub("~[\'\"]","\n", cont)
            k = [i.strip().strip(',]["\'').strip() for i in cont.split('\n')]
            k = [i.strip(',]["\'') for i in k]
            with open(os.path.join(out_dir, f"{count}_{'_'.join(filename[:10].split())}.txt"), mode="w", encoding="utf-8") as file_w:
                
                for text in k:
                    file_w.write(text + '\n')
        except Exception as ex:
            temp_name = f"{count}_{'_'.join(filename[:10].split())}.txt"
            file_names.append(temp_name)
            print(ex)

path = path.drop(columns=['content'])
path['content'] = file_names

path.to_csv('file_name_content_final.csv', mode='a', encoding = 'utf-16', index = False)