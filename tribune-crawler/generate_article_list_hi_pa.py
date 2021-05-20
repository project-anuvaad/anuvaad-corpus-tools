#for hi,pa only
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

def link_gen(lang):
	if lang=="hi": return "https://www.dainiktribuneonline.com/"
	if lang=="pa": return "https://www.punjabitribuneonline.com/"

def write_link_month(lang,year, month, out_dir,log):
	df=pandas.DataFrame(columns=['Headline','Datetime','Link'])
	lang_dict={"en":"english","hi":'hindi','pa':'punjabi'}
	month_code=time.strptime(month,'%B').tm_mon
	month_code="{:02d}".format(month_code)
	last_date= calendar.monthrange(int(year),int(month_code))[1]

	s_date=["01","06","11","16","21","26"]
	e_date=["05","10","15","20","25",str(last_date)]

	for st,end in zip(s_date,e_date):
		s_date_full=st+"/"+month_code+"/"+year
		e_date_full=end+"/"+month_code+"/"+year

		myobj = {'FromDate': s_date_full,'ToDate': e_date_full}
		url = link_gen(lang)+"archive"

		markup_string = requests.post(url, data = myobj).content
		soup = BeautifulSoup(markup_string, "lxml")
		entries=soup.findAll(class_="col-lg-12 col-md-12 col-sm-12 archive-news-item")
		if log :print(s_date_full,"-",e_date_full,"-",len(entries),"entries")
		for ent in entries:
			headline=ent.find("h4").text.strip()
			date=ent.find(class_="card-time").text.strip()
			link=link_gen(lang)
			link+=ent.find(class_="card-top-align")["href"].strip()
			df = df.append({"Headline": headline,"Datetime": date ,"Link": link},ignore_index=True,)
				
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