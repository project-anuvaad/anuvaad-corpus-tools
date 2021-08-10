import requests
import time
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
import bs4
import copy
from argparse import ArgumentParser

def scraper(month,year,lang_code,inp_dir,save_dir,count,log,stopcount):
	list_c=list()
	articles_data = pd.read_csv(str(inp_dir),encoding='utf-16-le')
	if stopcount!=None : print("total no of links to be scraped - "+str(stopcount-count)+" from-"+str(count)+" to-"+str(stopcount))
	else : print("total no of links to be scraped - "+str(int(articles_data.shape[0])-count)+" from-"+str(count)+" to-"+str(int(articles_data.shape[0])-1))
	start_time = time.time()
	for link in articles_data['Link'][count:stopcount]:
		#print(link)
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
			markup_string = requests.get(link,headers=headers, stream=True).content
			soup = BeautifulSoup(markup_string, "html.parser")
			head=[]
			try:
				head.extend(soup.find(['h1'],class_="article-heading"))		#Headline
			except:
				pass
			try:
				head.extend(soup.find(['h1'],class_="article-h1"))		#Headline1
			except:
				pass
			try:
				head.extend(soup.findAll(['p'],class_="margin-bt10px"))		#sub-head  
			except:
				pass
			try:
				head.extend(soup.findAll(['p'],class_="article_sum"))		#sub-head2  
			except:
				pass
			try:
				head.extend(soup.findAll(['div'],class_="field-item even"))		#para
			except:
				pass
			try:
				head.extend(soup.findAll(['ol'],class_="special"))		#Highlights    
			except:
				pass
			try:
				head.extend(soup.findAll(['ul'],class_="high"))		#Highlights2    
			except:
				pass
			try:
				head.extend(soup.findAll(['h1'],class_="article-heading margin-bt10px"))		#vid-head
			except:
				pass
			head=list(filter(None,head))

			if not os.path.exists(str(save_dir)):
				os.makedirs(str(save_dir))
			with open(os.path.join(str(save_dir), f"ZEE-{lang_code}-{month[:3]}-{year}-{count}.txt"), mode="w", encoding="utf-8") as file_w:
				for text in range(len(head)):
					try:
						file_w.write(head[text].text.strip() + "\r\n")
					except:
						try:
							file_w.write(head[text].string + "\r\n")
						except:
							if log : print('---error-while-encoding-occured---')
			if log : 
				if os.stat(os.path.join(str(save_dir), f"ZEE-{lang_code}-{month[:3]}-{year}-{count}.txt")).st_size == 0:
					print(count,"empty", link)
				else:
						print(f"ZEE-{lang_code}-{month[:3]}-{year}-{count}.txt")
			count+=1
		except:
			print(count,"error",link)
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
	if len(inp_dir)==0  : inp_dir="article_list/"+str(year)+"/"+str(month[:3])+" "+str(year)+"/"+f"ZEE_{lang_code}_{month.lower()}_{year}.csv"
	if len(save_dir)==0 : save_dir="scraped_files/"+str(year)+"/"+str(month)+" "+str(year)+"/"+lang_full[lang_code]
	log=args.log
	scraper(month,year,lang_code,inp_dir,save_dir,count,log,stopcount)

if __name__ == "__main__":
	main()


'''
<h1 class="article-heading">Healt writes to Home Minister Amit Shah</h1>
<p class="margin-bt10px">IMA said that healthcare violence</p>
<div class="field-item even"
<ol class="special"
<h1 class="article-heading margin-bt10px" 
'''