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

def create_directory(path):
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except FileExistsError as fe_error:
        return True
    except OSError as error:
        print(error)
    return False


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


def write_link_month(lang,year, month, driver, out_dir, full_log):

	lang_full = {'en':'english','bn':'bengali','hi':'hindi'}

	month_code=time.strptime(month,'%B').tm_mon
	start_from=[]
	end_to=[]

	start_from.append("01."+"{:02d}".format(month_code)+'.'+year)
	start_from.append("11."+"{:02d}".format(month_code)+'.'+year)
	start_from.append("21."+"{:02d}".format(month_code)+'.'+year)

	last_date= calendar.monthrange(int(year),int(month_code))[1]
	#end_to= "{:02d}".format(last_date)+"."+"{:02d}".format(month_code)+'.'+year
	end_to.append("10."+"{:02d}".format(month_code)+'.'+year)
	end_to.append("20."+"{:02d}".format(month_code)+'.'+year)
	end_to.append("{:02d}".format(last_date)+"."+"{:02d}".format(month_code)+'.'+year)

	data_table = pd.DataFrame(columns=["Headline", "Datetime", "Link"])

	if full_log : print("\n----------------",year, month, lang_full[lang],"----------------\n")

	for i in range(0,3):  
		wait = WebDriverWait(driver, config.DRIVER_WAIT_TIME)
		repeat = True
		if full_log : print("------",start_from[i],"to", end_to[i],"----")

		while repeat:
			count=1
			driver.get("https://www.dw.com/search/?languageCode="+lang+"&from="+start_from[i]+"&to="+end_to[i]+"&sort=DATE&resultsCounter=100")

			time.sleep(5)

			while True:
				elements = driver.find_elements_by_xpath('//a[@class="addPage"]/span')
				if len(elements) == 1:
					entries = driver.find_elements_by_xpath("//div[@class='searchResult']")
					if full_log :print(f"{len(entries)}-",end="")
					driver.execute_script("arguments[0].click();", elements[0])
					time.sleep(10)
					entries = driver.find_elements_by_xpath("//div[@class='searchResult']")
				else:
					if full_log :print(f"{len(entries)}-",end="")
					repeat=False
					break
			entries = driver.find_elements_by_xpath("//div[@class='searchResult']")
			if full_log : print(f"Appending {len(entries)} entries\n")
			for ent in entries :
				headline = ent.find_element_by_xpath(".//h2").text
				datetime = ent.find_element_by_xpath(".//span[@class='date']").text
				headline = headline.replace(datetime,"").strip()
				link = ent.find_element_by_xpath("./a[contains(href,True)]").get_attribute("href")
				data_table = data_table.append({"Headline": headline, "Datetime": datetime, "Link": link},ignore_index=True,)

	create_dir="article_list/"+str(year)+"/"+str(month)+" "+str(year)+"/"
	if not os.path.exists(create_dir):
		print("creating directory...")
		create_directory(create_dir)
	out_dir+=create_dir

	data_table.drop_duplicates(subset=["Link"], inplace=True)
	data_table.to_csv(
		os.path.join(out_dir, f"dw_{lang_full[lang]}_{month.lower()}_{year}.csv"),
		encoding=config.CSV_FILE_ENCODING,
		index=False,
	)
	print(f"{create_dir}/dw_{lang_full[lang]}_{month.lower()}_{year}.csv has been committed with {data_table.shape[0]} entries.")
	
	return




def main():
	parser = ArgumentParser()
	parser.add_argument("--log", help="will print log",action="store_true")
	parser.add_argument("--output-dir", help="output directory", type=str, required=True)
	parser.add_argument("--lang-code", help="Language Code - bn,hi,en", type=str, required=True)
	parser.add_argument("--year", help="Year in YYYY format", type=str, required=True)
	parser.add_argument("--month", help="Month ", type=str, required=True)
	args = parser.parse_args()
	n_lang=args.lang_code
	n_year=args.year
	pass_month=args.month
	save_csv_dir = args.output_dir
	log=args.log
	
	driver = get_driver()
	write_link_month(n_lang,n_year, pass_month, driver, save_csv_dir,log)
	driver.close()
	driver.quit()

if __name__ == "__main__":
	main()
