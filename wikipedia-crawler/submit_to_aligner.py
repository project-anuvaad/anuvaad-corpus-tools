# TODO: set variables for source and target language, make directories for each respecitve source-target pair. Have just one csv file for one aligning language pair. The additional ones are just appended to the original file. Makes it easy to maintain,edit and keep track of.
# TODO: make google sheets for wikipedia scraping

import os
from pathlib import Path
import pandas as pd
from aligner_utils import upload_document,download_file,extract_bitext,get_alignment_result,submit_alignment_files
import time

def trial():
    bearerToken = 'enter your token here'

    lang = 'kn'
    b_path = os.path.join(r'C:\Users\Dhanvi\Wikipedia_Scraping','Tokenized_Files-'+lang)
    output_path = os.path.join(r'C:\Users\Dhanvi\Wikipedia_Scraping','Aligned_Files-'+lang)
    Path(output_path).mkdir(parents=True,exist_ok=True)
    count = 0
    with open('finished_ids-'+lang+'.txt','r') as f:
        finished_ids = f.read().split(',')
    count = len(finished_ids)
    for f in os.listdir(b_path):
        if('-en.txt' in f):
            source_am = []
            source_m = []
            target_am = []
            target_m = []
            id = f.split('-')[0]
            if(id in finished_ids):
                continue
            tgt_file = os.path.join(b_path,f)
            src_file = os.path.join(b_path,f.replace('en',lang))
            print('src_file',src_file)
            print('tgt_file',tgt_file)
            with open(src_file,'r',encoding='utf-16') as f_src:
                src_lines = f_src.readlines()
            with open(tgt_file,'r',encoding='utf-16') as f_tgt:
                tgt_lines = f_tgt.readlines()
            if(len(src_lines) == 0 or len(tgt_lines) == 0):
                print('Skipping because of no lines')
                print(id)
                continue
            print('Handling id',id,count)
            count += 1
            src_filepath = upload_document(bearerToken,src_file)
            tgt_filepath = upload_document(bearerToken,tgt_file)
            if(src_filepath is not None and tgt_filepath is not None):
                align_rsp = submit_alignment_files(bearerToken,src_filepath,'hi',tgt_filepath,'en')
                prev_status = ''
                if align_rsp is not None and align_rsp['jobID'] is not None:
                    job_id = align_rsp['jobID']
                    print('Current jobid is ',job_id)
                    while(1):
                        status,rsp = get_alignment_result(bearerToken,job_id)
                        if(rsp['jobs'][0]['status'] != prev_status):
                            print(rsp)
                            prev_status = rsp['jobs'][0]['status']
                            print(prev_status)
                        if status:
                            print('Job completed')
                            source_am = download_file(bearerToken,rsp['jobs'][0]['output']['almostMatch']['source'],source_am)
                            target_am = download_file(bearerToken,rsp['jobs'][0]['output']['almostMatch']['target'],target_am)
                            source_m = download_file(bearerToken,rsp['jobs'][0]['output']['match']['source'],source_m)
                            target_m = download_file(bearerToken,rsp['jobs'][0]['output']['match']['target'],target_m)
                            break
                        else:
                            time.sleep(60)

            match_list = []
            almost_match_list = []

            for i,s in enumerate(source_m):
                if(len(s.split()) > 3 or len(target_m[i].split()) > 3):
                    curr = [target_m[i],s]
                    match_list.append(curr)

            for i,s in enumerate(source_am):
                if(len(s.split())>3 or len(target_am[i].split()) > 3):
                    curr = [target_am[i],s]
                    almost_match_list.append(curr)
            header = ['en-sentence',lang+'-sentence']

            if(len(match_list) > 0):
                df_m = pd.DataFrame(match_list)
                if(os.path.exists(os.path.join(output_path,'en-'+lang+'-m.csv'))):
                    df_m.to_csv(os.path.join(output_path,'en-'+lang+'-m.csv'),header=False,index=False,mode='a',encoding='utf-16')
                else:
                    df_m.to_csv(os.path.join(output_path,'en-'+lang+'-m.csv'),header=header,index=False,mode='a',encoding='utf-16')

            if(len(almost_match_list) > 0):
                df_am = pd.DataFrame(almost_match_list)
                if(os.path.exists(os.path.join(output_path,'en-'+lang+'-am.csv'))):
                    df_am.to_csv(os.path.join(output_path,'en-'+lang+'-am.csv'),header=False,index=False,mode='a',encoding='utf-16')
                else:
                    df_am.to_csv(os.path.join(output_path,'en-'+lang+'-am.csv'),header=header,index=False,mode='a',encoding='utf-16')

            with open('finished_ids.txt','a+') as f:
                f.write(','+id)
        break

if __name__ == "__main__":
    print(doc)
