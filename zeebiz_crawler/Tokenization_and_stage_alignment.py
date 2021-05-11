# this  is only usefull when you have a data like [ date , urls , scraped txt ]  in csv file  (columns order should be same )
 

# all necessary  imports
import pandas as pd
import numpy as np
from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
import os
import re
from ast import literal_eval
from indicnlp import common
from indicnlp.tokenize import sentence_tokenize
import nltk
from nltk.tokenize import sent_tokenize
from indicnlp import common
import sys
import argparse
import requests
import csv
import pandas as pd
import urllib.request, json 





#    inputs        :
# ---------------


# start and end date represents  from which range you want to  tokenize and align
start_date='2008/01/01'
end_date='2021/04/30'

#filename1 should be non-english file (path should be ,  where you stored the scraped  csv file  using above script )
filename1='/home/test/Desktop/Anuvaad/BS/all_data/final_data/total_hindi_text_modified_date.csv'

#filename2 should be english file

filename2='/home/test/Desktop/Anuvaad/BS/all_data/final_data/BS_english_total_nondup_mod.csv'

# non english file language 
lan='hi'

# divide_by_months  represents  how many months wise you should divide the data in given  start and end date range
#(for ex  :  if we give divide_by_months=1 , then it will take 1 month data from csv file and will be tokenized ,
#  if we give divide_by_month=12 then it will take 1 year data from csv file and tokenize and align it)
divide_by_months=3


# auth token of anuvaad  of stage    should be   recent one
header_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6InN0YWdldXNlckB0YXJlbnRvLmNvbSIsInBhc3N3b3JkIjoiYickMmIkMTIkYkZ3bXRHV2ZDWjI2WXM2aVlrVU5oZUJkZTlraXNVaUJ4Lkk0WFNGdzk1SHJnbWRMcEY0VksnIiwiZXhwIjoxNjIwNzMyODIyfQ.F94cvgn_CpUhGxdY28yxcLMPTcLQSOq8tfVQszrMdTY'







def divide_dates_months_wise(start_date,end_date,divide_by_months):

    st=start_date.split('/')
    lt=end_date.split('/')
    st=[int(val) for val in st]
    lt=[int(val) for val in lt]


    start_date = datetime.date(st[0],st[1],st[2])
    end_date = datetime.date(lt[0],lt[1],lt[2])


    ls=[]
    while True:
        ls.append(start_date)
        start_date = start_date + relativedelta(months=divide_by_months)
        if end_date < start_date + relativedelta(months=0):
            break
        if start_date > end_date:
            break


    #print('start_date','end_date')

    date_rages_by_division=[]

    for i in range(len(ls)-1):
        date_rages_by_division.append((ls[i],ls[i+1]-datetime.timedelta(days=1)))
    date_rages_by_division.append((ls[-1],end_date))


    return date_rages_by_division





def tokenize_text(lan,all_data):
    full_list_sentences=[]
    for one_list in all_data:
    

        if lan!='en':    

            sentences_one=[]
            for sen in one_list:
                indic_string=sen
                sentences=sentence_tokenize.sentence_split(indic_string, lang=lan)
                for t in sentences:
                    sentences_one.append(t)
        else:

            sentences_one=[]
            for sen in one_list:
                indic_string=sen
                sentences=sent_tokenize(sen)
                for t in sentences:
                    sentences_one.append(t)
        sentences1=list(set(sentences_one))
        sentences2=[sen for sen in sentences1 if len(sen) >6 ]     
        sentences3=[sen.strip(' \t*.') for sen in sentences2]  

        full_list_sentences.append(sentences3)

    return full_list_sentences

def get_data_in_given_range(date_ranges,filename) :
    
    all_months_data=[]
    
    
    
    df=pd.read_csv(filename,header=None)
                     
    df['new_date']=None
    for num in range(len(df.iloc[:,0])):
        try:
            df['new_date'][num]= datetime.datetime.strptime(df.iloc[:,0][num], '%Y/%m/%d')
        except:
            df['new_date'][num]=np.nan

    for sub_date in date_ranges:

        d1=sub_date[0].day
        m1=sub_date[0].month
        y1=sub_date[0].year
        d2=sub_date[1].day
        m2=sub_date[1].month
        y2=sub_date[1].year
        
        value1=str(d1)+'/'+str(m1)+'/'+str(y1)
        value2=str(d2)+'/'+str(m2)+'/'+str(y2)
        
        s_date=datetime.datetime.strptime(value1, '%d/%m/%Y')
        e_date=datetime.datetime.strptime(value2, '%d/%m/%Y')
        
        
        #df['date']= [datetime.datetime.strptime(date_time_str, '%Y/%m/%d') for date_time_str in df.iloc[:,0]]

        df1=df[np.logical_and(df['new_date']>=s_date , df['new_date'] <= e_date ) ]

        print(df1)

        
        fulllst = []
        for item in df1.iloc[:,2]:
            try:
                sen = literal_eval(item)
                fulllst = fulllst + sen
            except:
                pass

        all_months_data.append(fulllst)


    return all_months_data






def alignment(text_file1,text_file2,header_token,lan):
    
    
    #declaring constant values
    upload_url = "https://stage-auth.anuvaad.org/anuvaad-api/file-uploader/v0/upload-file"
    aligner_url = "https://stage-auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/async/initiate"
    download_url = "https://stage-auth.anuvaad.org/download/"
    search_url = 'https://stage-auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/jobs/search/bulk'
    #files must be in UTF-16 Format
    file1_path =text_file1       
    source_locale =lan                       
    file2_path =text_file2

    # parameters for file upload API
    payload = {}
    file1_body = [
    ('file', open(file1_path,'rb'))
    ]
    headers =  {'auth-token':header_token }

    upload_response1 = requests.request("POST", upload_url, headers=headers, data = payload, files = file1_body)
    file1_response  = upload_response1.json()["data"]

    file2_body = [
    ('file', open(file2_path,'rb'))
    ]

    upload_response2 = requests.request("POST", upload_url, headers=headers, data = payload, files = file2_body)

    file2_response  = upload_response2.json()["data"]
    #print(file2_path , " Uploaded successfully as ", file2_response)
    
    aligner_body = {
    "workflowCode":"WF_A_AL",
    "files": [
                {
                    "locale": source_locale,
                    "path": file1_response,
                    "type": "txt"
                },
                {
                    "locale": "en",
                    "path": file2_response,
                    "type": "txt"
                }
    ]
    }

    aligner_response = requests.request("POST", aligner_url, json=aligner_body, headers=headers).json()
    #shows status
    print("aligner_response")
    #take only JOB-ID from response
    #print("Job submitted to aligner successfully, save job ID given below : ")
    return (aligner_response['jobID'])







def tokenize_data_store_into_txt_files():

    date_ranges=divide_dates_months_wise(start_date,end_date,divide_by_months)


    all_data1=get_data_in_given_range(date_ranges,filename1)

    all_sentences1=tokenize_text(lan,all_data1)


    for num in range(len(all_sentences1)):
        with open(filename1[:-4]+str(date_ranges[num][0])+str(date_ranges[num][1])+'.txt', 'w',encoding='utf-16') as file_handler:
            for item in all_sentences1[num]:
                file_handler.write("{}\n".format(item))



    all_data2=get_data_in_given_range(date_ranges,filename2)

    all_sentences2=tokenize_text('en',all_data2)




    for num in range(len(all_sentences2)):
        with open(filename2[:-4]+str(date_ranges[num][0])+str(date_ranges[num][1])+'.txt', 'w',encoding='utf-16') as file_handler:
            for item in all_sentences2[num]:
                file_handler.write("{}\n".format(item))

                
                
                
def remove_duplicate_lines_from_txt_files():
    for num in range(len(date_ranges)):
    text_file1=filename1[:-4]+str(date_ranges[num][0])+str(date_ranges[num][1])+'.txt'
    text_file2=filename2[:-4]+str(date_ranges[num][0])+str(date_ranges[num][1])+'.txt'
    
    f=open(text_file1,encoding='utf-16')
    all_text=f.readlines()
    print(len(all_text))
    all_unique_text=list(set(all_text))
    print(len(all_unique_text))
    f.close()
    
    with open(text_file1, 'w',encoding='utf-16') as file_handler:
        for item in all_unique_text:
            file_handler.write("{}".format(item))

    
    
    f=open(text_file2,encoding='utf-16')
    all_text=f.readlines()
    print(len(all_text))
    all_unique_text=list(set(all_text))
    print(len(all_unique_text))
    f.close()
    with open(text_file2, 'w',encoding='utf-16') as file_handler:
        for item in all_unique_text:
            file_handler.write("{}".format(item))

def alignment_starts():

    job_ids_info=[]
    job_ids_num=[]

    en_sen_count=[]
    non_en_sen_count=[]

    for num in range(35,54):
        text_file1=filename1[:-4]+str(date_ranges[num][0])+str(date_ranges[num][1])+'.txt'
        text_file2=filename2[:-4]+str(date_ranges[num][0])+str(date_ranges[num][1])+'.txt'



        #print(text_file1,text_file2)
        jobid=alignment(text_file1,text_file2,header_token,lan)
        print('the given date_range of'+ str(date_ranges[num][0])+'  to  '+str(date_ranges[num][1])+' job ID is :   '+   str(jobid))
        job_ids_info.append('the given date_range of'+ str(date_ranges[num][0])+'  to  '+str(date_ranges[num][1])+' job ID is :   ')

        job_ids_num.append(jobid)


        file = open(text_file1,"r",encoding='utf-16')
        Counter = 0
        Content = file.read()
        CoList = Content.split("\n")
        for i in CoList:
            if i:
                Counter += 1         
        #print("This is the number of lines in the file")
        non_en_sen_count.append(Counter)
        file.close()



        file = open(text_file2,"r",encoding='utf-16')
        Counter = 0
        Content = file.read()
        CoList = Content.split("\n")
        for i in CoList:
            if i:
                Counter += 1         
        #print("This is the number of lines in the file")
        en_sen_count.append(Counter)
        file.close()




    df=pd.DataFrame()
    df['info ']=job_ids_info
    df['job id']=job_ids_num
    df['non_en_sen_count']=non_en_sen_count
    df['en_sen_count']=en_sen_count
    df.to_csv('ZEEBIZ_jobids.csv',index=None)  


    
if __name__=='__main__':
    
    tokenize_data_store_into_txt_files()
    remove_duplicate_lines_from_txt_files()
    
    # if you want only tokenization you can comment the below line
    alignment_starts()
    
    
