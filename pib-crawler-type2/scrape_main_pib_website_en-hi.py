import pandas as pd
import os
from argparse import ArgumentParser

from utilities import (
    create_directory,
    get_html,
    write_scrape_text_file,
    get_data,
)

HTML_FOLDER = "C://Users//navne//Desktop//Tarento_doc_scraping//PIB//code_base//upload_code//pib_main//url_location"
MINISTRY_NAME_PARALLEL_LOCATION = "./ministry_parallel_list.csv"


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--output-dir", help="output directory", type=str, required=True
    )
    parser.add_argument("--month", help="month", type=str, required=True)
    parser.add_argument("--year", help="year", type=str, required=True)
    parser.add_argument(
        "--import-csv",
        help="yes/no : Whether to import existing csv file.Default is 'no'",
        type=str,
        default="no",
    )
    args = parser.parse_args()
    main_dir = args.output_dir
    n_month, n_year = args.month.lower(), args.year
    work_dir = main_dir + "//" + n_month + "_" + n_year
    create_directory(main_dir)
    create_directory(work_dir)
    log_file_write = open(work_dir + "//scrape_en-hi_log_file.txt", mode="w")
    log_file_write.write(f"{n_month,n_year}\n")

    if args.import_csv.lower() == "yes":
        set_import = True
    elif args.import_csv.lower() == "no":
        set_import = False
    else:
        log_file_write.write(f"\n Please enter a valid option for import-csv")

    scrape_loc_en = work_dir + "//" + "scrape_file_en_" + n_month + "_" + n_year
    scrape_loc_hi = work_dir + "//" + "scrape_file_hi_" + n_month + "_" + n_year
    create_directory(scrape_loc_hi)
    create_directory(scrape_loc_en)
    url_file_loc = "file:///" + HTML_FOLDER + "//Press Information Bureau."
    filename_url_en = url_file_loc + "_en_" + n_month + "_" + n_year + ".html"
    filename_url_hi = url_file_loc + "_hi_" + n_month + "_" + n_year + ".html"

    ministy_pa_list = pd.read_csv(
        MINISTRY_NAME_PARALLEL_LOCATION,
        encoding="utf-16",
    )
    parse_url_en = get_html(filename_url_en)
    parse_url_hi = get_html(filename_url_hi)
    no_of_result_en = int(
        (parse_url_en.find("div", {"class": "search_box_result"}).contents[0]).split()[
            1
        ]
    )
    no_of_result_hi = int(
        (parse_url_hi.find("div", {"class": "search_box_result"}).contents[0]).split()[
            1
        ]
    )
    log_file_write.write(f"\nNo of search result in {n_month} of {n_year}:")
    log_file_write.write(f"\n English: {no_of_result_en} \n Hindi: {no_of_result_hi}")
    log_file_write.write(
        f"\nNo of Ministry in English search result:\
                         {len(parse_url_en.findAll('h3',{'class':'font104'}))}"
    )
    log_file_write.write(
        f"\nNo of Ministry in Hindi search result:\
                         {len(parse_url_hi.findAll('h3',{'class':'font104'}))}"
    )

    # Import or Create english dataframe
    df_en = get_data(
        n_month,
        n_year,
        filename_url_en,
        ministy_pa_list,
        "en",
        log_file_write,
        import_data=set_import,
        import_data_dir=work_dir,
    )
    if "PRID" not in df_en.columns.tolist():
        df_en["PRID"] = df_en["Link"].apply(lambda x: x.split("=")[-1])
    log_file_write.write(f"\n English Datframe \n")
    log_file_write.write(f"\n Datframe Info:\n")
    df_en.info(buf=log_file_write)

    # Write the English Dataframe
    df_en.to_csv(
        os.path.join(work_dir, "English_data_" + n_month + "_" + n_year + ".csv"),
        index=False,
        encoding="utf-16",
    )

    # Scraping English Documents
    iter_f = df_en.shape[0]
    log_file_write.write("\nStarting scraping for English Document")
    for i in range(iter_f):
        en_scrape_file = (
            scrape_loc_en
            + "//"
            + str(i).zfill(4)
            + "_en_"
            + "_".join(df_en.loc[i, ["English_Ministry_Name"]].values[0].split())
            + "_"
            + df_en.loc[i, ["Posting_Date"]].values[0].strftime("%Y-%m-%d")
            + "_"
            + str(df_en.loc[i, ["PRID"]].values[0])
            + ".txt"
        )
        m = 0
        while m == 0:
            try:
                b = get_html(df_en.Link[i], "lxml")
                m = b.body.form.find(
                    "div", {"class": "innner-page-main-about-us-content-right-part"}
                )
            except:
                log_file_write.write("\nerror:retrying")
                m = 0
        if m is None:
            log_file_write.write(
                f"\nindex: {i}, Link: {df_en.Link[i]}, no english content found"
            )
            continue
        k_en = [
            str(k.get_text()).strip()
            for k in m.findAll(
                [
                    "div",
                    "tr",
                    "td",
                    "p",
                    "ol",
                    "h2",
                    "h3",
                    "h4",
                    "ul",
                    "pre",
                    "span",
                    "li",
                ]
            )
            if len(
                k.find_parents(["p", "ol", "h2", "h3", "h4", "ul", "pre", "span", "li"])
            )
            == 0
        ]
        if len(k_en) == 0:
            log_file_write.write(
                f"\nindex: {i}, Link: {df_en.Link[i]},no English content in variuos tags"
            )
            continue
        log_file_write.write(f"\nindex: {i}, number of lines: {len(k_en)}")
        write_scrape_text_file(en_scrape_file, k_en, df_en.English_Ministry_Name[i])
    log_file_write.write(f"\nDone scraping for English Document")

    # Import or Create hindi dataframe
    df_hi = get_data(
        n_month,
        n_year,
        filename_url_hi,
        ministy_pa_list,
        "hi",
        log_file_write,
        import_data=set_import,
        import_data_dir=work_dir,
    )
    if "PRID" not in df_hi.columns.tolist():
        df_hi["PRID"] = df_hi["Link"].apply(lambda x: x.split("=")[-1])
    log_file_write.write(f"\nHindi Datframe \n")
    log_file_write.write(f"\nDatframe Info:\n")
    df_hi.info(buf=log_file_write)

    # Write the Hindi Dataframe
    df_hi.to_csv(
        os.path.join(work_dir, "Hindi_data_" + n_month + "_" + n_year + ".csv"),
        index=False,
        encoding="utf-16",
    )

    # Scraping Hindi Documents
    iter_f = df_hi.shape[0]
    log_file_write.write("\nStarting scraping for Hindi Document")
    for i in range(iter_f):
        hi_scrape_file = (
            scrape_loc_hi
            + "//"
            + str(i).zfill(4)
            + "_hi_"
            + "_".join(df_hi.loc[i, ["English_Ministry_Name"]].values[0].split())
            + "_"
            + df_hi.loc[i, ["Posting_Date"]].values[0].strftime("%Y-%m-%d")
            + "_"
            + str(df_hi.loc[i, ["PRID"]].values[0])
            + ".txt"
        )
        m = 0
        while m == 0:
            try:
                b = get_html(df_hi.Link[i], "lxml")
                m = b.body.form.find(
                    "div", {"class": "innner-page-main-about-us-content-right-part"}
                )
            except:
                log_file_write.write("\nerror:retrying")
                m = 0
        if m is None:
            log_file_write.write(
                f"\nindex: {i}, Link: {df_hi.Link[i]}, no hindi content found"
            )
            continue
        k_hi = [
            str(k.get_text()).strip()
            for k in m.findAll(
                [
                    "div",
                    "tr",
                    "td",
                    "p",
                    "ol",
                    "h2",
                    "h3",
                    "h4",
                    "ul",
                    "pre",
                    "span",
                    "li",
                ]
            )
            if len(
                k.find_parents(["p", "ol", "h2", "h3", "h4", "ul", "pre", "span", "li"])
            )
            == 0
        ]
        if len(k_hi) == 0:
            log_file_write.write(
                f"\nindex: {i}, Link: {df_hi.Link[i]},no hindi content in variuos tags"
            )
            continue
        log_file_write.write(f"\nindex: {i}, number of lines: {len(k_hi)}")
        write_scrape_text_file(hi_scrape_file, k_hi, df_hi.Hindi_Ministry_Name[i])
    log_file_write.write("\nDone scraping for Hindi Document")
    log_file_write.close()


if __name__ == "__main__":
    main()
