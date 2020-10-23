import pandas as pd
import numpy as np
import os
import glob
import time
import sys
from argparse import ArgumentParser
from utilities import create_directory, get_file_content, extract_bitext, detect_non_eng

BEARER_TOKEN =


def preprocess_dataframe(df_data):
    """
    Add index and PRID(press release id) columns to dataframe
    Remove Null Posting_Datetime entry
    """
    df_data["Posting_Date"] = pd.to_datetime(df_data["Posting_Date"], errors="coerce")
    df_data["Posting_Datetime"] = pd.to_datetime(
        df_data["Posting_Datetime"], errors="coerce"
    )
    if "index" not in df_data.columns.tolist():
        df_data.reset_index(inplace=True)

    if not "PRID" in df_data.columns.tolist():
        df_data["PRID"] = df_data["Link"].apply(lambda x: x.split("=")[-1])

    df_data["Posting_Datetime"] = df_data.apply(
        lambda x: x["Posting_Date"]
        if pd.isnull(x["Posting_Datetime"])
        else x["Posting_Datetime"],
        axis=1,
    )
    return df_data


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--output-dir", help="output directory", type=str, required=True
    )
    parser.add_argument("--month", help="month", type=str, required=True)
    parser.add_argument("--year", help="year", type=str, required=True)
    args = parser.parse_args()

    n_month, n_year = str(args.month).lower(), str(args.year)
    work_dir = args.output_dir + "//" + n_month + "_" + n_year
    align_loc = work_dir + "//" + "align_" + n_month + "_" + n_year
    tokenize_loc_en = work_dir + "//" + "tokenize_en_" + n_month + "_" + n_year
    tokenize_loc_hi = work_dir + "//" + "tokenize_hi_" + n_month + "_" + n_year
    submit_aligner = work_dir + "//" + "submit_aligner_" + n_month + "_" + n_year
    en_data_file = "_".join(["English", "data", n_month, n_year]) + ".csv"
    hi_data_file = "_".join(["Hindi", "data", n_month, n_year]) + ".csv"

    create_directory(align_loc)
    create_directory(submit_aligner)

    df_en = pd.read_csv(work_dir + "//" + en_data_file, encoding="utf-16")
    df_hi = pd.read_csv(work_dir + "//" + hi_data_file, encoding="utf-16")
    df_en = preprocess_dataframe(df_en)
    df_hi = preprocess_dataframe(df_hi)
    df_en.to_csv(work_dir + "//" + en_data_file, index=False, encoding="utf-16")
    df_hi.to_csv(work_dir + "//" + hi_data_file, index=False, encoding="utf-16")

    # Crete files which are parallel based on Ministry Name and Posting Date
    k_hi = pd.DataFrame(
        df_hi[["English_Ministry_Name", "Posting_Date", "index"]]
        .groupby(["English_Ministry_Name", "Posting_Date"])["index"]
        .apply(lambda x: x.tolist())
    )
    k_en = pd.DataFrame(
        df_en[["English_Ministry_Name", "Posting_Date", "index"]]
        .groupby(["English_Ministry_Name", "Posting_Date"])["index"]
        .apply(lambda x: x.tolist())
    )
    k_merge = pd.merge(
        k_en,
        k_hi,
        left_index=True,
        right_index=True,
        how="inner",
        suffixes=("_en", "_hi"),
    )
    k_merge.to_csv(
        work_dir + "//" + "submit_aligner_" + n_month + "_" + n_year + ".csv",
        index=True,
        encoding="utf-16",
    )

    fl_tok_en = sorted(glob.glob(tokenize_loc_en + "//" + "*.txt"))
    fl_tok_hi = sorted(glob.glob(tokenize_loc_hi + "//" + "*.txt"))
    no_sen_df = pd.DataFrame(
        columns=[
            "Filename_en",
            "Total_sentences_en",
            "Filename_hi",
            "Total_sentences_hi",
        ]
    )
    for count, i in enumerate(k_merge.iterrows()):
        en_align_file = (
            submit_aligner
            + "//subalign_"
            + str(count).zfill(4)
            + "_en_"
            + "_".join(i[0][0].split())
            + "_"
            + i[0][1].strftime("%Y-%m-%d")
            + ".txt"
        )
        hi_align_file = (
            submit_aligner
            + "//subalign_"
            + str(count).zfill(4)
            + "_hi_"
            + "_".join(i[0][0].split())
            + "_"
            + i[0][1].strftime("%Y-%m-%d")
            + ".txt"
        )
        with open(en_align_file, encoding="utf-16", mode="w") as flw_en:
            count_en = 0
            for ind in i[1]["index_en"]:
                with open(fl_tok_en[ind], encoding="utf-16", mode="r") as flr_en:
                    k_en = flr_en.read()
                    count_en += k_en.count("\n")
                    flw_en.write(k_en)
        with open(hi_align_file, encoding="utf-16", mode="w") as flw_hi:
            count_hi = 0
            for ind in i[1]["index_hi"]:
                with open(fl_tok_hi[ind], encoding="utf-16", mode="r") as flr_hi:
                    k_hi = flr_hi.read()
                    count_hi += k_hi.count("\n")
                    flw_hi.write(k_hi)
        no_sen_df = no_sen_df.append(
            {
                "Filename_en": os.path.basename(en_align_file),
                "Total_sentences_en": count_en,
                "Filename_hi": os.path.basename(hi_align_file),
                "Total_sentences_hi": count_hi,
            },
            ignore_index=True,
        )
        print(
            f"Writing {os.path.basename(en_align_file)} and {os.path.basename(hi_align_file)} done"
        )
    no_sen_df.to_csv(
        work_dir + "//" + "tok_sen_count_" + n_month + "_" + n_year + ".csv",
        index=False,
        encoding="utf-16",
    )
    fl_list = glob.glob(submit_aligner + "//" + "*.txt")
    en_fl = sorted([i for i in fl_list if os.path.basename(i).split("_")[2] == "en"])
    hi_fl = sorted([i for i in fl_list if os.path.basename(i).split("_")[2] == "hi"])
    c_fl = list(zip(en_fl, hi_fl))
    for i in c_fl:
        extract_bitext(BEARER_TOKEN, align_loc, i[0], i[1])


if __name__ == "__main__":
    main()
