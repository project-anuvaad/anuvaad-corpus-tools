import pandas as pd
import config
import time
import os
from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_driver(web_browser="chrome"):
    if web_browser == "chrome":

        options = webdriver.chrome.options.Options()
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--log-level=3")
        prefs = {
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option(
            "excludeSwitches", ["load-extension", "enable-automation", "enable-logging"]
        )
        driver = webdriver.Chrome(config.CHROME_DRIVER_PATH, options=options)
        return driver
    else:
        print("Currently only support chrome driver")
        return None


def write_english_link_month(year, month, driver, out_dir):
    month = month.capitalize()
    month_day_dict = {
        "January": 31,
        "February": 28,
        "March": 31,
        "April": 30,
        "May": 31,
        "June": 30,
        "July": 31,
        "August": 31,
        "September": 30,
        "October": 31,
        "November": 30,
        "December": 31,
    }
    month_end_day = month_day_dict[month]
    print(year, month)
    wait = WebDriverWait(driver, config.DRIVER_WAIT_TIME)
    data_table = pd.DataFrame(columns=["Headline", "Datetime", "Link"])
    for start_date, end_date in [
        (1, 5),
        (4, 9),
        (8, 13),
        (12, 17),
        (16, 21),
        (20, 25),
        (24, 28),
        (27, month_end_day),
    ]:
        print(f"dates between:{start_date}-{end_date}")
        repeat = True
        while repeat:
            start_date_class_attr = "react-datepicker__day react-datepicker__day--" + str(
                start_date
            ).zfill(
                3
            )
            end_date_class_attr = "react-datepicker__day react-datepicker__day--" + str(
                end_date
            ).zfill(3)
            driver.get("https://en.prothomalo.com/search")
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@class='label-with-arrow-m__label-with-arrow__2kufR']",
                    )
                )
            )
            k = driver.find_elements_by_xpath(
                "//div[@class='label-with-arrow-m__label-with-arrow__2kufR']"
            )[-1]
            driver.execute_script("arguments[0].click();", k)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@placeholder='Start date']")
                )
            )
            k = driver.find_elements_by_xpath("//input[@placeholder='Start date']")[-1]
            driver.execute_script("arguments[0].click();", k)
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']",
                    )
                )
            )
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//option[contains(text(),'{month}')]")
                )
            )
            select_year = Select(
                driver.find_element_by_xpath(
                    "//select[@class='react-datepicker__year-select']"
                )
            )
            select_year.select_by_visible_text(year)
            select_month = Select(
                driver.find_element_by_xpath(
                    "//select[@class='react-datepicker__month-select']"
                )
            )
            select_month.select_by_visible_text(month)
            while True:
                if (
                    month
                    in driver.find_elements_by_xpath(
                        "//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']"
                    )[0].text
                ):
                    break
                else:
                    time.sleep(2)
                    print("waiting 2 sec")
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//div[contains(@class,'{start_date_class_attr}')]")
                )
            )
            k = [
                i
                for i in driver.find_elements_by_xpath(
                    f"//div[contains(@class,'{start_date_class_attr}')]"
                )
                if "react-datepicker__day--outside-month"
                not in i.get_attribute("class").split()
            ][0]
            driver.execute_script("arguments[0].click();", k)

            k = driver.find_elements_by_xpath("//input[@placeholder='End Date']")[-1]
            driver.execute_script("arguments[0].click();", k)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//option[contains(text(),'{month}')]")
                )
            )
            select_month = Select(
                driver.find_element_by_xpath(
                    "//select[@class='react-datepicker__month-select']"
                )
            )
            select_month.select_by_visible_text(month)
            while True:
                if (
                    month
                    in driver.find_elements_by_xpath(
                        "//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']"
                    )[0].text
                ):
                    break
                else:
                    time.sleep(2)
                    print("waiting 2 sec")
            select_year = Select(
                driver.find_element_by_xpath(
                    "//select[@class='react-datepicker__year-select']"
                )
            )
            select_year.select_by_visible_text(year)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//div[contains(@class,'{end_date_class_attr}')]")
                )
            )
            k = [
                i
                for i in driver.find_elements_by_xpath(
                    f"//div[contains(@class,'{end_date_class_attr}')]"
                )
                if "react-datepicker__day--outside-month"
                not in i.get_attribute("class").split()
            ][0]
            driver.execute_script("arguments[0].click();", k)
            time.sleep(2)
            no_entries = int(
                driver.find_elements_by_xpath(
                    "//div[@class='searchStories1AdWithLoadMore-m__label__2NcU1']/span"
                )[1].text
            )
            print(f"No of entries found:{no_entries}")
            while True:
                headings = driver.find_elements_by_xpath(
                    '//h2[@class="headline headline-type-27  story-headline  headline-m__headline__3vaq9 headline-m__headline-type-27__3ywG6"]'
                )
                elements = driver.find_elements_by_xpath(
                    '//span[@class="load-more-content more-m__content__1XWY0 more-m__en-content__2lUOO"]'
                )
                if len(elements) == 1:
                    driver.execute_script("arguments[0].click();", elements[0])
                    time.sleep(2)
                    headings = driver.find_elements_by_xpath(
                        '//h2[@class="headline headline-type-27  story-headline  headline-m__headline__3vaq9 headline-m__headline-type-27__3ywG6"]'
                    )
                    print(len(headings), end="-")
                elif len(headings) == no_entries:
                    repeat = False
                    break
                else:
                    break
        entries = driver.find_elements_by_xpath(
            "//div[@class='customStoryCard9-m__wrapper__yEFJV']"
        )
        print(f"Appending {len(entries)} entries")
        for entry in entries:
            headline = entry.find_element_by_xpath(
                ".//h2[@class='headline headline-type-27  story-headline  headline-m__headline__3vaq9 headline-m__headline-type-27__3ywG6']"
            ).text
            datetime = entry.find_element_by_xpath(
                ".//div[@class='story-meta-data storyMetaData-m__story-meta-data__2E2m1']"
            ).text
            link = entry.find_element_by_xpath(
                "./div[@class='customStoryCard9-m__story-data__2qgWb']/a[contains(href,True)]"
            ).get_attribute("href")
            data_table = data_table.append(
                {"Headline": headline, "Datetime": datetime, "Link": link},
                ignore_index=True,
            )
    data_table.drop_duplicates(subset=["Link"], inplace=True)
    data_table.to_csv(
        os.path.join(out_dir, f"prothomalo_english_{month.lower()}_{year}.csv"),
        encoding=config.CSV_FILE_ENCODING,
        index=False,
    )
    return


def write_bengali_link_month(year, month, driver, out_dir):
    month = month.capitalize()
    print(year, month)
    month_day_dict = {
        "January": 31,
        "February": 28,
        "March": 31,
        "April": 30,
        "May": 31,
        "June": 30,
        "July": 31,
        "August": 31,
        "September": 30,
        "October": 31,
        "November": 30,
        "December": 31,
    }
    month_end_day = month_day_dict[month]
    wait = WebDriverWait(driver, config.DRIVER_WAIT_TIME)
    data_table = pd.DataFrame(columns=["Headline", "Datetime", "Link"])
    bengali_digit_lookup_table = {
        "১": "1",
        "২": "2",
        "৩": "3",
        "৪": "4",
        "৫": "5",
        "৬": "6",
        "৭": "7",
        "৮": "8",
        "৯": "9",
        "০": "0",
    }
    for start_date, end_date in [(i, i + 1) for i in list(range(1, month_end_day))]:
        print(f"dates between: {start_date}-{end_date}")
        repeat = True
        while repeat:
            start_date_class_attr = "react-datepicker__day react-datepicker__day--" + str(
                start_date
            ).zfill(
                3
            )
            end_date_class_attr = "react-datepicker__day react-datepicker__day--" + str(
                end_date
            ).zfill(3)
            driver.get("https://www.prothomalo.com/search")
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@class='label-with-arrow-m__label-with-arrow__2kufR']",
                    )
                )
            )
            k = driver.find_elements_by_xpath(
                "//div[@class='label-with-arrow-m__label-with-arrow__2kufR']"
            )[-1]
            driver.execute_script("arguments[0].click();", k)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@placeholder='শুরুর তারিখ']")
                )
            )
            k = driver.find_elements_by_xpath("//input[@placeholder='শুরুর তারিখ']")[-1]
            driver.execute_script("arguments[0].click();", k)
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']",
                    )
                )
            )
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//option[contains(text(),'{month}')]")
                )
            )
            select_year = Select(
                driver.find_element_by_xpath(
                    "//select[@class='react-datepicker__year-select']"
                )
            )
            select_year.select_by_visible_text(year)
            select_month = Select(
                driver.find_element_by_xpath(
                    "//select[@class='react-datepicker__month-select']"
                )
            )
            select_month.select_by_visible_text(month)
            while True:
                if (
                    month
                    in driver.find_elements_by_xpath(
                        "//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']"
                    )[0].text
                ):
                    break
                else:
                    time.sleep(2)
                    print("waiting 2 sec")
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//div[contains(@class,'{start_date_class_attr}')]")
                )
            )
            k = [
                i
                for i in driver.find_elements_by_xpath(
                    f"//div[contains(@class,'{start_date_class_attr}')]"
                )
                if "react-datepicker__day--outside-month"
                not in i.get_attribute("class").split()
            ][0]
            driver.execute_script("arguments[0].click();", k)

            k = driver.find_elements_by_xpath("//input[@placeholder='শেষ তারিখ']")[-1]
            driver.execute_script("arguments[0].click();", k)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//option[contains(text(),'{month}')]")
                )
            )
            select_month = Select(
                driver.find_element_by_xpath(
                    "//select[@class='react-datepicker__month-select']"
                )
            )
            select_month.select_by_visible_text(month)
            while True:
                if (
                    month
                    in driver.find_elements_by_xpath(
                        "//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']"
                    )[0].text
                ):
                    break
                else:
                    time.sleep(2)
                    print("waiting 2 sec")
            select_year = Select(
                driver.find_element_by_xpath(
                    "//select[@class='react-datepicker__year-select']"
                )
            )
            select_year.select_by_visible_text(year)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//div[contains(@class,'{end_date_class_attr}')]")
                )
            )
            k = [
                i
                for i in driver.find_elements_by_xpath(
                    f"//div[contains(@class,'{end_date_class_attr}')]"
                )
                if "react-datepicker__day--outside-month"
                not in i.get_attribute("class").split()
            ][0]
            driver.execute_script("arguments[0].click();", k)
            time.sleep(2)
            no_entries = driver.find_elements_by_xpath(
                "//div[@class='searchStories1AdWithLoadMore-m__label__2NcU1']/span"
            )[1].text
            entries = ""
            for digit in no_entries:
                entries += bengali_digit_lookup_table[digit]
            no_entries = int(entries)
            print(f"No of entries found:{no_entries}")
            while True:
                headings = driver.find_elements_by_xpath(
                    '//h2[@class="headline headline-type-27  story-headline  headline-m__headline__3vaq9 headline-m__headline-type-27__3ywG6"]'
                )
                elements = driver.find_elements_by_xpath(
                    '//span[@class="load-more-content more-m__content__1XWY0 more-m__bn-content__3Ppnx"]'
                )
                if len(elements) == 1:
                    driver.execute_script("arguments[0].click();", elements[0])
                    time.sleep(2)
                    headings = driver.find_elements_by_xpath(
                        '//h2[@class="headline headline-type-27  story-headline  headline-m__headline__3vaq9 headline-m__headline-type-27__3ywG6"]'
                    )
                elif len(headings) == no_entries:
                    print(
                        f"number of link:{len(headings)} equal no of entries:{no_entries}\n.Breaking from loop"
                    )
                    repeat = False
                    break
                else:
                    print(
                        f"number of link:{len(headings)} NOT equal of entries:{no_entries}\n.Breaking from loop and retrying"
                    )
                    break
        entries = driver.find_elements_by_xpath(
            "//div[@class='customStoryCard9-m__wrapper__yEFJV']"
        )
        print(f"Appending {len(entries)} entries")
        for entry in entries:
            headline = entry.find_element_by_xpath(
                ".//h2[@class='headline headline-type-27  story-headline  headline-m__headline__3vaq9 headline-m__headline-type-27__3ywG6']"
            ).text
            datetime = entry.find_element_by_xpath(
                ".//div[@class='story-meta-data storyMetaData-m__story-meta-data__2E2m1']"
            ).text
            link = entry.find_element_by_xpath(
                "./div[@class='customStoryCard9-m__story-data__2qgWb']/a[contains(href,True)]"
            ).get_attribute("href")
            data_table = data_table.append(
                {"Headline": headline, "Datetime": datetime, "Link": link},
                ignore_index=True,
            )
    data_table.drop_duplicates(subset=["Link"], inplace=True)
    data_table.to_csv(
        os.path.join(out_dir, f"prothomalo_bengali_{month.lower()}_{year}.csv"),
        encoding=config.CSV_FILE_ENCODING,
        index=False,
    )
    return


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--output-dir", help="output directory", type=str, required=True
    )
    parser.add_argument("--year", help="year", type=str, required=True)
    parser.add_argument(
        "--start-month", help="starting month", type=str, default="january"
    )
    parser.add_argument(
        "--end-month", help="stoping month", type=str, default="december"
    )
    parser.add_argument("--lang", help="en-English,bn-Bangal", type=str, required=True)
    parser.add_argument(
        "--month-list",
        help="specify comma separated list of full name of months in not providing range of month in start and end month. If spefied will overide range",
        type=str,
        default="",
    )
    args = parser.parse_args()
    save_csv_dir = args.output_dir
    n_month_start, n_month_end, n_year, lang = (
        args.start_month.lower(),
        args.end_month.lower(),
        args.year,
        args.lang,
    )
    driver = get_driver()
    if lang == "en":
        if args.month_list:
            month_list = args.month_list.split(",")
            for month in month_list:
                pass_month = month.strip().lower().capitalize()
                write_english_link_month(n_year, pass_month, driver, save_csv_dir)
        else:
            driver = get_driver()
            month_list = [
                "january",
                "february",
                "march",
                "april",
                "may",
                "june",
                "july",
                "august",
                "september",
                "october",
                "november",
                "december",
            ]
            start_index = month_list.index(n_month_start)
            end_index = month_list.index(n_month_end) + 1
            for month in month_list[start_index:end_index]:
                pass_month = month.strip().lower().capitalize()
                write_english_link_month(n_year, pass_month, driver, save_csv_dir)
    elif lang == "bn":
        if args.month_list:
            month_list = args.month_list.split(",")
            for month in month_list:
                pass_month = month.strip().lower().capitalize()
                write_bengali_link_month(n_year, pass_month, driver, save_csv_dir)
        else:
            month_list = [
                "january",
                "february",
                "march",
                "april",
                "may",
                "june",
                "july",
                "august",
                "september",
                "october",
                "november",
                "december",
            ]
            start_index = month_list.index(n_month_start)
            end_index = month_list.index(n_month_end) + 1
            for month in month_list[start_index:end_index]:
                pass_month = month.strip().lower().capitalize()
                write_bengali_link_month(n_year, pass_month, driver, save_csv_dir)
    driver.close()
    driver.quit()


if __name__ == "__main__":
    main()
