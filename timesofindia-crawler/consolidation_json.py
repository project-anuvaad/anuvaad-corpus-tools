import pandas as pd
import os
import config
from argparse import ArgumentParser

def consolidate(lang,year,month_list):
	source0, target0, source1, target1 = [], [], [], []
	lang_dict={'hi':'hindi','te':'telugu','kn':'kannada','ta':'tamil','ml':'malayalam','mr':'marathi','gu':'gujarati'}
	score_table={"hi":1.23,"mr":1.05}
	data_table=pd.DataFrame()
	
	for month in month_list:
		try:
			x_data_table=pd.read_csv(f"{year}/{month}_{year}/{lang_dict[lang].capitalize()}/align_{lang}_en/000_{lang}_sen_{month}_{year}_aligned_am_src.tsv", encoding="utf-16", sep="\t")
			data_table=data_table.append(x_data_table,ignore_index=True)
			del x_data_table
		except:
			print("no data in month -",str(month))

	print("total no of pairs before applying threshold\tm-"+str(data_table.shape[0]))

	data_table=data_table[data_table["score_out"]>=score_table[lang]]
	data_table.drop_duplicates(subset=["src_out"], inplace=True)
	print("total no of pairs after applying threshold\tm-"+str(data_table.shape[0]))

	out_dir=f"Consolidated_Files/{year}"
	try:
		os.mkdir(out_dir)
	except:
		pass
	data_table.to_csv(
		os.path.join(out_dir, f"Total_TOI_{lang}-En_{year}_Aligner_Match.csv"),
		encoding=config.CSV_FILE_ENCODING,
		index=False,
	)
	data_table.to_csv(
		os.path.join(out_dir, f"Total_TOI_{lang}-En_{year}_Aligner_Match.tsv"),
		encoding=config.CSV_FILE_ENCODING,
		index=False,
		sep = '\t'
	)

def main():
	parser = ArgumentParser()
	parser.add_argument("--lang-code", help="Language Code - bn,hi,en", type=str, required=True)
	parser.add_argument("--year", help="year", type=str, required=True)
	parser.add_argument("--month-list", help="default : all -> all 12 months\neg : janaury,march,june -> only jan,mar,jun files will be consolidated.  ", type=str, default="all")
	args = parser.parse_args()
	n_lang=args.lang_code
	year= args.year
	if args.month_list == "all":
		month_list = ["january","february","march","april","may","june","july","august","september","october","november","december",]
	else :
		month_list = args.month_list.split(",")
	consolidate(n_lang,year,month_list)

if __name__ == "__main__":
	main()