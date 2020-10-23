# Running tokenizer on scraped file
import sys
import pandas as pd
import numpy as np
import os
import glob
from argparse import ArgumentParser
from utilities import (
    create_directory,
    write_sentence_list_to_file,
    api_sen_tokenizer_call,
)


def tokenized_scrape_file(n_month, n_year, lang, out_dir):
    """
    Read scrape file and tokenized the sentences
    Write the tokenized file
    """
    if lang == "en":
        language = "English"
    elif lang == "hi":
        language = "Hindi"
    else:
        print("Invalid language code passed")
        return None
    work_dir = out_dir + "//" + n_month + "_" + n_year
    scrape_loc = work_dir + "//" + "_".join(["scrape_file", lang, n_month, n_year])
    tokenize_loc = work_dir + "//" + "_".join(["tokenize", lang, n_month, n_year])
    create_directory(tokenize_loc)
    fl_list = sorted(glob.glob(os.path.join(scrape_loc, "*.txt")))
    for k, fl in enumerate(fl_list):
        print(os.path.basename(fl))
        flname = tokenize_loc + "//tok_" + os.path.basename(fl)
        with open(fl, mode="r", encoding="utf-16") as file_n:
            para_val = [
                {"text": line.strip()}
                for line in file_n
                if len(line.strip().split()) > 2
            ]
        if len(para_val) > 500:
            sen = []
            for i in range(int(np.ceil(len(para_val) / 500)) + 1):
                js = {"paragraphs": para_val[i * 500 : (i + 1) * 500]}
                sen_sub = api_sen_tokenizer_call(js, lang)
                for line in sen_sub:
                    sen.append(line)
        else:
            js = {"paragraphs": para_val}
            sen = api_sen_tokenizer_call(js, lang)
        dump_1 = (
            pd.DataFrame(sen, columns=["sen"])
            .drop_duplicates()
            .loc[:, "sen"]
            .values.tolist()
        )
        sen = dump_1
        write_sentence_list_to_file(flname, sen)
    return None


def total_sen_csv_from_tokenized_file(n_month, n_year, lang, out_dir):
    if lang == "en":
        language = "English"
    elif lang == "hi":
        language = "Hindi"
    else:
        print("Invalid language code passed")
        return None
    total_pd = pd.DataFrame(columns=[language + "_sen"])
    work_dir = out_dir + "//" + n_month + "_" + n_year
    tokenize_loc = work_dir + "//" + "_".join(["tokenize", lang, n_month, n_year])
    fl_list = sorted(glob.glob(os.path.join(tokenize_loc, "*.txt")))
    for k, fl in enumerate(fl_list):
        with open(fl, mode="r", encoding="utf-16") as file_n:
            for line in file_n:
                total_pd = total_pd.append(
                    {language + "_sen": line.strip()}, ignore_index=True
                )
    total_pd.drop_duplicates(inplace=True)
    total_pd.to_csv(
        work_dir + "//" + "total_" + lang + "_sen_" + n_month + "_" + n_year + ".csv",
        index=False,
        encoding="utf-16",
    )
    return total_pd


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--output-dir", help="output directory", type=str, required=True
    )
    parser.add_argument("--month", help="month", type=str, required=True)
    parser.add_argument("--year", help="year", type=str, required=True)
    args = parser.parse_args()

    #     months = "january february march april may june july august september october november december".split()

    #     for n_month in months[:]:
    tokenized_scrape_file(args.month, args.year, "en", args.output_dir)
    tokenized_scrape_file(args.month, args.year, "hi", args.output_dir)

    # Writing all tokenized sentences to csv file
    #     for n_month in months[:]:
    total_sen_csv_from_tokenized_file(args.month, args.year, "en", args.output_dir)
    total_sen_csv_from_tokenized_file(args.month, args.year, "hi", args.output_dir)


if __name__ == "__main__":
    main()
