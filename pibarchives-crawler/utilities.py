from bs4 import BeautifulSoup
import os
from retry import retry
import urllib
import requests
import json
import time
from langdetect import detect

ENGLISH_TOKENIZER_API = 
HINDI_TOKENIZER_API   = 
DOCUMENT_UPLOAD_API   = 
DOCUMENT_DOWNLOAD_API = 
SUBMIT_ALIGNER_API    = 
GET_ALIGNER_RESULT    = 



def create_directory(path):
    try:
        os.mkdir(path)
        return True
    except FileExistsError:
        return True
    except OSError as error:
        print(error)
    return False


@retry(Exception, tries=10, delay=3, backoff=2, max_delay=40)
def get_html(open_link):
    url = urllib.request.urlopen(open_link,timeout=10)
    b_soup = BeautifulSoup(url, "html.parser", from_encoding="utf-8")
    n_pass = 1
    while b_soup == None and n_pass < 10:
        with urllib.request.urlopen(filename) as url:
            b_soup = BeautifulSoup(url, "html.parser", from_encoding="utf-8")
            print("Trying:", n_pass)
            n_pass += 1
    return b_soup


def write_sentence_list_to_file(filename, sen_l):
    """
    Writes fiven list of sentences to a given file name
    Removes double quotation if they are in odd number
    """
    with open(filename, mode="w", encoding="utf-16") as fl:
        for ln_edit1 in sen_l:
            ln_edit1 = " ".join(ln_edit1.split())
            if (ln_edit1.count('"') % 2) != 0:
                ln_edit1 = ln_edit1.replace('"', "")
            if len(ln_edit1.split()) < 4:
                continue
            ln_edit2 = " ".join(ln_edit1.split())
            fl.write(ln_edit2 + "\n")
    return None


@retry(Exception, tries=-1, delay=2, backoff=2, max_delay=40)
def api_sen_tokenizer_call(js, lang):
    '''
    Returns list of tokenized sentences
    '''
    if lang == "en":
        req = requests.post(ENGLISH_TOKENIZER_API, json=js)
    elif lang == "hi":
        req = requests.post(HINDI_TOKENIZER_API, json=js)
    else:
        print("Not valid langauge code")
        return None
    obj = json.loads(req.text)
    sentences = [
        i.strip().replace("\n", " ").replace("\r", " ")
        for l in obj["data"]
        for i in l["text"]
    ]
    return sentences


def get_file_content(filepath):
    with open(filepath,mode='r',encoding='utf-16') as fl:
        try:
            data=fl.read()
        except:
            print('error, retuning None for file:',os.path.basename(filepath), sep='\n')
            return None
    return data


def detect_non_eng(en_line):
    for line_split in en_line.split():
        
        try:
            if(detect(line_split.lower()) in ['hi','bn','gu','kn','ml','mr','ne','pa','ta','te','ur']):
                return True
            else:
                continue
        except:
            continue
    return False


def upload_document(token, filepath, fileType='file/txt'):
    data  = open(filepath, 'rb')
    try:
        r           = requests.post(url = DOCUMENT_UPLOAD_API, data = data,
                                 headers = {'Content-Type': 'text/plain'})
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
        return None
    data.close()
    obj         = json.loads(r.text)
    return obj['data']

def download_file(token, save_dir, file_id, prefix, extension='.txt'):
    url          = f'{DOCUMENT_DOWNLOAD_API}/{file_id}'
    header       = {'Authorization': 'Bearer {}'.format(token)}
    output_file = os.path.join(save_dir,'_'.join(prefix.split('_')[1:]) + extension)
    try:
        r        = requests.get(url, headers=header, timeout=10)

        with open(output_file, 'wb') as f:
            f.write(r.content)
            print('file %s, downloaded at %s' % (os.path.basename(output_file), os.path.basename(save_dir)))
    except requests.exceptions.Timeout:
        print(f'Timeout for URL: {url}')
        return
    except requests.exceptions.TooManyRedirects:
        print(f'TooManyRedirects for URL: {url}')
        return
    except requests.exceptions.RequestException as e:
        print(f'RequestException for URL: {url}')
        return
    return
    
def submit_alignment_files(token, file_id1, lang_code1, file_id2, lang_code2):
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
    header          = {
                            'Authorization': 'Bearer {}'.format(token),
                            'Content-Type': 'application/json'
                      }
    try:
        r           = requests.post(url = SUBMIT_ALIGNER_API, headers=header, data = json.dumps(body))
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
#         print (e.response.text)
        return None
#     print("Submit allignment:\n",r.text)
    return json.loads(r.text)


def get_alignment_result(token, job_id):
    url          = f'{GET_ALIGNER_RESULT}/{job_id}'
    header       = {'Authorization': 'Bearer {}'.format(token)}
    
    try:
        r        = requests.get(url, headers=header)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
        return None, None
    rsp          = json.loads(r.text)
    if rsp is not None and len(rsp) > 0:
        if rsp[0]['status'] == 'COMPLETED':
            return True, rsp
    return False, rsp

def extract_bitext(token, output_dir,source_filepath, target_filepath):
    create_directory(output_dir)
    src_resp = upload_document(token, source_filepath, 'file/txt')
    tgt_resp = upload_document(token, target_filepath, 'file/txt')
    if src_resp['filepath'] is not None and tgt_resp['filepath'] is not None:
            print(f"uploaded : {os.path.basename(source_filepath)} as upload id : {src_resp['filepath']}")
            print(f"uploaded : {os.path.basename(target_filepath)} as upload id :{tgt_resp['filepath']}")
            align_rsp = submit_alignment_files(token, src_resp['filepath'], 'en', tgt_resp['filepath'], 'hi')
            if align_rsp is not None and align_rsp['jobID'] is not None:
                print('alignment jobId %s' % (align_rsp['jobID']))
            
                while(1):
                    status, rsp = get_alignment_result(token, align_rsp['jobID'])
                    #print(rsp)
                    if status:
                        print('jobId %s, completed successfully' % (align_rsp['jobID']))
                        download_file(token, output_dir, rsp[0]['output']['almostMatch']['source'],\
                                      os.path.basename(source_filepath).split('.')[0]+'_aligned_am_src')
                        download_file(token, output_dir, rsp[0]['output']['almostMatch']['target'],\
                                      os.path.basename(target_filepath).split('.')[0]+'_aligned_am_tgt')

                        download_file(token, output_dir, rsp[0]['output']['match']['source'],\
                                      os.path.basename(source_filepath).split('.')[0]+'_aligned_m_src')
                        download_file(token, output_dir, rsp[0]['output']['match']['target'],\
                                      os.path.basename(target_filepath).split('.')[0]+'_aligned_m_tgt')
                        break
                    else:
                        if rsp:
                            print(f"jobId {align_rsp['jobID']}, Status: {rsp[0]['status']}, waiting for 10 seconds")
                        time.sleep(10)