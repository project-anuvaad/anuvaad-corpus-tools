import pandas as pd
import config
import time
import os
import calendar
from pathlib import Path
from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

lang_dict = {'en':'english','hi':'hindi','kn':'kannada','te':'telugu','ml':'malayalam','ta':'tamil'}

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

def create_directory(path):
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except FileExistsError as fe_error:
        return True
    except OSError as error:
        print(error)
    return False

def link_prepare(lang):
	link=""
	if lang=="en":
		link+="https://www.goodreturns.in/"
	else :
		link+="https://"
		link+=str(lang_dict[lang])
		link+=".goodreturns.in/"
	return link

def write_link_month(lang,year, month, driver, out_dir, log): 

	link=link_prepare(lang)
	month_code=time.strptime(month,'%B').tm_mon
	month_code="{:02d}".format(month_code)
	last_date= calendar.monthrange(int(year),int(month_code))[1]

	data_table = pd.DataFrame(columns=["Headline","Datetime", "Link"])

	print("\n----------------",year, month, lang_dict[lang],"----------------\n")

	for day in range(1,last_date+1):
		day="{:02d}".format(day)
		date= str(year) + "/" + str(month_code) + "/" + str(day) 
		day_link = link +date+ "/"
		
		wait = WebDriverWait(driver, config.DRIVER_WAIT_TIME)

		driver.get(day_link)

		time.sleep(3)

		entries = driver.find_elements_by_xpath("//ul[@class='dayindexTitle']/li")
			
		print(f"{date} - {len(entries)} entries ... ",end='')
		
		for ent in entries :
			headline = ent.find_element_by_xpath(".//a").text
			hlink = ent.find_element_by_xpath("./a[contains(href,True)]").get_attribute("href")
			data_table = data_table.append({"Headline": headline,"Datetime": date ,"Link": hlink},ignore_index=True,)

		print("Appended Successfully")
	if not os.path.exists(out_dir):
		create_directory(out_dir)
	data_table.drop_duplicates(subset=["Link"], inplace=True)
	data_table.to_csv(
		os.path.join(out_dir, f"goodreturns_{lang_dict[lang]}_{month.lower()}_{year}.csv"),
		encoding=config.CSV_FILE_ENCODING,
		index=False,
	)
	print(f"\nFile goodreturns_{lang_dict[lang]}_{month.lower()}_{year}.csv is committed with {data_table.shape[0]} entries at dir = {out_dir}. \n")

	return




def main():
	parser = ArgumentParser()
	parser.add_argument("--log", help="will print log",action="store_true")
	parser.add_argument("--output-dir", help="output directory", type=str, default="")
	parser.add_argument("--lang-code", help="Language Code - bn,hi,en", type=str, required=True)
	parser.add_argument("--year", help="Year in YYYY format", type=str, required=True)
	parser.add_argument("--month", help="Month ", type=str, required=True)
	args = parser.parse_args()
	n_lang=args.lang_code
	n_year=args.year
	pass_month=args.month
	save_csv_dir = args.output_dir
	log=args.log
	if len(save_csv_dir)==0 : save_csv_dir="article_list/"+str(n_year)+"/"+str(pass_month)+" "+str(n_year)+"/"
	driver = get_driver()
	write_link_month(n_lang,n_year, pass_month, driver, save_csv_dir, log) 
	driver.close()
	driver.quit()

if __name__ == "__main__":
	main()
