#file contains code to process newsonair scraped CSV to get tokenized sentences in a TXT file

import pandas as pd
from ast import literal_eval
from indicnlp.tokenize import sentence_tokenize
from nltk.tokenize import sent_tokenize 


ENG_CSV = "/home/eng_csv.csv"
HIN_CSV = "/home/hin_csv.csv"
ENG_TXT = "/home/eng_txt.txt"
HIN_TXT = "/home/hin_txt.txt"


hi_df = pd.read_csv(HIN_CSV)
lst = hi_df['data'].to_list()

#iterate through items in list and get paragraphs
fulllst = []
for item in lst:
    sen = literal_eval(item)
    fulllst = fulllst + sen


#tokenizing scraped hindi paragraphs using indic NLP
with open(HIN_TXT, "w" , encoding="utf-16") as fobj:
    for x in fulllst:
        sentences=sentence_tokenize.sentence_split(x, lang='hi')
        for t in sentences:
            fobj.write(t + "\n")

#iterate through items in list and get paragraphs
en_df = pd.read_csv(ENG_CSV)
lst = en_df['data'].to_list()
fulllst = []
for item in lst:
    sen = literal_eval(item)
    fulllst = fulllst + sen

#tokenizing scraped English sentences using NLTK
with open(ENG_TXT, "w" , encoding="utf-16") as fobj:
    for x in fulllst:
        sentences=sent_tokenize(x) 
        for sen in sentences:
            fobj.write(sen + "\n")

#the two output txt files could be aligned to obtain parallel dataset