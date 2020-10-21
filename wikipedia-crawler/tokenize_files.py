# TODO: Try writing tokenization logic for the required languages in terms of the categories they belong to. English,Indo-Aryan and Dravidian languages. Tokenize them based on these logic and store the tokenized files in a separte directory
import os
from pathlib import Path
import pandas as pd
from tokenize_utils import tokenize_eng_file, tokenize_hi_file

b_path = os.path.join(r'C:\Users\Dhanvi\Wikipedia_Scraping','Scraped_Files')
output_path = os.path.join(r'C:\Users\Dhanvi\Wikipedia_Scraping', 'Tokenized_Files')
Path(output_path).mkdir(parents=True,exist_ok=True)

lang = 'hi'
eng_sentences = []
lang_sentences = []

for f in os.listdir(b_path):
    if('-en.txt' in f):
        id = f.split('-')[0]
        if(id+'-'+lang+'.txt' not in os.listdir(b_path)):
            continue
        src_file = os.path.join(b_path,f)
        tgt_file = os.path.join(b_path,id+'-'+lang+'.txt')
        finsrc = open(src_file,'r',encoding='utf-16')
        fintgt = open(tgt_file,'r',encoding='utf-16')
        sent_src = tokenize_eng_file(finsrc.read())
        sent_tgt = tokenize_hi_file(fintgt.read())
        finsrc.close()
        fintgt.close()
        foutsrc = open(os.path.join(output_path,f),'w',encoding='utf-16')
        fouttgt = open(os.path.join(output_path,id+'-'+lang+'.txt'),'w',encoding='utf-16')
        for s in sent_src:
            if(s.strip() == '' or 'Posted On:' in s or 'by PIB' in s):
                continue
            else:
                s = s.replace('"','')
                eng_sentences.append(s)
                foutsrc.write(s+'\n')
        for s in sent_tgt:
            if(s.strip() == '' or 'Posted On:' in s or 'by PIB' in s):
                continue
            else:
                s = s.replace('"','')
                lang_sentences.append(s)
                fouttgt.write(s+'\n')
        foutsrc.close()
        fouttgt.close()

df = pd.DataFrame(eng_sentences)
df = df.drop_duplicates()
df.to_csv('Total-en-Sentences.csv',header=['en-Sentences'],index=False,mode='a')

df = pd.DataFrame(lang_sentences)
df = df.drop_duplicates()
df.to_csv('Total-'+lang+'-Sentences.csv',header=[lang+'-Sentences'],index=False,mode='a')
