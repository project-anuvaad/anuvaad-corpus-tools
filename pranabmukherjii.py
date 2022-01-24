#importing libraries

import csv
import re
import os
import requests
import pandas as pd
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

#scrape link

url = 'http://pranabmukherjee.nic.in/'

links = []
dates= []
def func(f):
    page = url + f
    req = requests.get(page)
    soup = BeautifulSoup(req.text, 'lxml')
    data = soup.find('ul', class_ = 'speechlist')
    dat = data.find_all('b')
    new = data.find_all('a', href =True)
    for link in new:
        dum =url+ link['href']
        links.append(dum)
    for date in dat:
        dates.append(date.text)



################################ Topics covered in Pranabmukherjee  #####################################
## Speech, Press ##
### Speech - speeches2017.html, speeches2017hindi.html change year accordingly ###
#### Press - pr2017.html, prhindi2017.html  change year accordingly ####
##### Years - 2012, 2013, 2014, 2015, 2016, 2017, 2018 #####
#########################################################################################################


#scrape links and dates for specified languages

page = 'prhindi2017.html'               ## 'pr2017.html'  - for english  change year accordingly 
func(page)

# lll = "http://pranabmukherjee.nic.in/sph311212.html"
# x = re.findall("sph", lll)
# if(x[0]=="sph"):
#     print("s")
# links

eng_list = []
hindi_list = []
for i in range(0,len(links)):
    dummy = links[i]
    x = re.findall("prh", dummy)
    if(len(x)==0):
        eng_list.append(links[i])
    else:
        hindi_list.append(links[i])


print(len(hindi_list),len(eng_list))
len(dates)

df=pd.DataFrame(hindi_list, columns=["link"])
df['dates'] = dates

df.to_csv('pranab_hindi.csv',encoding = 'utf-16', mode ='w', index = False)
setof = pd.read_csv('pranab_hindi.csv',encoding = 'utf-16')
setof.head()

print(len(setof['dates']))

#content scraping

contents = []
titles = []
for i in tqdm(range(0,len(setof['link']))):
    try:
        re = requests.get(setof['link'][i])
        re.encoding = 'utf-8'
        soup = BeautifulSoup(re.text, 'html.parser')

        title = soup.find('div', id = 'SpeechHeading').text

        title = title.replace("\r\n", "\n")
        title = title.replace("\n","")
        title = title.strip()
        titles.append(title)
        content = soup.find_all('div', id = 'SpeechContent')

        dd = []
        for i in content:
            dd.append(i.text)
        dd = str(dd)
        cont = dd.replace(r"\r\n", r"\o")
    #     cont = cont.replace(r"\n\o","\n")
        cont = cont.replace("\\o","")
        cont = cont.replace("\\n", "\n")
        contents.append(cont)
    except Exception as ex:
        print('page not found')
        titles.append('page not found')
        contents.append('page not found')


# print(contents[38])
# print(contents[82])
# print(titles[69])

setof['title']= titles
setof['content'] = contents

setof.to_csv('pranab_rm_content.csv', 'w', encoding = 'utf-16', index = False)
setof= setof.drop(labels = [38,82,69], axis = 0)

setof.to_csv('pranab_hindi_2017_content.csv', encoding = 'utf-16', mode='w', index = False )


fil = pd.read_csv('pranab_hindi_2017_content.csv', encoding = 'utf-16' )
# fil

# write the content to text files
 
bad_chars = [';', ':', '!', '?', '|', '"', '+', '<', '>', '.', "*",']','[']

out_dir = "pranab_hi_2017_contents"                                         ##change directory according to year chosen
file_names = []
for count in tqdm(range(0,len(fil['content']))):
    filename = ''.join(i for i in fil['title'][count] if not i in bad_chars)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(os.path.join(out_dir, f"{count}_{'_'.join(filename[:10].split())}.txt")):
        try:
            temp_name = f"{count}_{'_'.join(filename[:10].split())}.txt"
            file_names.append(temp_name)
            ddd = str(fil['content'][count])
            cont = ddd.replace("['", '')
            cont = cont.replace("']", '')
            cont = cont.replace('["','')
            cont = cont.replace('"]','')
            cont = cont.strip('\n').strip()
            #k = [i.strip().strip(',]["\'').strip() for i in ddd.split('\n')]

            with open(os.path.join(out_dir, f"{count}_{'_'.join(filename[:10].split())}.txt"), mode = 'w', encoding = 'utf-16') as file_w:
                
                for text in cont:
                    file_w.write(text )
        except Exception as ex:
            temp_name = f"{count}_{'_'.join(filename[:10].split())}.txt"
            file_names.append(temp_name)  


fil = fil.drop(columns = ['content'])
# fil.head()

fil['content'] = file_names
fil.to_csv('pranab_hi_2017_content_final.csv', mode = 'a', encoding = 'utf-16', index = False)

final = pd.read_csv('pranab_hi_2017_content_final.csv', encoding = 'utf-16')
# final.head()





