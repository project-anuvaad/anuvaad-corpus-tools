## importing libraries

import os
import re
import wget
import rarfile
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


 ## get links based on particular medium and term

title=[]
links =[]
URL = 'https://www.tntextbooks.in/p/2nd-books.html'
response = requests.get(URL) #headers={'Content-Type': 'application/json; charset=utf-8'})

soup = BeautifulSoup(response.text,'html.parser')
let = soup.find_all('table')
for i in let :
#     f_li = i.find_all('a')
#     ?link = f_li.contents[0]
    print('**************************************************************************')
    anc = i.find_all('a')
    text = i.find('th').text
    title.append(text)
    print(text)
    temp=[]
    for f in anc:
        hre = f['href']
        temp.append(hre)
        print(hre)
    links.append(temp)
    print('--------------------------------------------------------------------------')

len(links)


## create directory for the specifies files

for i in title:
    os.mkdir(i)
    

## align the google drive link for each file to its mediums

for i in range(0, len(links),4):
#     print(links[i:i+4],end='\n')
    print(links[i:i+4])


## download the pdf files

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


## assign the path for the files to be stored

base_path= '/home/test/Project_Anuvaad/tntextbooks/'
for d in tqdm(range(0,len(links))):
    
    for j in links[d]:
        spli = j.strip().split('=')
        file_id = spli[1]
        response = requests.get(j) 
        soup = BeautifulSoup(response.text,'html.parser')
        tel = soup.find('title').text
        tel = tel.split(' ')[0]+'.pdf'
        print(tel)

        

        



        destination = base_path + title[d] + '/'+tel
        download_file_from_google_drive(file_id, destination)


