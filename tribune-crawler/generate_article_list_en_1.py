#for en only - from 1998 to Nov-2014 
import requests
from bs4 import BeautifulSoup
import bs4
import pandas 
from tqdm import tqdm
import config
import time
import os
import calendar
from pathlib import Path
from argparse import ArgumentParser

def create_directory(path):
	try:
		Path(path).mkdir(parents=True, exist_ok=True)
		return True
	except FileExistsError as fe_error:
		return True
	except OSError as error:
		print(error)
	return False

def write_link_month(lang,year, month, out_dir,log):
	df=pandas.DataFrame(columns=['Page-name','Date','Link'])
	lang_dict={"en":"english"}
	month_code=time.strptime(month,'%B').tm_mon
	month_code="{:02d}".format(month_code)
	last_date= calendar.monthrange(int(year),int(month_code))[1]
	sub_pages=["biz","delhi","chd","cth1","cth2","battrib","calendar","bathinda","asrtrib","kashmir","ldh","ldh1","jmtrib","latest-news","jobs","j&k","jaltrib","index","main1","main2","main3","main4","main5","main6","main7","main8","main9","main10","health","harayana","himplus","himachal","jal","dplus","edit","dun","sports","nation","ttlife","ttlife1","punjab","letters","region","world"]

	for d in range(1,last_date+1):
		full_date=year+month_code+"{:02d}".format(d)
		for sub in sub_pages:
			link="https://www.tribuneindia.com/"+year+"/"+full_date+"/"+sub+".htm"
			df = df.append({"Page-name": sub,"Date": full_date ,"Link": link},ignore_index=True,)
	if not os.path.exists(out_dir):
		create_directory(out_dir)
	df.drop_duplicates(subset=["Link"], inplace=True)
	df.to_csv(
		os.path.join(out_dir, f"tribune_{lang_dict[lang]}_{month.lower()}_{year}.csv"),
		encoding=config.CSV_FILE_ENCODING,
		index=False,
	)
	print(f"\nFile tribune_{lang_dict[lang]}_{month.lower()}_{year}.csv is committed with {df.shape[0]} entries. \n")
	return

def main():
	parser = ArgumentParser()
	parser.add_argument("--log", help="will print log",action="store_true")
	parser.add_argument("--output-dir", help="output directory", type=str, default="")
	parser.add_argument("--lang-code", help="Language Code - bn,hi,en", type=str, required=True)
	parser.add_argument("--year", help="Year in YYYY format", type=str, required=True)
	parser.add_argument("--month", help="Month ", type=str, required=True)
	args = parser.parse_args()
	log=args.log
	n_lang=args.lang_code
	n_year=args.year
	pass_month=args.month
	save_csv_dir = args.output_dir
	if len(save_csv_dir)==0 : save_csv_dir="article_list/"+str(n_year)+"/"+str(pass_month)+" "+str(n_year)+"/"
	write_link_month(n_lang,n_year, pass_month, save_csv_dir,log) 
	
if __name__ == "__main__":
	main()