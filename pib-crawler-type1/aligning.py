import os
import requests
import json
from io import StringIO
import time
import pandas as pd
from pathlib import Path

def upload_document(token, filepath, fileType='file/txt'):
    data = open(filepath, 'rb')
    url = 'https://auth.anuvaad.org/upload'
    try:
        r = requests.post(url = url, data = data,headers = {'Content-Type': 'text/plain'})
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
        return None
    # print("upload:\n",r.text)
    data.close()
    obj = json.loads(r.text)
    # print(obj['data'])
    return obj['data']

def download_file(token, save_dir, file_id, prefix, appendList,extension='.txt'):
    url = 'https://auth.anuvaad.org/download/{}'.format(file_id)
    header = {'Authorization': 'Bearer {}'.format(token)}
    try:
        r = requests.get(url, headers=header, timeout=10)
        # print(r)
        list_lines = r.content.decode("utf-16").split("\n")
        for s in list_lines:
            appendList.append(s.replace('\r','')
            # print('file %s, downloaded at %s' % (file_id, save_dir))
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
    # print("Submit allignment:\n",r.text)
    return json.loads(r.text)

def get_alignment_result(token, job_id):
    url = 'https://auth.anuvaad.org/anuvaad-etl/extractor/aligner/v1/alignment/jobs/get/{}'.format(job_id)
    #print(url)
    header = {'Authorization': 'Bearer {}'.format(token)}
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
        return None, None
    rsp = json.loads(r.text)
    # print(rsp)
    if rsp is not None and len(rsp) > 0:
        if rsp[0]['status'] == 'COMPLETED':
            return True, rsp
    return False, rsp

def extract_bitext(token, output_dir,source_filepath, target_filepath,english_match,english_am,hindi_match,hindi_am):
    prev_status = ''
    src_resp = upload_document(token, source_filepath, 'file/txt')
    tgt_resp = upload_document(token, target_filepath, 'file/txt')
    if src_resp['filepath'] is not None and tgt_resp['filepath'] is not None:
            align_rsp = submit_alignment_files(token, src_resp['filepath'], 'en', tgt_resp['filepath'], 'hi')
            if align_rsp is not None and align_rsp['jobID'] is not None:
                # print('alignment jobId %s' % (align_rsp['jobID']))
                while(1):
                    status, rsp = get_alignment_result(token, align_rsp['jobID'])
                    if(rsp[0]['status'] != prev_status):
                        print(rsp)
                        prev_status = rsp[0]['status']
                        print(prev_status)
                    if status:
                        print('jobId %s, completed successfully' % (align_rsp['jobID']))

                        english_am=download_file(token, output_dir, rsp[0]['output']['almostMatch']['source'],os.path.basename(source_filepath).split('.')[0]+'_aligned_am_src',english_am)
                        hindi_am=download_file(token, output_dir, rsp[0]['output']['almostMatch']['target'],os.path.basename(target_filepath).split('.')[0]+'_aligned_am_tgt',hindi_am)

                        english_match=download_file(token, output_dir, rsp[0]['output']['match']['source'],os.path.basename(source_filepath).split('.')[0]+'_aligned_m_src',english_match)
                        hindi_match=download_file(token, output_dir, rsp[0]['output']['match']['target'],os.path.basename(target_filepath).split('.')[0]+'_aligned_m_tgt',hindi_match)
                        break
                    else:
                        # print('jobId %s, still running, waiting for 10 seconds' % (align_rsp['jobID']))
                        time.sleep(10)
                return english_match,english_am,hindi_match,hindi_am

def main(month,year,index):
    bearerToken = 'Enter your token here'

    almost_match_list = []
    match_list = []
    
    lang = 'Hindi'

    src_match=[]
    src_am=[]
    tgt_match=[]
    tgt_am=[]
    
    header_matches = ["File No","English_Sen","Hindi_Sen","English_Link","Hindi_Link"]
    
    base_url = "https://www.pib.gov.in/PressReleasePage.aspx?PRID="
    
    df = pd.read_csv(os.path.join(os.getcwd(),year,month,"Parallel-"+lang+".csv"))

    file_tokenized_path = os.path.join(os.getcwd(),year,month,"Tokenized-Mine-No-Constraints")
    output_dir = os.path.join(os.getcwd(),year,month,"Aligned")

    Path(output_dir).mkdir(parents=True,exist_ok=True)

    for i in range(index,len(df)):
        src = df['English_Filename'][i]
        tgt = df[lang+'_Filename'][i]
        src_filename = os.path.basename(src)
        src_rid = src_filename.split('-')[0]
        tgt_filename = os.path.basename(tgt)
        tgt_rid = tgt_filename.split('-')[0]
        print('handling file with id ',i)
        print(src_filename)
        file_src_path = file_tokenized_path+src_filename
        file_tgt_path = file_tokenized_path+tgt_filename
        src_match,src_am,tgt_match,tgt_am=extract_bitext(bearerToken,output_dir,file_src_path,file_tgt_path,src_match,src_am,tgt_match,tgt_am)
        fsrc_m = open(os.path.join(output_dir,rid+'-English-Match.txt'),'w',encoding = 'utf-8')
        ftgt_m = open(os.path.join(output_dir,hrid+"-"+lang+"-Match.txt"),'w',encoding = 'utf-8')
        fsrc_am = open(os.path.join(output_dir,rid+'-English-AMatch.txt'),'w',encoding = 'utf-8')
        ftgt_am = open(os.path.join(output_dir,hrid+"-"+lang+"-AMatch.txt"),'w',encoding = 'utf-8')
        for j,sen in enumerate(english_match):
            if(len(sen.split()) > 4 or len(hindi_match[j].split()) > 4 and sen.strip() != '' and hindi_match[j].strip() != ''):
                fsrc_m.write(sen+"\n")
                ftgt_m.write(hindi_match[j]+"\n")
                match_list.append([i,sen,hindi_match[j],base_url+rid,base_url+hrid])
        for j,sen in enumerate(english_am):
            if(len(sen.split()) > 4 or len(hindi_am[j].split()) > 4):
                fsrc_am.write(sen+"\n")
                ftgt_am.write(hindi_am[j]+"\n")
                almost_match_list.append([i,sen,hindi_am[j],base_url+rid,base_url+hrid])

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

        english_match = []
        english_am = []
        hindi_match = []
        hindi_am = []
        match_list = []
        almost_match_list = []
        fsrc_m.close()
        ftgt_m.close()
        fsrc_am.close()
        ftgt_am.close()


if __name__ == "__main__":
    main('August','2020',0)
