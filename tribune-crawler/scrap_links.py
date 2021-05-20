import requests
import time
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
import bs4
import copy
from argparse import ArgumentParser

def retry_scraper(month,year,lang_code,inp_dir,save_dir,log,count_list):
	countlistx1=list()
	articles_data = pd.read_csv(str(inp_dir),encoding='utf-16-le')
	print("total no of links to be scraped - ",len(count_list))
	start_time = time.time()
	for count in count_list:
		link=articles_data.iloc[int(count)]['Link']
		#print("--->",count,link)
		try:
			markup_string = requests.get(link, stream=True).content
			soup = BeautifulSoup(markup_string, "lxml")
			head=[]
			try:
				head.extend(soup.find(class_="glb-heading"))		#Headline
			except:
				y=True
				pass
			try:
				head.extend(soup.find(class_="story-desc"))		#Headline
			except:
				if y==True:
					print(count,link)
			head=list(filter(None,head))
			if not os.path.exists(str(save_dir)):
				os.makedirs(str(save_dir))
			with open(os.path.join(str(save_dir), f"TOI-{lang_code}-{month[:3]}-{year}-{count}.txt"), mode="w", encoding="utf-16") as file_w:
				for text in range(len(head)):
					try:
						file_w.write(head[text].text.strip() + "\r\n")
					except:
						pass
				if log : print(f"tribune-{lang_code}-{month[:3]}-{year}-{count}.txt")
		except:
			print(count,":error---------",link)
			countlistx1.append(count)
			
	time_taken=time.time() - start_time
	print("total errors occured :",len(countlistx1))
	if len(countlistx1)>0: print("error occured at count :",countlistx1)				
	print("Time Take - ",int(time_taken//60)," minutes ",int(time_taken%60)," seconds")
	return

def scraper(month,year,lang_code,inp_dir,save_dir,count,log,retry):
	countlistx=list()
	articles_data = pd.read_csv(str(inp_dir),encoding='utf-16-le')
	print("total no of links to be scraped - "+str(int(articles_data.shape[0])-count)+" from-"+str(count)+" to-"+str(int(articles_data.shape[0])-1))
	start_time = time.time()
	for link in articles_data['Link'][count:]:
		#print(link)
		try:
			markup_string = requests.get(link, stream=True).content
			soup = BeautifulSoup(markup_string, "lxml")
			head=[]
			try:
				head.extend(soup.find(class_="glb-heading"))		#Headline
			except:
				y=True
				pass
			try:
				head.extend(soup.find(class_="story-desc"))		#Headline
			except:
				if y==True:
					print(count,link)
			head=list(filter(None,head))
			if not os.path.exists(str(save_dir)):
				os.makedirs(str(save_dir))
			with open(os.path.join(str(save_dir), f"TOI-{lang_code}-{month[:3]}-{year}-{count}.txt"), mode="w", encoding="utf-16") as file_w:
				for text in range(len(head)):
					try:
						file_w.write(head[text].text.strip() + "\r\n")
					except:
						pass
				if log : print(f"tribune-{lang_code}-{month[:3]}-{year}-{count}.txt")
				count+=1
		except:
			print(count,"error---------",link)
			countlistx.append(count)
			count+=1

	time_taken=time.time() - start_time
	print("total errors occured :",len(countlistx))
	if len(countlistx)>0: print("error occured at count :",countlistx)		
	print("Time Take - ",int(time_taken//60)," minutes ",int(time_taken%60)," seconds")
	if retry and len(countlistx)>0:
		print("retrying... above counts")
		retry_scraper(month,year,lang_code,inp_dir,save_dir,log,countlistx)
	return

def main():
	parser = ArgumentParser()
	parser.add_argument("--lang-code", help="Language Code - bn,hi,en", type=str, required=True)
	parser.add_argument("--year", help="Year in YYYY format", type=str, required=True)
	parser.add_argument("--month", help="Month ", type=str, required=True)
	parser.add_argument("--count", help="count to start from", type=int, default=0)
	parser.add_argument("--log", help="will print log",action="store_true")
	parser.add_argument("--retry-failed", help="will print log",action="store_true")
	parser.add_argument("--count-list", help="enter count of the list to ",default="")
	parser.add_argument("--input-csv",help="csv file to be scraped",type=str ,default="")
	parser.add_argument("--output-dir", help="output directory", type=str, default="")
	lang_full = {'en':'english','gu':'gujarati','hi':'hindi','mr':'marathi','kn':'kannada','bn':'bengali','gu':'gujarati','ml':'malayalam','te':'telugu','ta':'tamil','pa':'punjabi'}
	args = parser.parse_args()
	lang_code=args.lang_code
	year=args.year
	month=args.month
	count=args.count
	count_list=args.count_list
	retry_failed=args.retry_failed
	inp_dir=args.input_csv
	save_dir=args.output_dir
	if len(inp_dir)==0  : inp_dir="article_list/"+str(year)+"/"+str(month)+" "+str(year)+"/"+f"tribune_{lang_full[lang_code]}_{month.lower()}_{year}.csv"
	if len(save_dir)==0 : save_dir="scraped_files/"+str(year)+"/"+str(month)+" "+str(year)+"/"+lang_full[lang_code]
	log=args.log
	if count_list == "":
		scraper(month,year,lang_code,inp_dir,save_dir,count,log,retry_failed)
	else:
		count_list=count_list.split(",")
		retry_scraper(month,year,lang_code,inp_dir,save_dir,log,count_list)

if __name__ == "__main__":
	main()