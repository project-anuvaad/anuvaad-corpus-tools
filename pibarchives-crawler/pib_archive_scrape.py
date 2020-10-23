# Scrape PIB Archive Website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from utilities import create_directory, get_html
import time
import pandas as pd
import os
import numpy as np
import re
import random
from argparse import ArgumentParser

WAIT_TIME = 8
EXE_PATH = "C:\\Users\\navne\\Downloads\\geckodriver-v0.27.0-win64\\geckodriver.exe"


def get_prid_and_ministry_list(month, year, lang):
    """
    Change exe_path variable to the driver location
    Get the release id, ministry-list for a given year,month,language
    This will open a firefox browser and populate forms to get only the release Id
    """

    def _is_element_stale(try_element):
        """
        check whether selenium web-element is stale or not
        True- If element is stale
        """
        try:
            try_element.is_displayed()
            return False
        except StaleElementReferenceException:
            return True
        except NoSuchElementException:
            return True

    driver = webdriver.Firefox(executable_path=EXE_PATH)
    if lang == "en":
        language = "English"
        df_return = pd.DataFrame(columns=["English_release_id"])
        ministry_select_text = "All Ministries"
        driver.get("http://pibarchive.nic.in/archive2/erelease.aspx")
        link_initial = "http://pibarchive.nic.in/archive2/erelcontent.aspx?relid="
    elif lang == "hi":
        language = "Hindi"
        df_return = pd.DataFrame(columns=["Hindi_release_id"])
        ministry_select_text = "सभी मंत्रालय"
        driver.get("http://pibarchive.nic.in/archive2/hindirelease.aspx")
        link_initial = "http://pibarchive.nic.in/archive2/hindiContentRel.aspx?relid="
    else:
        print("Correct language code not specified")
        return None, None
    assert "PIB" in driver.title, "/'PIB/' not in title"
    n_year = str(year)
    n_month = str(month).capitalize()
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 20)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".col-md-4.erelease-left1"))
    )

    # Populate ministry,month and year
    # Extract all ministry name
    select_ministry = Select(driver.find_element_by_id("minID"))
    select_ministry.select_by_visible_text(ministry_select_text)
    select_month = Select(driver.find_element_by_id("rmonthID"))
    select_month.select_by_visible_text(n_month)
    select_year = Select(driver.find_element_by_id("ryearID"))
    select_year.select_by_visible_text(n_year)
    set_day = driver.find_element_by_id("rdateID")
    option_ministry = driver.find_element_by_id("minID").find_elements_by_tag_name(
        "option"
    )
    count_old = 0
    list_ministry = []
    for mn in option_ministry:
        list_ministry.append(" ".join(str(mn.text).split()))

    # Loop through all the days for a given month
    print(f"Extracting release id for {n_month}, {n_year}, {language}")
    count = 0
    first_id = ""
    old_f_id = ""
    day_options = set_day.find_elements_by_tag_name("option")
    wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='link1']")))
    old_releaseid_el = driver.find_element(By.XPATH, "//ul[@class='link1']")
    for option in day_options:
        if option.text == "All":
            continue
        old_releaseid_el = driver.find_element(By.XPATH, "//ul[@class='link1']")
        option.click()
        time.sleep(0.5)
        wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='link1']")))
        day_val = str(
            pd.to_datetime(
                "-".join(
                    driver.find_element(
                        By.XPATH, "//div[@id='relhead' and @class='mddiv']"
                    ).text.split()[2:]
                ),
                errors="coerce",
            ).day
        )
        if day_val == "nan":
            day_val = option.text
        start_time = time.time()
        while (not _is_element_stale(old_releaseid_el)) or day_val != option.text:
            time.sleep(0.5)
            if time.time() - start_time > WAIT_TIME:
                rand_day = random.choice(day_options)
                while option.text == rand_day.text or rand_day.text == "All":
                    rand_day = random.choice(day_options)
                old_releaseid_el = driver.find_element(By.XPATH, "//ul[@class='link1']")
                rand_day.click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@class='link1']"))
                )

                while not _is_element_stale(old_releaseid_el):
                    time.sleep(0.5)
                old_releaseid_el = driver.find_element(By.XPATH, "//ul[@class='link1']")
                option.click()
                time.sleep(0.5)
                wait.until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@class='link1']"))
                )
                start_time = time.time()
            day_val = str(
                pd.to_datetime(
                    "-".join(
                        driver.find_element(
                            By.XPATH, "//div[@id='relhead' and @class='mddiv']"
                        ).text.split()[2:]
                    ),
                    errors="coerce",
                ).day
            )
            if day_val == "nan":
                day_val = option.text

        trial = 0
        while first_id == old_f_id:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "lreleaseID")))
            content = driver.find_element_by_id("lreleaseID")
            all_id = content.find_elements_by_xpath(
                "//li[@class='rel rel-list' and @id]"
            )
            if len(all_id) == 0 and trial > 1:
                break
            try:
                all_id[-1].click()
                first_id = all_id[0].get_attribute("id")
            except:
                pass
            trial += 1
        for ct, on_id in enumerate(all_id):
            if ct == 0:
                first_id = on_id.get_attribute("id")
            count += 1
            df_return = df_return.append(
                {language + "_release_id": on_id.get_attribute("id")}, ignore_index=True
            )
        old_f_id = first_id
    if count != count_old:
        print("Total count is :", count)
    count_old = count
    driver.close()
    df_return["Link"] = df_return[language + "_release_id"].apply(
        lambda x: link_initial + x
    )
    return df_return, list_ministry


def scrape_pib_archives(df_data, month, year, lang, out_dir, list_ministry):
    """
    Scrape text using the links provided in dataframe
    Create and write a new dataframe with postin date-time
    """
    print(f'Scraping for {month}, {year}, {"English" if lang=="en" else "Hindi"}')
    n_month, n_year = str(month), str(year)
    n_month = n_month.lower()
    main_dir = out_dir
    work_dir = main_dir + "//" + n_month + "_" + n_year
    create_directory(work_dir)
    if lang == "en":
        language = "English"
        language_2 = "Hindi"
        scrape_loc = work_dir + "//" + "scrape_file_en_" + n_month + "_" + n_year
    elif lang == "hi":
        language = "Hindi"
        language_2 = "English"
        scrape_loc = work_dir + "//" + "scrape_file_hi_" + n_month + "_" + n_year
    else:
        print("Pass valid language code")
        return None
    create_directory(scrape_loc)
    df_data[language + "_Ministry_Name"] = [""] * df_data.shape[0]
    df_data[language_2 + "_Ministry_Name"] = [""] * df_data.shape[0]
    df_data["Posting_Datetime"] = [pd.to_datetime(np.nan)] * df_data.shape[0]
    df_data["Posting_Date"] = df_data["Posting_Datetime"].apply(lambda x: x.date())
    for p_th in range(df_data.shape[0])[:]:
        b_source = get_html(df_data.loc[p_th, "Link"])
        m_dt = b_source.find("div", attrs={"class": "mddiv content-ministry"})
        m = b_source.find("div", attrs={"class": "contentdiv"})
        df_data.at[p_th, language + "_Ministry_Name"] = str(
            " ".join(m_dt.contents[0].strip().split())
        )
        if (
            str(" ".join(m_dt.contents[0].strip().split()))
            not in list_ministry[language + "_Ministry_Name"].values.tolist()
        ):
            print(
                "Ministry name missing:",
                str(" ".join(m_dt.contents[0].strip().split())),
            )
        else:
            df_data.at[p_th, language_2 + "_Ministry_Name"] = list_ministry[
                list_ministry[language + "_Ministry_Name"]
                == df_data.at[p_th, language + "_Ministry_Name"]
            ][language_2 + "_Ministry_Name"].values[0]

        df_data.at[p_th, "Posting_Datetime"] = pd.to_datetime(
            (" ".join(m_dt.contents[1].text.split()[:-1]))
            .replace(".", ":")
            .replace(": ", ":")
        )
        df_data.at[p_th, "Posting_Date"] = df_data.at[p_th, "Posting_Datetime"].date()
        scrape_file = (
            scrape_loc
            + "//"
            + str(p_th).zfill(4)
            + "_"
            + lang
            + "_"
            + "_".join(df_data.loc[p_th, ["English_Ministry_Name"]].values[0].split())
            + "_"
            + df_data.loc[p_th, ["Posting_Date"]].values[0].strftime("%Y-%m-%d")
            + "_"
            + df_data.loc[p_th, "Link"].split("=")[-1]
            + ".txt"
        )
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
        with open(scrape_file, mode="w", encoding="utf-16") as file_w:
            for line in k_en:
                if "@font-face" in line.strip():
                    continue
                line = re.sub("\r\n-", "\n-", line)
                line = re.sub("\.\s+\r\n", ".\n", line)
                #         print(line)
                line = re.sub(":\s+\r\n", ":\n", line)
                line = re.sub(";\s+\r\n", ";\n", line)
                line = line.replace("\r\n", " ")
                for ln in line.split("\n"):
                    ln = ln.strip()
                    if len(ln.strip()) == 0:
                        continue
                    if "@font-face" in ln.strip():
                        continue
                    ln = " ".join(ln.split())

                    file_w.write(ln.strip().replace("\r", "") + "\n")
    print(df_data.info())
    if True:
        df_data.to_csv(
            os.path.join(
                work_dir, language + "_data_" + n_month + "_" + n_year + ".csv"
            ),
            index=False,
            encoding="utf-16",
        )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--output-dir", help="output directory", type=str, required=True
    )
    parser.add_argument("--month", help="month", type=str, required=True)
    parser.add_argument("--year", help="year", type=str, required=True)
    args = parser.parse_args()
    create_directory(args.output_dir)
    # creating release id and url link datframe
    # also creating ministry list
    df_en, list_ministry_en = get_prid_and_ministry_list(args.month, args.year, "en")
    df_hi, list_ministry_hi = get_prid_and_ministry_list(args.month, args.year, "hi")
    if len(list_ministry_en) == len(list_ministry_en):
        print(len(list_ministry_en), len(list_ministry_en))
        ministry_data = pd.DataFrame(
            list(zip(list_ministry_en, list_ministry_hi)),
            columns=["English_Ministry_Name", "Hindi_Ministry_Name"],
        )
        # Scraping the url links
        scrape_pib_archives(
            df_en, args.month, args.year, "en", args.output_dir, ministry_data
        )
        scrape_pib_archives(
            df_hi, args.month, args.year, "hi", args.output_dir, ministry_data
        )
        work_dir = args.output_dir + "//" + args.month + "_" + args.year
        ministry_data.to_csv(
            os.path.join(
                work_dir, "ministry_list_" + args.month + "_" + args.year + ".csv"
            ),
            index=False,
            encoding="utf-16",
        )
    else:
        print("Number of ministry entry in English and Hindi is not matching")
