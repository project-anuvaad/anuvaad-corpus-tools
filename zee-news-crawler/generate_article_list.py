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
parser.add_argument("--lang-code", help="language code - en,bn,ta,te,ml,gu,kn,mr,hi", type=str, required=True)
parser.add_argument("--year", help="Year in YYYY format", type=str, required=True)
parser.add_argument("--month", help="Month ", type=str, required=True)
args = parser.parse_args()
year=args.year
lang=args.lang_code
month_full=args.month
month=month_full.lower()[:3]
save_csv_dir = args.output_dir
if save_csv_dir=="":
	save_csv_dir=f"article_list/{year}/{month} {year}"
	try:
		os.makedirs(save_csv_dir)
	except:
		pass

data_table = pd.DataFrame(columns=["Datetime", "Link"])
if lang=="en" : link=f"https://zeenews.india.com/sitemaps/{year}-{month}-video-sitemap.xml";link1=f"https://zeenews.india.com/sitemaps/sitemap-{year}-{month}.xml"
elif lang=="hi" : link=f"https://zeenews.india.com/hindi/sitemaps/{year}-{month}-video-sitemap.xml";link1=f"https://zeenews.india.com/hindi/sitemaps/sitemap-{year}-{month}.xml"
elif lang=="mr" : link=f"https://zeenews.india.com/marathi/sitemaps/{year}-{month}-video-sitemap.xml";link1=f"https://zeenews.india.com/marathi/sitemaps/sitemap-{year}-{month}.xml"
elif lang=="bn" : link=f"https://zeenews.india.com/bengali/sitemaps/{year}-{month}-video-sitemap.xml";link1=f"https://zeenews.india.com/bengali/sitemaps/sitemap-{year}-{month}.xml"
elif lang=="ta" : link=f"https://zeenews.india.com/tamil/sitemaps/{year}-{month}-video-sitemap.xml";link1=f"https://zeenews.india.com/tamil/sitemaps/sitemap-{year}-{month}.xml"
elif lang=="te" : link=f"https://zeenews.india.com/telugu/sitemaps/{year}-{month}-video-sitemap.xml";link1=f"https://zeenews.india.com/telugu/sitemaps/sitemap-{year}-{month}.xml"
elif lang=="ml" : link=f"https://zeenews.india.com/malayalam/sitemaps/{year}-{month}-video-sitemap.xml";link1=f"https://zeenews.india.com/malayalam/sitemaps/sitemap-{year}-{month}.xml"
elif lang=="gu" : link=f"https://zeenews.india.com/gujarati/sitemaps/{year}-{month}-video-sitemap.xml";link1=f"https://zeenews.india.com/gujarati/sitemaps/sitemap-{year}-{month}.xml"
elif lang=="kn" : link=f"https://zeenews.india.com/kannada/sitemaps/{year}-{month}-video-sitemap.xml";link1=f"https://zeenews.india.com/kannada/sitemaps/sitemap-{year}-{month}.xml"
else:
	print("this code only supports 9 langs !!!")
	sys.exit(1)
print(link)
print(link1)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
markup_string = requests.get(link,headers=headers, stream=True).content
soup = bs4.BeautifulSoup(markup_string, "xml")
url_list=soup.findAll(['url'])
for url in url_list:
	date=url.video.publication_date.text.strip()
	hlink=url.loc.text.strip()
	data_table = data_table.append({"Datetime": date ,"Link": hlink},ignore_index=True,)
vid_art=int(data_table.shape[0])
print("vids -",str(vid_art),"articles")

markup_string = requests.get(link1,headers=headers, stream=True).content
soup = bs4.BeautifulSoup(markup_string, "xml")
url_list=soup.findAll(['url'])
for url in url_list:
	date=url.lastmod.text.strip()
	hlink=url.loc.text.strip()
	data_table = data_table.append({"Datetime": date ,"Link": hlink},ignore_index=True,)
print("news -",str(int(data_table.shape[0])-vid_art),"articles")

data_table.drop_duplicates(subset=["Link"], inplace=True)
data_table.to_csv(os.path.join(save_csv_dir, f"ZEE_{lang}_{month_full.lower()}_{year}.csv"),encoding=config.CSV_FILE_ENCODING,index=False,)
print(f"\nFile ZEE_{lang}_{month_full.lower()}_{year}.csv is committed with {data_table.shape[0]} entries. \n")


