# importing libraries

import os
import re
import csv
import shutil
import requests
import pandas as pd
import urllib.request
from tqdm import tqdm
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing import Pool

#scrape link
url = "https://eparlib.nic.in/" 
# print(url)

#scrape date
dates = []
def scrape_dates(Link):
  req = requests.get(Link)
  soup  = BeautifulSoup(req.text,'html.parser')
  lok_sabha = soup.find('table', class_ = 'panel table table-bordered table-hover')
  datess = lok_sabha.find_all('td', headers = 't1')
  for date in datess:
      d = date.text
      dates.append(d)

#parse through pages
for i in tqdm(range(41,60)):       #change the range in accordance
    num = 100 * i
    page_url = url +'handle/123456789/6/browse?type=date&sort_by=1&order=ASC&rpp=100&etal=-1&null=&offset='+str(num)

    scrape_dates(page_url)

len(dates)


data_url = []
def scrape_parse(Link):
  req = requests.get(Link)
  soup  = BeautifulSoup(req.text,'html.parser')
  lok_sabha = soup.find('table', class_ = 'panel table table-bordered table-hover')
  data_link = lok_sabha.find_all('a',href=True)
  for i in data_link:
      temp = url + i['href']
      data_url.append(temp)


for i in tqdm(range(41,60)):           #change the range in accordance
    num = 100 * i
    page_url = url +'handle/123456789/6/browse?type=date&sort_by=1&order=ASC&rpp=100&etal=-1&null=&offset='+str(num)

    scrape_parse(page_url)

len(data_url)

#create dataframe

df = pd.DataFrame(dates, columns = ['date'])
df['url_parse'] = data_url

df.to_csv('debate_en.csv', encoding = 'utf-16', mode = 'w', index = False)

files = pd.read_csv('debate_en.csv', encoding = 'utf-16')
# files.head()

#parse through links for pdf links

pdf_links = []
for i in tqdm(range(0,len(files['url_parse']))):
    req = requests.get(files['url_parse'][i])
    soup  = BeautifulSoup(req.text,'html.parser')
    lok_sabha = soup.find('table', class_ = 'table panel-body')
    lok_sabha = lok_sabha.find('td', headers = 't1')
    pdf_link = lok_sabha.find('a',href=True)
    print(res)
    res = url + pdf_link['href']
    pdf_links.append(res)

len(pdf_links)

files['pdf_link'] = pdf_links

files.to_csv('debate_en_links.csv', encoding = ' utf-16', mode = 'w', index = False)
# files

# def download_file(download_url, filename):
#     response = urllib.request.urlopen(download_url)    
#     file = open(filename + ".pdf", 'wb')
#     file.write(response.read())
#     file.close()

# print(pdf_links[0])


links_data = pd.read_csv('debate_en_links_pdf.csv',encoding='utf-16')
links_data

file_name = []
for i in range(0,len(links_data['pdf_link'])):
    pdf_path = links_data['pdf_link'][i]
    d = pdf_path.split('/')
    file_name.append(d[8])

links_data['file_name'] = file_name
links_data.to_csv('debate_en_pdf_links.csv', mode = 'w', encoding = 'utf-16', index = False)

final = pd.read_csv('debate_en_pdf_links.csv', encoding = 'utf-16')
final


out_dir = "debates_en_pre_pdf"       #change the directory name for different sections
os.makedirs(out_dir)

#download the pdf

def download_file(urls):
    local_filename = urls.split('/')[-1]
    with requests.get(urls, stream=True) as r:
        with open(os.path.join(out_dir,local_filename), 'wb') as f:
            shutil.copyfileobj(r.raw, f)


for i in tqdm(range(0, len(final['pdf_link']))):
    pdf_path = final['pdf_link'][i]
    
#     pdf_name = local_filename
    download_file(pdf_path)

