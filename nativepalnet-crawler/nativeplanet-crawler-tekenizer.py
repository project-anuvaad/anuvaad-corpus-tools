import pandas as pd
import numpy as np
import re
import tqdm
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time
import argparse
import os
from indicnlp import common
from indicnlp.tokenize import sentence_tokenize
from indicnlp import common
import nltk
from nltk.tokenize import sent_tokenize






# input : link 

link='https://tamil.nativeplanet.com/haryana/attractions/#shaking-minarets'
lan='ta'   #language of the text

outputfile='textnative_haryana.txt' # name of the output file 





# urls scraping 
chrome_path='/home/test/Downloads/chromedriver'
driver=webdriver.Chrome(chrome_path)
driver.get(link)
#driver.maximize_window()

scroll=6000

time.sleep(10)
driver.execute_script("window.scrollTo(0, 1000000);")

time.sleep(60)

driver.execute_script("window.scrollTo(0, 1000000);")

time.sleep(5)

parent=driver.find_element_by_id('destionationsList')

links1=parent.find_elements_by_tag_name("a")
href_links=[]
for el in links1:
        if el.get_attribute('href') == None or not re.search('^http', el.get_attribute('href')):
            pass
        else:
            href_links.append(el.get_attribute("href"))
l=list(set(href_links))

#data scraping
news_article=[]
for lin in tqdm.tqdm(l):
    
    try:
        url = urlopen(lin)
        content = url.read()

        soup = BeautifulSoup(content, 'lxml')


        table = soup.findAll('div',attrs={"class":"np-article-content"})

        for x in table:
            f=x.find_all('p')


        for j in f:  
                text=j.text.replace('\n',' ')
                news_article.append(text)
    except :
        print('not able to  get the text from this url '+lin)

data=list(set(news_article))        


#tokenizer        

if lan!='en':    

    sentences_one=[]
    for sen in data:
        indic_string=sen

        sentences=sentence_tokenize.sentence_split(indic_string, lang=lan)

        # print the sentences
        for t in sentences:
            sentences_one.append(t)
else:
    
    sentences_one=[]
    for sen in data:
        indic_string=sen

        # Split the sentence, language code "hi" is passed for hingi
        sentences=sent_tokenize(sen)

        # print the sentences
        for t in sentences:
            sentences_one.append(t)
sentences1=list(set(sentences_one))
sentences2=[sen for sen in sentences1 if len(sen)>6]     
sentences3=[sen.strip(' \t*.') for sen in sentences2]  

        

with open(outputfile, 'w',encoding='utf-16') as file_handler:
    for item in sentences3:
        file_handler.write("{}\n".format(item))   
        

