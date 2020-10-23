import os
import requests
import json
from io import StringIO
import time
import pandas as pd
from pathlib import Path

"""
--------------------------------------------------------------------------------
Upload documents to server.
Input: Authorization token (token), path of the file to be uploaded (filepath), type of the file (filetype)
Ouput: Returns the file_id of the uploaded file
--------------------------------------------------------------------------------
"""
def upload_document(token, filepath, fileType='file/txt'):
    data = open(filepath, 'rb')
    url = 'https://auth.anuvaad.org/upload'
    try:
        r = requests.post(url = url, data = data,headers = {'Content-Type': 'text/plain'})
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
        return None
    data.close()
    obj = json.loads(r.text)
    return obj['data']

"""
------------------------------------------------------------------------------------
Read the list of sentences from the processed file.
Input: Authorization token (token), file_id of the file to be downloaded (file_id), list to store all the sentences in the processed file (appendList)
Output: Returns the list of sentences in the file with id file_id
-------------------------------------------------------------------------------------
"""
def download_file(token,file_id,appendList):
    url = 'https://auth.anuvaad.org/download/{}'.format(file_id)
    header = {'Authorization': 'Bearer {}'.format(token)}
    try:
        r = requests.get(url, headers=header, timeout=10)
        list_lines = r.content.decode("utf-16").split("\n")
        for s in list_lines:
            appendList.append(s.replace('\r','')
        return appendList
    except requests.exceptions.Timeout:
        print(f'Timeout for URL: {url}')
        return
    except requests.exceptions.TooManyRedirects:
        print(f'TooManyRedirects for URL: {url}')
        return
    except requests.exceptions.RequestException as e:
        print(f'RequestException for URL: {url}')
        return

"""
--------------------------------------------------------------------------------------
Assign jobs to the aligner to align the sentences in the two files.
Input: Authorization token (token), file id of the uploaded source file (file_id1), language code of the source file (lang_code1), file id of the uploaded target file (file_id2), language code of the target file (lang_code2)
Output: Returns the job id of the assigned job
----------------------------------------------------------------------------------------
"""
def submit_alignment_files(token, file_id1, lang_code1, file_id2, lang_code2):
    url = 'https://auth.anuvaad.org/anuvaad-etl/extractor/aligner/v1/sentences/align'
    body = {
        "source": {
            "filepath": file_id1,
            "locale": lang_code1
        },
        "target": {
            "filepath": file_id2,
            "locale": lang_code2
      }
    }
    header = {'Authorization': 'Bearer {}'.format(token),'Content-Type': 'application/json'}
    try:
        r = requests.post(url = url, headers=header, data = json.dumps(body))
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
        return None
    return json.loads(r.text)
    
"""
--------------------------------------------------------------------------------------
Get the status of the assigned job
Input: Authorization token (token), job id of the interested job (job_id)
Output: Status of the job
--------------------------------------------------------------------------------------
"""
def get_alignment_result(token, job_id):
    url = 'https://auth.anuvaad.org/anuvaad-etl/extractor/aligner/v1/alignment/jobs/get/{}'.format(job_id)
    header = {'Authorization': 'Bearer {}'.format(token)}
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
        return None, None
    rsp = json.loads(r.text)
    if rsp is not None and len(rsp) > 0:
        if rsp[0]['status'] == 'COMPLETED':
            return True, rsp
    return False, rsp

"""
--------------------------------------------------------------------------------------------
Unify all the above function calls.
Input: Authorization token (token), destination directory to save the downloaded files (output_dir), path to the source file (source_filepath), path to the target file (target_filepath), list to store source match sentences (source_match), list to store source almost match sentences (source_am), list to store target match sentences (target_match), list to store target almost match sentences (target_am)
Output: List of match and almost match sentences
--------------------------------------------------------------------------------------------
"""
def extract_bitext(token, output_dir,source_filepath, target_filepath,source_match,source_am,target_match,target_am):
    prev_status = ''
    src_resp = upload_document(token, source_filepath, 'file/txt')
    tgt_resp = upload_document(token, target_filepath, 'file/txt')
    if src_resp['filepath'] is not None and tgt_resp['filepath'] is not None:
            align_rsp = submit_alignment_files(token, src_resp['filepath'], 'en', tgt_resp['filepath'], 'hi')
            if align_rsp is not None and align_rsp['jobID'] is not None:
                while(1):
                    status, rsp = get_alignment_result(token, align_rsp['jobID'])
                    if(rsp[0]['status'] != prev_status):
                        print(rsp)
                        prev_status = rsp[0]['status']
                        print(prev_status)
                    if status:
                        print('jobId %s, completed successfully' % (align_rsp['jobID']))

                        source_am=download_file(token, output_dir, rsp[0]['output']['almostMatch']['source'],os.path.basename(source_filepath).split('.')[0]+'_aligned_am_src',source_am)
                        target_am=download_file(token, output_dir, rsp[0]['output']['almostMatch']['target'],os.path.basename(target_filepath).split('.')[0]+'_aligned_am_tgt',target_am)

                        source_match=download_file(token, output_dir, rsp[0]['output']['match']['source'],os.path.basename(source_filepath).split('.')[0]+'_aligned_m_src',source_match)
                        target_match=download_file(token, output_dir, rsp[0]['output']['match']['target'],os.path.basename(target_filepath).split('.')[0]+'_aligned_m_tgt',target_match)
                        break
                    else:
                        time.sleep(10)
                return source_match,source_am,target_match,target_am

"""
--------------------------------------------------------------------------------------
Traverse through parallel files csv and assign jobs to aligner. Write total match and total almost match sentences from the given month in the specified year after the processing.
Input: month of the year (month), year (year), from which index to start reading the files (index)
Output: -
--------------------------------------------------------------------------------------
"""
def main(month,year,index):
    bearerToken = 'Enter your token here'
    
    #target language
    lang = 'Hindi'
    
    header_matches = ["File No","English_Sen","Hindi_Sen","English_Link","Hindi_Link"]
    
    base_url = "https://www.pib.gov.in/PressReleasePage.aspx?PRID="
    
    df = pd.read_csv(os.path.join(os.getcwd(),year,month,"Parallel-"+lang+".csv"))

    file_tokenized_path = os.path.join(os.getcwd(),year,month,"Tokenized-Mine-No-Constraints")
    output_dir = os.path.join(os.getcwd(),year,month,"Aligned")

    Path(output_dir).mkdir(parents=True,exist_ok=True)

    for i in range(index,len(df)):
    
        #empty lists to hold overall defined structure
        almost_match_list = []
        match_list = []
        
        #empty lists to hold match and almost match sentences for each parallel files pair
        src_match=[]
        src_am=[]
        tgt_match=[]
        tgt_am=[]
        
        src = df['English_Filename'][i]
        tgt = df[lang+'_Filename'][i]
        
        src_filename = os.path.basename(src)
        src_rid = src_filename.split('-')[0]
        
        tgt_filename = os.path.basename(tgt)
        tgt_rid = tgt_filename.split('-')[0]
        
        print('handling file with id ',i)
        print(src_filename)
        
        file_src_path = os.path.join(file_tokenized_path,src_filename)
        file_tgt_path = os.path.join(file_tokenized_path,tgt_filename)
        
        src_match,src_am,tgt_match,tgt_am=extract_bitext(bearerToken,output_dir,file_src_path,file_tgt_path,src_match,src_am,tgt_match,tgt_am)
        
        fsrc_m = open(os.path.join(output_dir,rid+'-English-Match.txt'),'w',encoding = 'utf-8')
        ftgt_m = open(os.path.join(output_dir,hrid+"-"+lang+"-Match.txt"),'w',encoding = 'utf-8')
        fsrc_am = open(os.path.join(output_dir,rid+'-English-AMatch.txt'),'w',encoding = 'utf-8')
        ftgt_am = open(os.path.join(output_dir,hrid+"-"+lang+"-AMatch.txt"),'w',encoding = 'utf-8')
        
        #for number of matched sentences
        for j,sen in enumerate(source_match):
        
            #if there are more than 4 words in either source or target and both sentences are not empty
            if(len(sen.split()) > 4 or len(target_match[j].split()) > 4 and sen.strip() != '' and target_match[j].strip() != ''):
                fsrc_m.write(sen+"\n")
                ftgt_m.write(target_match[j]+"\n")
                match_list.append([i,sen,target_match[j],base_url+rid,base_url+hrid])
        
        #for number of almost matched sentences    
        for j,sen in enumerate(source_am):
        
            if(len(sen.split()) > 4 or len(target_am[j].split()) > 4):
                fsrc_am.write(sen+"\n")
                ftgt_am.write(target_am[j]+"\n")
                almost_match_list.append([i,sen,target_am[j],base_url+rid,base_url+hrid])
        
        
        if(len(match_list) > 0):
            df_m = pd.DataFrame(match_list)
            file_name_total = os.path.join(os.getcwd(),year,month'Total-English-'+lang+'Match.csv')
            if(not os.path.exists(file_name_total)):
                df_m.to_csv(file_name_total,header=header_matches,index=False,mode='a')
            else:
                df_m.to_csv(file_name_total,header=False,index=False,mode='a')

        if(len(almost_match_list) > 0):
            df_am = pd.DataFrame(almost_match_list)
            file_name_am = os.path.join(os.getcwd(),'Total-English-'+lang+'Almost-Match.csv')
            if(not os.path.exists(file_name_am)):
                df_am.to_csv(file_name_am,header=header_matches,index=False,mode='a')
            else:
                df_am.to_csv(file_name_am,header=False,index=False,mode='a')
                
        fsrc_m.close()
        ftgt_m.close()
        fsrc_am.close()
        ftgt_am.close()


if __name__ == "__main__":
    main('August','2020',0)
