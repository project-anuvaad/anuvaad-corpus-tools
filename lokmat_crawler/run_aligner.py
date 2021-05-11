import config
import os
import glob
import time
import sys
import requests
import json
from argparse import ArgumentParser
from pathlib import Path
from util_tokenize_align import extract_bitext


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
    parser = ArgumentParser()
    #     parser.add_argument(
    #         "--csv-file-loc", help="location of csv file containing urls and release id",\
    #         type=str, required=True)
    parser.add_argument(
        "--input-folder",
        help="location of input  folder which contain main year folder",
        type=str,
        required=True,
    )
    parser.add_argument("--month", help="month", type=str, required=True)
    parser.add_argument("--year", help="year", type=str, required=True)
    parser.add_argument(
        "--lang-src",
        help="language code of source language:\
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
    parser.add_argument("--jobid", help="jobID", type=str, default="")
    args = parser.parse_args()
    n_month, n_year = args.month, args.year
    jobid = args.jobid
    lang = args.lang_src
    target_lang = "en"
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
        input_folder = args.input_folder
        source_file_loc = (
            input_folder
            + "//"
            + n_year
            + "//"
            + n_month
            + "_"
            + n_year
            + "//"
            + look_up_dict[lang]
        )
        target_file_loc = (
            input_folder
            + "//"
            + n_year
            + "//"
            + n_month
            + "_"
            + n_year
            + "//"
            + look_up_dict[target_lang]
        )
        source_loc = (
            source_file_loc
            + "//"
            + "total_"
            + lang
            + "_sen_"
            + n_month
            + "_"
            + n_year
            + ".txt"
        )
        target_loc = (
            target_file_loc
            + "//"
            + "total_"
            + target_lang
            + "_sen_"
            + n_month
            + "_"
            + n_year
            + ".txt"
        )
        align_loc = source_file_loc + "//align_" + lang + "_" + target_lang
        create_directory(align_loc)
    else:
        print("Please enter the corrent langauge code")
        return
    url = "https://users-auth.anuvaad.org/anuvaad/user-mgmt/v1/users/login"
    body = {"userName": config.ANUVAAD_USERNAME, "password": config.ANUVAAD_PASSWORD}
    r = requests.post(url=url, json=body)
    r.raise_for_status()
    bearerToken = json.loads(r.text)["data"]["token"]
    instance_time_start = time.time()
    print(f"Starting alligner")
    extract_bitext(
        bearerToken,
        align_loc,
        source_loc,
        target_loc,
        jobid,
        lang,
        config.BREAK_PROGRESS,
    )
    instance_run_time = time.time() - instance_time_start
    print(f"Time take since start:{(instance_run_time):.2f}")


if __name__ == "__main__":
    main()
