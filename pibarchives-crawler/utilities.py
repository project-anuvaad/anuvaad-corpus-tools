from bs4 import BeautifulSoup
import os
from retry import retry
import urllib
import requests
import json


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
def get_html(filename):
    url = urllib.request.urlopen(filename)
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
    url_en = "https://auth.anuvaad.org/tokenize-sentence"
    url_hi = "https://auth.anuvaad.org/tokenize-hindi-sentence"
    if lang == "en":
        req = requests.post(url_en, json=js)
    elif lang == "hi":
        req = requests.post(url_hi, json=js)
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
