import os
import pandas as pd
import requests
import json
import glob
import time
from retry import retry


@retry(Exception, tries=-1, delay=2, backoff=2, max_delay=40)
def get_sen_token(js, lang):
    url_en = "https://auth.anuvaad.org/tokenize-sentence"
    url_hi = "https://auth.anuvaad.org/tokenize-hindi-sentence"
    #     url_en='https://auth.anuvaad.org/v2/tokenize-sentence'
    #     url_hi='https://auth.anuvaad.org/v2/tokenize-sentence'
    if lang == "en":
        req = requests.post(url_en, json=js)
    elif lang == "hi":
        req = requests.post(url_hi, json=js)
    else:
        print("Not valid langauge code")
        return None
    obj = json.loads(req.text)
    # print(obj)
    sentences = [
        i.strip().replace("\n", " ").replace("\r", " ")
        for l in obj["data"]
        for i in l["text"]
    ]
    #     sentences_2=[' '.join(i.split()) for i in sentences]
    return sentences


def write_tok_file(filename, sen_l, lang):
    with open(filename, mode="w", encoding="utf-16") as fl:
        # count=0
        for l in sen_l:
            l = " ".join(l.split())
            if (l.count('"') % 2) != 0:
                # print(l)
                l = l.replace('"', "")
                # print(l)
            if len(l.split()) < 4:
                continue
            l2 = " ".join(l.split())
            fl.write(l2 + "\n")
            # count+=1
    return None


def upload_document(token, filepath, fileType="file/txt"):
    data = open(filepath, "rb")
    print(f"Uploading: {os.path.basename(filepath)}")
    data_file = [("file", data)]
    url = "https://auth.anuvaad.org/anuvaad-api/file-uploader/v0/upload-file"
    try:
        r = requests.post(url=url, files=data_file, headers={"auth-token": token})
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
        return None
    #     print("response:\n",r.text)
    data.close()
    obj = json.loads(r.text)
    #     print(obj)
    return obj["data"]


@retry(Exception, tries=-1, delay=2, backoff=2, max_delay=40)
def download_file(token, save_dir, file_id, prefix, extension=".txt"):
    url = "https://auth.anuvaad.org/download/{}".format(file_id)
    header = {"auth-token": token}
    output_file = os.path.join(
        save_dir, "000_" + "_".join(prefix.split("_")[1:]) + extension
    )
    while True:
        try:
            r = requests.get(url, headers=header, timeout=10)
            with open(output_file, "wb") as f:
                f.write(r.content)
            if os.path.exists(output_file):
                print(
                    "file %s, downloaded at %s"
                    % (os.path.basename(output_file), os.path.basename(save_dir))
                )
                return
        except requests.exceptions.Timeout:
            print(f"Timeout for URL: {url}")
        except requests.exceptions.TooManyRedirects:
            print(f"TooManyRedirects for URL: {url}")
        except requests.exceptions.RequestException as e:
            print(f"RequestException for URL: {url}")
        time.sleep(2)
    return


def submit_alignment_files(token, file_id1, lang_code1, file_id2, lang_code2):
    url = "https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/async/initiate"
    body = {
        "workflowCode": "WF_A_AL",
        "files": [
            {"locale": str(lang_code1), "path": str(file_id1), "type": "txt"},
            {"locale": str(lang_code2), "path": str(file_id2), "type": "txt"},
        ],
    }
    #     print(json.dumps(body))
    header = {"auth-token": token, "Content-Type": "application/json"}
    try:
        r = requests.post(url=url, headers=header, data=json.dumps(body))
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        #         print (e.response.text)
        return None
    #     print("Submit allignment:\n",r.text)
    return json.loads(r.text)


@retry(Exception, tries=-1, delay=2, backoff=2, max_delay=40)
def get_alignment_result(token, job_id):
    url = "https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/jobs/search/bulk"
    # print(url)
    body = {"jobIDs": [job_id], "taskDetails": "true"}
    header = {"auth-token": token, "Content-Type": "application/json"}
    try:
        r = requests.post(url=url, headers=header, data=json.dumps(body))
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
        return None, None
    rsp = json.loads(r.text)
    if rsp is not None and len(rsp) > 0:
        if rsp["jobs"][0]["status"] == "COMPLETED":
            return True, rsp
        elif rsp["jobs"][0]["status"] == "FAILED":
            return True, rsp
        elif rsp["jobs"][0]["status"] == "INPROGRESS":
            return True, rsp
    return False, rsp


def extract_bitext(
    token,
    output_dir,
    source_filepath,
    target_filepath,
    jobid,
    source_lang_code="hi",
    break_progress=True,
):
    rerun = True
    while rerun:
        if len(jobid) == 0:
            src_resp = upload_document(token, source_filepath, "file/txt")
            tgt_resp = upload_document(token, target_filepath, "file/txt")
            if src_resp is not None and tgt_resp is not None:
                print(
                    f"uploaded source: {os.path.basename(source_filepath)} as upload id : {src_resp}"
                )
                print(
                    f"uploaded target: {os.path.basename(target_filepath)} as upload id :{tgt_resp}"
                )
                align_rsp = submit_alignment_files(
                    token, src_resp, source_lang_code, tgt_resp, "en"
                )
                #                 print(align_rsp)
                if align_rsp is not None and align_rsp["jobID"] is not None:
                    print("alignment jobId %s" % (align_rsp["jobID"]))

                    while 1:
                        status, rsp = get_alignment_result(token, align_rsp["jobID"])
                        # print(rsp)
                        if status and rsp["jobs"][0]["status"] == "COMPLETED":
                            print(
                                "jobId %s, completed successfully"
                                % (align_rsp["jobID"])
                            )
                            download_file(
                                token,
                                output_dir,
                                rsp["jobs"][0]["output"]["almostMatch"]["source"],
                                os.path.basename(source_filepath).split(".")[0]
                                + "_aligned_am_src",
                            )
                            download_file(
                                token,
                                output_dir,
                                rsp["jobs"][0]["output"]["almostMatch"]["target"],
                                os.path.basename(target_filepath).split(".")[0]
                                + "_aligned_am_tgt",
                            )

                            download_file(
                                token,
                                output_dir,
                                rsp["jobs"][0]["output"]["match"]["source"],
                                os.path.basename(source_filepath).split(".")[0]
                                + "_aligned_m_src",
                            )
                            download_file(
                                token,
                                output_dir,
                                rsp["jobs"][0]["output"]["match"]["target"],
                                os.path.basename(target_filepath).split(".")[0]
                                + "_aligned_m_tgt",
                            )
                            rerun = False
                            break
                        elif status and rsp["jobs"][0]["status"] == "FAILED":
                            break
                        elif (
                            status
                            and rsp["jobs"][0]["status"] == "INPROGRESS"
                            and break_progress
                        ):
                            print(
                                f"jobId {jobid} for file ID {os.path.basename(source_filepath).split('.')[0]}, Status: {rsp['jobs'][0]['status']}"
                            )
                            rerun = False
                            break
                        elif rsp:
                            print(
                                f"jobId {align_rsp['jobID']} for file ID {os.path.basename(source_filepath).split('.')[0]}, Status: {rsp['jobs'][0]['status']}, waiting for 10 seconds"
                            )
                        time.sleep(10)
        else:
            while 1:
                status, rsp = get_alignment_result(token, jobid)
                # print(rsp)
                if status and rsp["jobs"][0]["status"] == "COMPLETED":
                    print("jobId %s, completed successfully" % (jobid))
                    download_file(
                        token,
                        output_dir,
                        rsp["jobs"][0]["output"]["almostMatch"]["source"],
                        os.path.basename(source_filepath).split(".")[0]
                        + "_aligned_am_src",
                    )
                    download_file(
                        token,
                        output_dir,
                        rsp["jobs"][0]["output"]["almostMatch"]["target"],
                        os.path.basename(target_filepath).split(".")[0]
                        + "_aligned_am_tgt",
                    )

                    download_file(
                        token,
                        output_dir,
                        rsp["jobs"][0]["output"]["match"]["source"],
                        os.path.basename(source_filepath).split(".")[0]
                        + "_aligned_m_src",
                    )
                    download_file(
                        token,
                        output_dir,
                        rsp["jobs"][0]["output"]["match"]["target"],
                        os.path.basename(target_filepath).split(".")[0]
                        + "_aligned_m_tgt",
                    )
                    rerun = False
                    break
                elif status and rsp["jobs"][0]["status"] == "FAILED":
                    break
                elif (
                    status
                    and rsp["jobs"][0]["status"] == "INPROGRESS"
                    and break_progress
                ):
                    print(
                        f"jobId {jobid} for file ID {os.path.basename(source_filepath).split('.')[0]}, Status: {rsp['jobs'][0]['status']}"
                    )
                    rerun = False
                    break
                elif rsp:
                    print(
                        f"jobId {jobid} for file ID {os.path.basename(source_filepath).split('.')[0]}, Status: {rsp['jobs'][0]['status']}, waiting for 10 seconds"
                    )
                time.sleep(10)

    return
