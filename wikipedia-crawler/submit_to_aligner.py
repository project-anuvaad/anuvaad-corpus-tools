import os
from pathlib import Path
import pandas as pd
from aligner_utils import upload_document,download_file,extract_bitext,get_alignment_result,submit_alignment_files
import time

bearerToken = 'Enter your token here'

lang = 'hi'
b_path = os.path.join(os.getcwd(),'Tokenized_Files')
output_path = os.path.join(os.getcwd(),'Aligned_Files')
Path(output_path).mkdir(parents=True,exist_ok=True)
count = 0
finished_ids = []
if(os.path.exists('finished_ids.txt')):
    with open('finished_ids.txt','r') as f:
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
        src_file = os.path.join(b_path,f)
        tgt_file = os.path.join(b_path,id+'-'+lang+'.txt')
        with open(src_file,'r',encoding='utf-16') as f_src:
            src_lines = f_src.readlines()
        with open(tgt_file,'r',encoding='utf-16') as f_tgt:
            tgt_lines = f_tgt.readlines()
        if(len(src_lines) == 0 or len(tgt_lines) == 0):
            continue
        print('Handling id',id,count)
        count += 1
        src_resp = upload_document(bearerToken,src_file)
        tgt_resp = upload_document(bearerToken,tgt_file)
        if(src_resp['filepath'] is not None and tgt_resp['filepath'] is not None):
            align_rsp = submit_alignment_files(bearerToken,src_resp['filepath'],'en',tgt_resp['filepath'],'hi')
            prev_status = ''
            if align_rsp is not None and align_rsp['jobID'] is not None:
                job_id = align_rsp['jobID']
                print('Current jobid is ',job_id)
                while(1):
                    status,rsp = get_alignment_result(bearerToken,job_id)
                    if(rsp[0]['status'] != prev_status):
                        print(rsp)
                        prev_status = rsp[0]['status']
                        print(prev_status)
                    if status:
                        print('Job completed')
                        source_am = download_file(bearerToken,rsp[0]['output']['almostMatch']['source'],source_am)
                        target_am = download_file(bearerToken,rsp[0]['output']['almostMatch']['target'],target_am)
                        source_m = download_file(bearerToken,rsp[0]['output']['match']['source'],source_m)
                        target_m = download_file(bearerToken,rsp[0]['output']['match']['target'],target_m)
                        break
                    else:
                        time.sleep(20)

        match_list = []
        almost_match_list = []

        for i,s in enumerate(source_m):
            if(len(s.split()) > 3 or len(target_m[i].split()) > 3):
                curr = [s,target_m[i]]
                match_list.append(curr)

        for i,s in enumerate(source_am):
            if(len(s.split())>3 or len(target_am[i].split()) > 3):
                curr = [s,target_am[i]]
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
