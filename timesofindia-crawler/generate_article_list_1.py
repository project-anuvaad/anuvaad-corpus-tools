# use for lang - bn,gu,kn,ml,ta,te
import pandas as pd
import bs4
import requests
from argparse import ArgumentParser
import time
import os
import sys
import config

parser = ArgumentParser()
parser.add_argument("--output-dir", help="output directory", type=str, default="")
parser.add_argument("--lang-code", help="language code - bn,ta,te,ml,gu,kn", type=str, required=True)
parser.add_argument("--year", help="Year in YYYY format", type=str, required=True)
parser.add_argument("--month", help="Month ", type=str, required=True)
args = parser.parse_args()
year=args.year
lang=args.lang_code
month=args.month
save_csv_dir = args.output_dir
lang_codes=["bn","ta","te","ml","gu","kn"]
if lang not in lang_codes:
	print("currently only supports bn,ta,te,ml,kn,gu langs")
	sys.exit(1)
if save_csv_dir=="":
	save_csv_dir=f"article_list/{year}/{month} {year}"
month_code=time.strptime(month,'%B').tm_mon
month_code="{:02d}".format(month_code)

data_table = pd.DataFrame(columns=["Datetime", "Link"])
if lang=="bn" : link=f"https://eisamay.indiatimes.com/staticsitemap/eisamay/{year}-{month.capitalize()}.xml";link1=f"https://eisamay.indiatimes.com/staticsitemap/eisamayvideo/{year}-{month.capitalize()}.xml"
if lang=="te" : link=f"https://telugu.samayam.com/staticsitemap/telugu/{year}-{month.capitalize()}.xml";link1=f"https://telugu.samayam.com/staticsitemap/teluguvideo/{year}-{month.capitalize()}.xml"
if lang=="ta" : link=f"https://tamil.samayam.com/staticsitemap/tamil/{year}-{month.capitalize()}.xml";link1=f"https://tamil.samayam.com/staticsitemap/tamilvideo/{year}-{month.capitalize()}.xml"
if lang=="ml" : link=f"https://malayalam.samayam.com/staticsitemap/malayalam/{year}-{month.capitalize()}.xml";link1=f"https://malayalam.samayam.com/staticsitemap/malayalamvideo/{year}-{month.capitalize()}.xml"
if lang=="gu" : link=f"https://www.iamgujarat.com/staticsitemap/iag/{year}-{month.capitalize()}.xml";link1=f"https://www.iamgujarat.com/staticsitemap/iagvideo/{year}-{month.capitalize()}.xml"
if lang=="kn" : link=f"https://vijaykarnataka.com/staticsitemap/vk/{year}-{month.capitalize()}.xml";link1=f"https://vijaykarnataka.com/staticsitemap/vkvideo/{year}-{month.capitalize()}.xml"

#gu - old = startlink='https://www.iamgujarat.com/tilsitemap/'+year+'-sitemap/' = link='https://www.iamgujarat.com/tilsitemap/'+year+'-'+str(i)+'-sitemap/'

markup_string = requests.get(link, stream=True).content
soup = bs4.BeautifulSoup(markup_string, "xml")
url_list=soup.findAll(['url'])
for url in url_list:
	date=url.lastmod.text.strip()
	hlink=url.loc.text.strip()
	data_table = data_table.append({"Datetime": date ,"Link": hlink},ignore_index=True,)
print(data_table.shape[0])
markup_string = requests.get(link1, stream=True).content
soup = bs4.BeautifulSoup(markup_string, "xml")
url_list=soup.findAll(['url'])
for url in url_list:
	date=url.video.publication_date.text.strip()
	hlink=url.loc.text.strip()
	data_table = data_table.append({"Datetime": date ,"Link": hlink},ignore_index=True,)
data_table.drop_duplicates(subset=["Link"], inplace=True)
data_table.to_csv(os.path.join(save_csv_dir, f"TOI_{lang}_{month.lower()}_{year}.csv"),encoding=config.CSV_FILE_ENCODING,index=False,)
print(f"\nFile TOI_{lang}_{month.lower()}_{year}.csv is committed with {data_table.shape[0]} entries. \n")






















'''
00-   
01-	  8,7,6,5
02-   3,4,5
03-   03,02
04-   01,02

'''