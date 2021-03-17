import requests
import time
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
import copy
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

def scraper(month,year,lang_code,inp_dir,save_dir,count,log):

	articles_data = pd.read_csv(str(inp_dir),encoding='utf-16')
	print("total no of links to be scraped - "+str(int(articles_data.shape[0])-count)+" from-"+str(count)+" to-"+str(int(articles_data.shape[0])-1))
	start_time = time.time()
	para_flag=0

	for link in articles_data['Link'][count:]:
		
		markup_string = requests.get(link, stream=True).content
		soup = BeautifulSoup(markup_string, "html.parser")
		head=[]
		if soup.find(class_='col3').findAll(['h1']) is not None :
			head = soup.find(class_='col3').findAll(['h1'])
		#head = soup.find(class_='col3').findAll(['h1']) #heading
		if soup.find(['p'],class_='intro') is not None :
			head.append(soup.find(['p'],class_='intro')) #introduction
		para=[]
		try:
			para=soup.select(".group > .longText") #paragraph-selectiom
		except:
			para_flag=1
		try:
			para[0].find(class_='gallery col3').decompose() #misc-removing
		except:
			pass
		try:
			para[0].find(class_='sharing-bar').decompose() #sharebar-removing
		except:
			pass
		try:
			para[0].find(class_='teaserContentWrap share').decompose() #sharebar-removing
		except:
			pass
		try:
			for z in range(len(para[0].findAll(class_='picBox full'))):
				para[0].find(class_='picBox full').decompose() #picturebox-removing
		except:
			pass
		try:
			for z in range(len(para[0].findAll(['script']))):
				para[0].find('script').decompose() #script-removing
		except:
			pass
		try:
			for z in range(len(para[0].findAll(['input']))):
				para[0].find('input').decompose() #input-removing
		except:
			pass

		if para_flag != 1 and len(para)!=0:
			for j in range(len(para[0].findAll('a'))): #paragraph-filtering
				try:
					para[0].find('a').parent.decompose()
					continue
				except:
					break
			head.extend(para[0].findAll('p'))
			#head=head[:-1] #unwanted-line

		if not os.path.exists(save_dir):
			os.makedirs(str(save_dir))
		with open(os.path.join(str(save_dir), f"DW-{month[:3]}-{year}-{count}.txt"), mode="w", encoding="utf-16") as file_w:
			for text in range(len(head)):
				file_w.write(head[text].text.strip() + "\r\n")
			if log :print(f"DW-{month[:3]}-{year}-{count}-.txt")
			count+=1
		para_flag=0
		

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
	lang_full = {'en':'english','bn':'bengali','hi':'hindi'}
	args = parser.parse_args()
	lang_code=args.lang_code
	year=args.year
	month=args.month
	count=args.count
	inp_dir=args.input_csv
	save_dir=args.output_dir
	if len(inp_dir)==0  : inp_dir="article_list/"+str(year)+"/"+str(month)+" "+str(year)+"/"+f"dw_{lang_full[lang_code]}_{month.lower()}_{year}.csv"
	if len(save_dir)==0 : save_dir="scraped_files/"+str(year)+"/"+str(month)+" "+str(year)+"/"+lang_full[lang_code]
	log=args.log
	scraper(month,year,lang_code,inp_dir,save_dir,count,log)

if __name__ == "__main__":
	main()
