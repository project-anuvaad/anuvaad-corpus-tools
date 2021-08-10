import pandas as pd
import os
import glob
import sys
from argparse import ArgumentParser
from langdetect import detect
from indicnlp.tokenize.sentence_tokenize import sentence_split
from pathlib import Path
from langdetect import DetectorFactory
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
DetectorFactory.seed = 0


def create_directory(path):
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except FileExistsError as fe_error:
        return True
    except OSError as error:
        print(error)
    return False


def main():
    cut_off = 0
    parser = ArgumentParser()
    parser.add_argument(
        "--scrape-file-loc",
        help="location of scrape file to be sentence splitted",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output-folder", help="location of output folder", type=str, required=True
    )
    parser.add_argument(
        "--lang",
        help="language code :\
                                        'Kannada':'kn',\
                                        'Tamil':'ta',\
                                        'Marathi':'mr',\
                                        'Telugu':'te',\
                                        'Bengali':'bn',\
                                        'Gujarati':'gu',\
                                        'Malayalam':'ml',\
                                        'Punjabi':'pa',\
                                        'Assamese':'asm',\
                                        'Odia':'or',\
                                        'Urdu':'ur'",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    lang = args.lang
    look_up_dict = {
        "English": "en",
        "Hindi": "hi",
        "Kannada": "kn",
        "Tamil": "ta",
        "Marathi": "mr",
        "Telugu": "te",
        "Bengali": "bn",
        "Gujarati": "gu",
        "Malayalam": "ml",
        "Punjabi": "pa",
        "Assamese": "asm",
        "Odia": "or",
        "Urdu": "ur",
    }
    # Note: Inverting above dictionery
    look_up_dict = {v: k for k, v in look_up_dict.items()}
    if lang in look_up_dict.keys():
        scrape_loc = args.scrape_file_loc
        csv_file_loc = (
            args.output_folder
        )
        # list_fl = '_'.join([look_up_dict[lang],n_month,n_year]) + '.csv'
        tokenize_loc = csv_file_loc + "//" + "tokenize_file_" + os.path.basename(os.path.normpath(scrape_loc))
        # submit_aligner = csv_file_loc + '\\' + 'submit_aligner'
        if not os.path.exists(scrape_loc):
            print(f"Path dosent exists:{scrape_loc}")
            return
        create_directory(csv_file_loc)
        create_directory(tokenize_loc)

    else:
        print("Please enter the corrent langauge code")
        return
    total_sen_pd = pd.DataFrame(columns=[look_up_dict[lang] + "_sen"])
    fl_list = sorted(glob.glob(os.path.join(scrape_loc, "*.txt")))
    fl_list_rename = [
        os.path.join(
            scrape_loc,
            "_".join(
                [
                    os.path.basename(i).split(".")[0].split()[0].zfill(5),
                    *os.path.basename(i).split(".")[0].split()[1:6],
                ]
            ),
        )
        + "."
        + os.path.basename(i).split(".")[-1]
        for i in fl_list
    ]
    for org, chg in zip(fl_list, fl_list_rename):
        os.rename(org, chg)
    fl_list = sorted(glob.glob(os.path.join(scrape_loc, "*.txt")))
    old_count = 0
    for k, fl in tqdm(enumerate(fl_list), total = len(fl_list)):
        if k < cut_off: continue
        # print(os.path.basename(fl))
        # Read Scrape Content
        tok_flname = tokenize_loc + "//tok_" + os.path.basename(fl)
        with open(fl, mode="r", encoding="utf-16-le") as file_r:
            content = file_r.read()
        #             print(content)
        # Cleaning scrape content
        paragraph = content.split("\n")
        content = []
        for para in paragraph:
            para = para.strip()
            para = " ".join(para.split())
            if len(para.split()) >= 1:
                if lang == "en":
                    content.append(para)
                else:
                    try:
                        if detect(para) != "en":
                            content.append(para)
                    except:
                        content.append(para)
        # Tokenizing paragraphs into sentences
        sentences = []
        if lang != 'en':
            for entry in content:
                [sentences.append(tok_sen) for tok_sen in sentence_split(entry, lang)]
        else:
            for entry in content:
                [sentences.append(tok_sen) for tok_sen in sent_tokenize(entry)]
        # Removing Duplicates
        dump_1 = (
            pd.DataFrame(sentences, columns=["sen"])
            .drop_duplicates()
            .loc[:, "sen"]
            .values.tolist()
        )
        sentences = dump_1
        # Write sentence token
        with open(tok_flname, mode="w", encoding="utf-16") as file_w:
            for sen in sentences:
                sen = sen.strip()
                sen = sen.strip('"')
                if len(sen.split()) >= 1:
                    file_w.write(sen + "\n")
                    total_sen_pd = total_sen_pd.append(
                        {look_up_dict[lang] + "_sen": sen.strip()}, ignore_index=True
                    )
        # print(f'Number of sentences found: {total_sen_pd.shape[0]-old_count}')
        old_count = total_sen_pd.shape[0]

    print(f"Total number of sentences found: {total_sen_pd.shape[0]}")
    total_sen_pd.drop_duplicates(inplace=True)
    print(
        f"Total number of sentences after removing duplicate: {total_sen_pd.shape[0]}"
    )
    sys.stdout.flush()
    total_sen_pd.to_csv(
        csv_file_loc
        + "//"
        + "total_"
        + lang
        + "_sen_"
        + os.path.basename(os.path.normpath(scrape_loc))
        + ".csv",
        index=False,
        encoding="utf-16",
    )
    with open(
        csv_file_loc
        + "//"
        + "total_"
        + lang
        + "_sen_"
        + os.path.basename(os.path.normpath(scrape_loc))
        + ".txt",
        mode="w",
        encoding="utf-16",
    ) as write_total:
        for line in total_sen_pd[look_up_dict[lang] + "_sen"].values.tolist():
            write_total.write(line.strip() + "\n")


if __name__ == "__main__":
    main()
