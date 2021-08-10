import requests
import time
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
import bs4
import copy
from argparse import ArgumentParser

def tags(lang):
	if lang == "en":
		return ["ga-headlines","Normal","_23498","_1Y-96","_3p5Tz img_cptn","_2ZigF id-r-highlights","_3YYSt clearfix"]
	else:
		return ["headline","articleBody","caption text_ellipsis","section tpstory_title","description","section tpstory_title"]

def scraper(month,year,lang_code,inp_dir,save_dir,count,log,stopcount):
	list_c=list()
	articles_data = pd.read_csv(str(inp_dir),encoding='utf-16-le')
	if stopcount!=None : print("total no of links to be scraped - "+str(stopcount-count)+" from-"+str(count)+" to-"+str(stopcount))
	else : print("total no of links to be scraped - "+str(int(articles_data.shape[0])-count)+" from-"+str(count)+" to-"+str(int(articles_data.shape[0])-1))
	start_time = time.time()
	for link in articles_data['Link'][count:stopcount]:
		#print(link)
		try:
			markup_string = requests.get(link, stream=True).content
			soup = BeautifulSoup(markup_string, "html.parser")
			head=[]
			try:
				head.extend(soup.findAll(['arttitle']))		#Headline
			except:
				pass
			for i in tags(lang_code):
				try:
					if i == "headline" or i == "articleBody" or i == "description" : head.extend(soup.findAll(attrs={"itemprop":i}))
					head.extend(soup.findAll(class_=i))
				except:
					pass
			head=list(filter(None,head))

			if not os.path.exists(str(save_dir)):
				os.makedirs(str(save_dir))
			with open(os.path.join(str(save_dir), f"TOI-{lang_code}-{month[:3]}-{year}-{count}.txt"), mode="w", encoding="utf-16") as file_w:
				for text in range(len(head)):
					try:
						try:
							if " ".join(head[text]['class']) == "_2ZigF id-r-highlights":
								try:
									file_w.write(head[text].get_text("\n",strip=True) + "\r\n")
								except:
									print("->",file_w.write(head[text].text.strip() + "\r\n"))
							else:
								file_w.write(head[text].text.strip() + "\r\n")
						except:
							file_w.write(head[text].text.strip() + "\r\n")
					except:
						if log : print('---error-while-encoding-occured---')
				if log : print(f"TOI-{lang_code}-{month[:3]}-{year}-{count}.txt")
				count+=1
		except:
			print(count,"----------",link)
			list_c.append(count)
			count+=1
	print("Total error :",len(list_c))
	if len(list_c)>0 : print("error counts are :",list_c)	
	time_taken=time.time() - start_time			
	print("Time Take - ",time_taken//60," minutes ",time_taken%60," seconds")
	return

def main():
	parser = ArgumentParser()
	parser.add_argument("--lang-code", help="Language Code - bn,hi,en", type=str, required=True)
	parser.add_argument("--year", help="Year in YYYY format", type=str, required=True)
	parser.add_argument("--month", help="Month ", type=str, required=True)
	parser.add_argument("--start-count", help="count to start from", type=int, default=0)
	parser.add_argument("--stop-count", help="count to start from", type=int, default=None)
	parser.add_argument("--log", help="will print log",action="store_true")
	parser.add_argument("--input-csv",help="csv file to be scraped",type=str ,default="")
	parser.add_argument("--output-dir", help="output directory", type=str, default="")
	lang_full = {'en':'english','gu':'gujarati','hi':'hindi','mr':'marathi','kn':'kannada','bn':'bengali','gu':'gujarati','ml':'malayalam','te':'telugu','ta':'tamil'}
	args = parser.parse_args()
	lang_code=args.lang_code
	year=args.year
	month=args.month
	count=args.start_count
	stopcount=args.stop_count
	inp_dir=args.input_csv
	save_dir=args.output_dir
	if len(inp_dir)==0  : inp_dir="article_list/"+str(year)+"/"+str(month)+" "+str(year)+"/"+f"TOI_{lang_full[lang_code]}_{month.lower()}_{year}.csv"
	if len(save_dir)==0 : save_dir="scraped_files/"+str(year)+"/"+str(month)+" "+str(year)+"/"+lang_full[lang_code]
	log=args.log
	scraper(month,year,lang_code,inp_dir,save_dir,count,log,stopcount)

if __name__ == "__main__":
	main()