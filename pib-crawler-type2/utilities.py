from bs4 import BeautifulSoup
import os
import pandas as pd
from retry import retry
import urllib
import requests
import json
import time
import re
from langdetect import detect

ENGLISH_TOKENIZER_API = ""
HINDI_TOKENIZER_API = ""
DOCUMENT_UPLOAD_API = ""
DOCUMENT_DOWNLOAD_API = ""
SUBMIT_ALIGNER_API = ""
GET_ALIGNER_RESULT = ""


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
def get_html(open_link, parser="html.parser"):
    url = urllib.request.urlopen(open_link, timeout=10)
    b_soup = BeautifulSoup(url, parser, from_encoding="utf-8")
    n_pass = 1
    while (b_soup is None) and n_pass < 10:
        with urllib.request.urlopen(open_link) as url:
            b_soup = BeautifulSoup(url, parser, from_encoding="utf-8")
            time.sleep(1)
            n_pass += 1
    return b_soup


def write_scrape_text_file(file_name, w_text, ministry_name):
    with open(file_name, mode="w", encoding="utf-16") as file_w:
        file_w.write(ministry_name.strip() + "\n")
        for line in w_text:
            for ln in line.split("\n"):
                if len(ln.strip()) > 0:
                    if ln.strip().startswith("Posted On:"):
                        continue
                    if ln.strip().endswith("by PIB Delhi"):
                        continue
                    file_w.write(ln.strip().replace("\r", "") + "\n")


def prep_data(parse_url_en, ministry_list, language, log_file_write):
    log_file_write.write(f"\nPreparing {language} dataframe.")
    df1_data = pd.DataFrame(columns=["Ministry", "Posting_Date", "Link"])
    parse_main_en = parse_url_en.find("div", {"class": "content-area"})
    no_index = 0
    for i in range(len(parse_main_en.contents) - 2):
        ministry_name = (
            " ".join(str((parse_main_en.contents[i + 1].li.h3.string)).strip().split())
        ).strip('"')
        if ministry_name not in ministry_list[language + "_Ministry_Name"].unique():
            log_file_write.write(
                f"\nThis ministry name is missing in ministry list csv file: {ministry_name}"
            )
        for k in parse_main_en.contents[i + 1].li.ul.findAll("li"):
            df1_data.loc[no_index] = [
                ministry_name,
                str(k.span.string).split(":").pop().strip(),
                str(k.a["href"]).strip(),
            ]
            no_index = no_index + 1
    df1_data = pd.merge(
        df1_data,
        ministry_list,
        left_on=["Ministry"],
        right_on=[language + "_Ministry_Name"],
        how="inner",
    )
    df1_data.drop(["Ministry"], inplace=True, axis=1)
    df1_data["Posting_Date"] = pd.to_datetime(df1_data["Posting_Date"])
    df1_data.reset_index(drop=True, inplace=True)
    df1_data["Posting_Datetime"] = [None] * df1_data.shape[0]
    for i in range(df1_data.shape[0]):
        x = get_html(df1_data.at[i, "Link"])
        look_in = [
            div
            for div in x.findAll("div", attrs={"class": True})
            if "ReleaseDateSubHead" in div["class"][0]
        ]
        if len(look_in) > 0:
            div = look_in[0]
            if re.search("[0-9]{2}?.+(AM|PM)", str(div.get_text())):
                df1_data.at[i, "Posting_Datetime"] = re.search(
                    "[0-9]{2}?.+(AM|PM)", str(div.get_text())
                ).group(0)
            else:
                df1_data.at[i, "Posting_Datetime"] = df1_data.at[
                    i, "Posting_Date"
                ].strftime("%Y-%m-%d")
        else:
            log_file_write.write(
                f"\nCould not find release date tag for entry number {i+1}.\nlink returned this:\n {x}"
            )

    df1_data["Posting_Datetime"] = pd.to_datetime(df1_data["Posting_Datetime"])
    df1_data.reset_index(drop=True, inplace=True)
    df1_data.reset_index(inplace=True)
    df1_data["PRID"] = df1_data["Link"].apply(lambda x: x.split("=")[-1])
    log_file_write.write(f"\n{language} dataframe complete.")
    return df1_data


def get_data(
    n_month,
    n_year,
    filename_url,
    ministry_pa_list,
    lang,
    log_file_write,
    import_data=False,
    import_data_dir="",
):
    if lang == "hi":
        language = "Hindi"
    elif lang == "en":
        language = "English"
    if import_data:
        try:
            df_data = pd.read_csv(
                import_data_dir
                + "//"
                + language
                + "_data_"
                + n_month
                + "_"
                + n_year
                + ".csv",
                encoding="utf-16",
            )
        except:
            log_file_write.write(f"\nTrying UTF-8 Encoding")
            df_data = pd.read_csv(
                import_data_dir
                + "//"
                + language
                + "_data_"
                + n_month
                + "_"
                + n_year
                + ".csv",
                encoding="utf-8",
            )
    else:
        df_data = prep_data(
            get_html(filename_url), ministry_pa_list, language, log_file_write
        )
    df_data["Posting_Date"] = pd.to_datetime(df_data["Posting_Date"])
    df_data["Posting_Datetime"] = pd.to_datetime(df_data["Posting_Datetime"])
    return df_data


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
    """
    Returns list of tokenized sentences
    """
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
    with open(filepath, mode="r", encoding="utf-16") as fl:
        try:
            data = fl.read()
        except:
            print(
                "error, retuning None for file:", os.path.basename(filepath), sep="\n"
            )
            return None
    return data


def detect_non_eng(en_line):
    for line_split in en_line.split():

        try:
            if detect(line_split.lower()) in [
                "hi",
                "bn",
                "gu",
                "kn",
                "ml",
                "mr",
                "ne",
                "pa",
                "ta",
                "te",
                "ur",
            ]:
                return True
            else:
                continue
        except:
            continue
    return False


def upload_document(token, filepath, filetype="file/txt"):
    data = open(filepath, "rb")
    try:
        r = requests.post(
            url=DOCUMENT_UPLOAD_API, data=data, headers={"Content-Type": "text/plain"}
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
        return None
    data.close()
    obj = json.loads(r.text)
    return obj["data"]


def download_file(token, save_dir, file_id, prefix, extension=".txt"):
    url = f"{DOCUMENT_DOWNLOAD_API}/{file_id}"
    header = {"Authorization": "Bearer {}".format(token)}
    output_file = os.path.join(save_dir, "_".join(prefix.split("_")[1:]) + extension)
    try:
        r = requests.get(url, headers=header, timeout=10)

        with open(output_file, "wb") as f:
            f.write(r.content)
            print(
                "file %s, downloaded at %s"
                % (os.path.basename(output_file), os.path.basename(save_dir))
            )
    except requests.exceptions.Timeout:
        print(f"Timeout for URL: {url}")
        return
    except requests.exceptions.TooManyRedirects:
        print(f"TooManyRedirects for URL: {url}")
        return
    except requests.exceptions.RequestException:
        print(f"RequestException for URL: {url}")
        return
    return


def submit_alignment_files(token, file_id1, lang_code1, file_id2, lang_code2):
    body = {
        "source": {"filepath": file_id1, "locale": lang_code1},
        "target": {"filepath": file_id2, "locale": lang_code2},
    }
    header = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }
    try:
        r = requests.post(url=SUBMIT_ALIGNER_API, headers=header, data=json.dumps(body))
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    return json.loads(r.text)


def get_alignment_result(token, job_id):
    url = f"{GET_ALIGNER_RESULT}/{job_id}"
    header = {"Authorization": "Bearer {}".format(token)}

    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
        return None, None
    rsp = json.loads(r.text)
    if rsp is not None and len(rsp) > 0:
        if rsp[0]["status"] == "COMPLETED":
            return True, rsp
    return False, rsp


def extract_bitext(token, output_dir, source_filepath, target_filepath):
    create_directory(output_dir)
    src_resp = upload_document(token, source_filepath, "file/txt")
    tgt_resp = upload_document(token, target_filepath, "file/txt")
    if src_resp["filepath"] is not None and tgt_resp["filepath"] is not None:
        print(
            f"uploaded : {os.path.basename(source_filepath)} as upload id : {src_resp['filepath']}"
        )
        print(
            f"uploaded : {os.path.basename(target_filepath)} as upload id :{tgt_resp['filepath']}"
        )
        align_rsp = submit_alignment_files(
            token, src_resp["filepath"], "en", tgt_resp["filepath"], "hi"
        )
        if align_rsp is not None and align_rsp["jobID"] is not None:
            print("alignment jobId %s" % (align_rsp["jobID"]))

            while 1:
                status, rsp = get_alignment_result(token, align_rsp["jobID"])
                # print(rsp)
                if status:
                    print("jobId %s, completed successfully" % (align_rsp["jobID"]))
                    download_file(
                        token,
                        output_dir,
                        rsp[0]["output"]["almostMatch"]["source"],
                        os.path.basename(source_filepath).split(".")[0]
                        + "_aligned_am_src",
                    )
                    download_file(
                        token,
                        output_dir,
                        rsp[0]["output"]["almostMatch"]["target"],
                        os.path.basename(target_filepath).split(".")[0]
                        + "_aligned_am_tgt",
                    )

                    download_file(
                        token,
                        output_dir,
                        rsp[0]["output"]["match"]["source"],
                        os.path.basename(source_filepath).split(".")[0]
                        + "_aligned_m_src",
                    )
                    download_file(
                        token,
                        output_dir,
                        rsp[0]["output"]["match"]["target"],
                        os.path.basename(target_filepath).split(".")[0]
                        + "_aligned_m_tgt",
                    )
                    break
                else:
                    if rsp:
                        print(
                            f"jobId {align_rsp['jobID']}, Status: {rsp[0]['status']}, waiting for 10 seconds"
                        )
                    time.sleep(10)
