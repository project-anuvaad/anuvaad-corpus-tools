import requests
from bs4 import BeautifulSoup
from pathlib import Path
import os
import time
import math
import random
import pandas as pd

acceptable_langs = ['Kannada','Bangla','Marathi','Odia','Urdu','Tamil','Hindi','Assamese','Malayalam','Telugu','Punjabi','Gujarati']
acceptable_lang_c = ['kn','bn','mr','or','ur','ta','hi','ml','te','pa','gu']
next_links = ['/wiki/Supreme_Court']

def get_next_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")
    div = soup.find('div',attrs={'id':'content'})
    aas = div.find_all('a',href=True)
    for a in aas:
        if(a is None):
            continue
        elif('/wiki/File:' in a['href']):
            continue
        elif('/wiki/Wikipedia:' in a['href'] or '/wiki/Category:' in a['href'] or 'Portal:' in a['href'] or 'Template' in a['href'] or 'Special:' in a['href'] or 'https://' in a['href'] or 'wikisource' in a['href']):
            continue
        elif('#' in a['href']):
            continue
        elif('_(disambiguation)' in a['href']):
            continue
        elif('/wiki/'in a['href'] and a['href'] not in next_links ):
            next_links.append(a['href'])

def get_id():
    uuid = str(hex(math.floor((2+random.random()) * 0x80000000)))[2:8]
    return uuid

def scrape_and_write(url,file_name):
    text = ''
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    div = soup.find('div',attrs={'id':'content'})
    f = open(file_name,'w',encoding='utf-16')
    p_tags = div.find_all('p')
    for p in p_tags:
        if(p.get_text().strip() != ''):
            sups = p.find_all('sup',attrs={'class':'reference'})
            text += ' '.join(p.get_text().strip().split())
            for sup in sups:
                text = text.replace(sup.get_text(),'')
            text += ' '
    f.write(text)
    f.close()


def get_other_langs(uuid,url,path):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    nav = soup.find('nav',attrs={'id':'p-lang'})
    lis = nav.find_all('li')
    for li in lis:
        a = li.find('a')
        lang = a['lang']
        if(lang in acceptable_lang_c):
            scrape_and_write(a['href'],os.path.join(path,uuid+'-'+lang+'.txt'))


def main():
    something = []
    path = 'Scraped_Files'
    handled_links = []
    if(os.path.exists('Links_to_UUID.csv')):
        df_hl = pd.read_csv('Links_to_UUID.csv')
        handled_links = df_hl['URL'].tolist()
    Path(path).mkdir(parents=True,exist_ok=True)
    for i,u in enumerate(next_links):
        base_url = 'https://en.wikipedia.org'
        url = base_url+u
        get_next_links(url)
        if(url in handled_links):
            next_links.remove(u)
            continue
        print(u)
        uuid = get_id()
        something.append([url,uuid])
        scrape_and_write(url,os.path.join(path,uuid+'-en.txt'))
        get_other_langs(uuid,url,path)
        df = pd.DataFrame(something)
        if(not os.path.exists('Links_to_UUID.csv')):
            df.to_csv('Links_to_UUID.csv',header=['URL','UUID'],index=False,mode='a')
        else:
            df.to_csv('Links_to_UUID.csv',header=False,index=False,mode='a')
        something = []
    print(len(next_links))

if __name__ == '__main__':
    main()
