
import requests
import time
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup

'''Scrapes articles from each link, 
    breaks the entire content into sentences and appends as a line,
    removes special characters to support allowed file names,
    creates a directory and file to write each article as a new txt file
    argv[0] --> filename,
    argv[1] --> csv file path with links to scrape from,
    argv[2] --> directory name.'''

september = pd.read_csv(str(sys.argv[1]))

filenames = september['Headline']

bad_chars = [';', ':', '!', '?', '|', '/', '"', '+', '<', '>', '.', "*"]

start_time = time.time()

for count, link in enumerate(september['Link']):
    markup_string = requests.get(link, stream=True).content
    soup = BeautifulSoup(markup_string, "html.parser")
    content = soup.findAll(['p', 'h1', 'h2', 'figcaption'])
    filename = ''.join(i for i in filenames[count] if not i in bad_chars)
    
    if not os.path.exists(str(sys.argv[2])):
        os.makedirs(str(sys.argv[2]))
    with open(os.path.join(str(sys.argv[2]), f"{count} {filename[:10]}.txt"), mode="w", encoding="utf-16") as file_w:
        for text in range(len(content)):
            file_w.write(content[text].text.strip() + "\r\n")
            
print(' %s seconds ' % (time.time() - start_time))





