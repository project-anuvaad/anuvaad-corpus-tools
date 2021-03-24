import requests
import time
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
import copy
from argparse import ArgumentParser

def scraper(month,year,lang_code,inp_dir,save_dir,count,log):

	articles_data = pd.read_csv(str(inp_dir),encoding='utf-16')
	print("total no of links to be scraped - "+str(int(articles_data.shape[0])-count)+" from-"+str(count)+" to-"+str(int(articles_data.shape[0])-1))
	start_time = time.time()
	para_flag=0

	for link in articles_data['Link'][count:]:
		
		markup_string = requests.get(link, stream=True).content
		soup = BeautifulSoup(markup_string, "html.parser")
		head=[]
		head.append(soup.find(class_='articleheading'))
		if soup.find(class_='oi-article-rt') is None :
			count +=1 
			continue
		else:
			head.extend(soup.find(class_='oi-article-rt').findAll(['p','strong','h2']))

		unwanted_lines=set()
		unwanted_class=["author-profile written-by","author-profile","written-by"]
		unwanted_class=set(unwanted_class)
		for n in range(len(head)) :
			if head[n].parent.get('class') is not None:
				if len(unwanted_class.intersection(set(head[n].parent.get('class')))) != 0:
					unwanted_lines.add(n)
					continue
			if head[n].parent.parent.get('class') is not None:
				if len(unwanted_class.intersection(set(head[n].parent.parent.get('class')))) != 0 :
					unwanted_lines.add(n)
					continue
			if head[n].get('class') is not None:
				if "widgetHeading" in head[n].get('class'):
					unwanted_lines.add(n)

		for i in sorted(unwanted_lines,reverse=True):
			del head[i]

		if not os.path.exists(save_dir):
			os.makedirs(str(save_dir))
		with open(os.path.join(str(save_dir), f"goodreturns-{month[:3]}-{year}-{count}.txt"), mode="w", encoding="utf-16") as file_w:
			for text in range(len(head)):
				file_w.write(head[text].text.strip() + "\r\n")
			if log :print(f"goodreturns-{month[:3]}-{year}-{count}-.txt")
			count+=1
		
	time_taken=time.time() - start_time			
	print("Time Take - ",time_taken//60," minutes ",time_taken%60," seconds")
	return

def main():
	parser = ArgumentParser()
	parser.add_argument("--lang-code", help="Language Code - bn,hi,en", type=str, required=True)
	parser.add_argument("--year", help="Year in YYYY format", type=str, required=True)
	parser.add_argument("--month", help="Month ", type=str, required=True)
	parser.add_argument("--count", help="count to start from", type=int, default=0)
	parser.add_argument("--log", help="will print log",action="store_true")
	parser.add_argument("--input-csv",help="csv file to be scraped",type=str ,default="")
	parser.add_argument("--output-dir", help="output directory", type=str, default="")
	lang_full = {'en':'english','te':'telugu','hi':'hindi','ta':'tamil','ml':'malayalam','kn':'kannada'}
	args = parser.parse_args()
	lang_code=args.lang_code
	year=args.year
	month=args.month
	count=args.count
	inp_dir=args.input_csv
	save_dir=args.output_dir
	if len(inp_dir)==0  : inp_dir="article_list/"+str(year)+"/"+str(month)+" "+str(year)+"/"+f"goodreturns_{lang_full[lang_code]}_{month.lower()}_{year}.csv"
	if len(save_dir)==0 : save_dir="scraped_files/"+str(year)+"/"+str(month)+" "+str(year)+"/"+lang_full[lang_code]
	log=args.log
	scraper(month,year,lang_code,inp_dir,save_dir,count,log)

if __name__ == "__main__":
	main()