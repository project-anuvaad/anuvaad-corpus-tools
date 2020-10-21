import requests
import json
from io import StringIO

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

def download_file(token,file_id, appendList):
    url = 'https://auth.anuvaad.org/download/{}'.format(file_id)
    header = {'Authorization': 'Bearer {}'.format(token)}
    try:
        r = requests.get(url, headers=header, timeout=10)
        # print(r)
        list_lines = r.content.decode("utf-16").split("\n")
        for s in list_lines:
            appendList.append(s.replace('\r',''))
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

def extract_bitext(year,month,lang,token, output_dir,source_filepath, target_filepath,english_match,english_am,hindi_match,hindi_am):
    prev_status = ''
    src_resp = upload_document(token, source_filepath, 'file/txt')
    tgt_resp = upload_document(token, target_filepath, 'file/txt')
    if src_resp['filepath'] is not None and tgt_resp['filepath'] is not None:
            align_rsp = submit_alignment_files(token, src_resp['filepath'], 'en', tgt_resp['filepath'], 'hi')
            if align_rsp is not None and align_rsp['jobID'] is not None:
                # print('alignment jobId %s' % (align_rsp['jobID']))
                job_id = align_rsp['jobID']
                while(1):
                    status, rsp = get_alignment_result(token, align_rsp['jobID'])
                    try:
                        if(rsp[0]['status'] != prev_status):
                            prev_status = rsp[0]['status']
                            print(prev_status)
                    except:
                        print('There was an error so enterd in get_result_server_fail')
                        get_result_server_fail(year,month,job_id,lang)

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
