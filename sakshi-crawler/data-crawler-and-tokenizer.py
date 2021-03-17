import requests
from bs4 import BeautifulSoup
import pandas 
from urllib.request import urlopen
from indicnlp import common
from indicnlp.tokenize import sentence_tokenize
import nltk
from nltk.tokenize import sent_tokenize
from indicnlp import common
from indicnlp.tokenize import sentence_tokenize


#inputs 

lan='hi'  
# mention the csv file which are having urls of sakshi 
file_name='/home/test/Desktop/Anuvaad/sakshi/dec_2020/sakshi_dec2020_hin.csv'
#name of output text file
output_file='text.txt'


def get_data():

    news_article=[]

    df=pd.read_csv(file_name,encoding='utf-16')
    data_list=list(df.iloc[:,0])
    for url_link in data_list:
        try :
            url = urlopen(url_link)
            content = url.read()

            soup = BeautifulSoup(content, 'lxml')


            table = soup.findAll('div',attrs={"class":"region region-content"})

            for x in table:
                f=x.find_all('p')

            for j in f:  
                text=j.text.replace('\n',' ')
                news_article.append(text)
        except :
            pass

    return  news_article


total_data=get_data()


# totkenization of the data 

if lan!='en':
    sentences_one=[]
    for sen in total_data:
        indic_string=sen

        sentences=sentence_tokenize.sentence_split(indic_string, lang=lan)
        for t in sentences:
            sentences_one.append(t)

else :
    sentences_one=[]
    for sen in total_data:
        indic_string=sen
        sentences=sent_tokenize(sen)

        # print the sentences
        for t in sentences:
            sentences_one.append(t)

sentences_one=list(set(sentences_one))
sentences1=[sen for sen in sentences_one if len ( sen )> 8]
sentences2=[sen.strip(' .*') for sen in sentences1]


with open(output_file, 'w',encoding='utf-16') as file_handler:
    for item in sentences2:
        file_handler.write("{}\n".format(item))

