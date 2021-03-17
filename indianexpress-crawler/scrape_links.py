
import requests
import time
import os
import pandas as pd
from bs4 import BeautifulSoup

'''
    argv[0] --> output folder,
    argv[1] --> month,
    argv[2] --> language,
    argv[3] --> section or topic
    '''

out_folder = str(sys.argv[0])
month = str(sys.argv[1])
language = str(sys.argv[2])
section = str(sys.argv[3])

september = pd.read_csv(f" '{out_folder}/{month}_{language}_articles_ie_{section}_2020.csv', encoding='utf-16' ")

filenames = september['Headings']
bad_chars = [';', ':', '!', '?', '|', '/', '"', '+', '<', '>', '.', "*"]
count = 0

start_time = time.time()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

for link in september['Link'][0:]:
    markup_string = requests.get(link, headers=headers, stream=True).content
    soup = BeautifulSoup(markup_string, "html.parser")
    content = soup.findAll(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figcaption'])
    filename = ''.join(i for i in filenames[count] if not i in bad_chars)
    out_dir = f" '{out_folder}/{month}/{month}_{language}_articles_2020' "
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(os.path.join(out_dir, f"{count} {filename[:10]}.txt"), mode="w", encoding="utf-16") as file_w:
        for text in range(len(content)):
            file_w.write(content[text].text.strip() + "\r\n")       
    count+=1
    
print(' %s seconds ' % (time.time() - start_time))

