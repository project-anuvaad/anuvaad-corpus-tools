import pandas as pd
import os
import glob
from argparse import ArgumentParser
from langdetect import detect
from indicnlp.tokenize.sentence_tokenize import sentence_split
from pathlib import Path
from langdetect import DetectorFactory

DetectorFactory.seed = 0


def create_directory(path):
	try:
		Path(path).mkdir(parents=True, exist_ok=True)
		return True
	except FileExistsError as fe_error:
		return True
	except OSError as error:
		print(error)
	return False


def main():
	parser = ArgumentParser()
	parser.add_argument("--scrape-file-loc",help="location of scrape file to be sentence splitted",type=str,default="scraped_files",)
	parser.add_argument("--output-folder", help="location of output folder", type=str, default="")
	parser.add_argument("--month", help="month", type=str, default="")
	parser.add_argument("--start-month", help="starting month for combining default=january", type=str, default="january")
	parser.add_argument("--end-month", help="stoping month for combination default=december", type=str, default="december")
	parser.add_argument("--year", help="year", type=str, required=True)
	parser.add_argument("--lang",type=str,required=True,help="language code : 'Kannada':'kn','Tamil':'ta','Marathi':'mr','Telugu':'te','Bengali':'bn','Gujarati':'gu','Malayalam':'ml','Punjabi':'pa','Assamese':'asm','Odia':'or','Urdu':'ur'",)
	args = parser.parse_args()
	n_year =  args.year
	org_month_list = ["january","february","march","april","may","june","july","august","september","october","november","december",]
	month_list = []
	if len(args.month) == 0 :
		start_index = org_month_list.index(args.start_month)
		end_index = org_month_list.index(args.end_month) + 1
		month_list.extend(org_month_list[start_index:end_index])
		print("output-folder "+ n_year+"/"+month_list[0]+"_"+n_year+"/ will consist scraped files of following months -" , month_list)
	else:
		month_list.append(args.month)
	lang = args.lang
	look_up_dict = {"English": "en","Hindi": "hi","Kannada": "kn","Tamil": "ta","Marathi": "mr","Telugu": "te","Bengali": "bn","Gujarati": "gu","Malayalam": "ml","Punjabi": "pa","Assamese": "asm","Odia": "or","Urdu": "ur",}
	look_up_dict = {v: k for k, v in look_up_dict.items()}	# Note: Inverting above dictionery
	if lang in look_up_dict.keys():
		if len(args.output_folder) == 0 : csv_file_loc = args.output_folder+ n_year +"/"+ month_list[0]+ "_"+ n_year+ "/"+ look_up_dict[lang]  
		else : csv_file_loc = args.output_folder+"/"+ n_year +"/"+ month_list[0]+ "_"+ n_year+ "/"+ look_up_dict[lang]	# list_fl = '_'.join([look_up_dict[lang],n_month,n_year]) + '.csv'
		tokenize_loc = csv_file_loc + "/" + "tokenize_file_" + month_list[0] + "_" + n_year   # submit_aligner = csv_file_loc + '\\' + 'submit_aligner'
		create_directory(csv_file_loc)
		create_directory(tokenize_loc)

	else:
		print("Please enter the corrent langauge code")
		return
	total_sen_pd = pd.DataFrame(columns=[look_up_dict[lang] + "_sen"])
	fl_list = []
	for month in month_list :
		scrape_loc = args.scrape_file_loc + "//"+ n_year+ "//"+ month+ " "+ n_year+ "//"+ look_up_dict[lang].lower()
		if not os.path.exists(scrape_loc):
			print(f"Path dosent exists:{scrape_loc}")
			return
		fl_list.extend(sorted(glob.glob(os.path.join(scrape_loc, "*.txt"))))
	old_count = 0
	for k, fl in enumerate(fl_list):
		tok_flname = tokenize_loc + "//tok_" + os.path.basename(fl)	# print(os.path.basename(fl) # Read Scrape Content
		with open(fl, mode="r", encoding="utf-16") as file_r:
			content = file_r.read()	#print(content)# Cleaning scrape content
		paragraph = content.split("\n")
		content = []
		for para in paragraph:
			para = para.strip()
			para = " ".join(para.split())
			if len(para.split()) >= 4:
				if lang == "en":
					content.append(para)
				else:
					try:
						if detect(para) != "en":
							content.append(para)
					except:
						content.append(para)
		# Tokenizing paragraphs into sentences
		sentences = []
		for entry in content:
			[sentences.append(tok_sen) for tok_sen in sentence_split(entry, lang)]
		# Removing Duplicates
		dump_1 = (pd.DataFrame(sentences, columns=["sen"]).drop_duplicates().loc[:, "sen"].values.tolist())
		sentences = dump_1
		# Write sentence token
		with open(tok_flname, mode="w", encoding="utf-16") as file_w:
			for sen in sentences:
				sen = sen.strip()
				sen = sen.strip('"')
				if len(sen.split()) >= 4:
					file_w.write(sen + "\n")
					total_sen_pd = total_sen_pd.append({look_up_dict[lang] + "_sen": sen.strip()}, ignore_index=True)
		# print(f'Number of sentences found: {total_sen_pd.shape[0]-old_count}')
		old_count = total_sen_pd.shape[0]

	print(f"Total number of sentences found: {total_sen_pd.shape[0]}")
	total_sen_pd.drop_duplicates(inplace=True)
	print(f"Total number of sentences after removing duplicate: {total_sen_pd.shape[0]}")
	total_sen_pd.to_csv(csv_file_loc+ "//"+ "total_"+ lang+ "_sen_"+ month_list[0]+ "_"+ n_year+ ".csv",index=False,encoding="utf-16",)

	with open(csv_file_loc+ "//"+ "total_"+ lang+ "_sen_"+ month_list[0]+ "_"+ n_year+ ".txt",mode="w",encoding="utf-16",) as write_total:
		for line in total_sen_pd[look_up_dict[lang] + "_sen"].values.tolist():
			write_total.write(line.strip() + "\n")

if __name__ == "__main__":
	main()
