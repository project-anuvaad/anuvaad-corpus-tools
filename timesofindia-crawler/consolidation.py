import pandas as pd
import os
import config
from argparse import ArgumentParser

def consolidate(lang,year,month_list):
	source0, target0, source1, target1 = [], [], [], []
	lang_dict={'hi':'hindi','te':'telugu','kn':'kannada','ta':'tamil','ml':'malayalam','mr':'marathi','gu':'gujarati'}
	
	for month in month_list:
	    with open(f"{year}/{month}_{year}/{lang_dict[lang].capitalize()}/align_{lang}_en/000_{lang}_sen_{month}_{year}_aligned_m_src.txt", encoding="utf-16") as sm:
	        for src0 in sm:
	            source0.append(src0.strip())
	    with open(f"{year}/{month}_{year}/{lang_dict[lang].capitalize()}/align_{lang}_en/000_en_sen_{month}_{year}_aligned_m_tgt.txt", encoding="utf-16") as tm:
	        for tgt0 in tm:
	            target0.append(tgt0.strip())
	    with open(f"{year}/{month}_{year}/{lang_dict[lang].capitalize()}/align_{lang}_en/000_{lang}_sen_{month}_{year}_aligned_am_src.txt", encoding="utf-16") as sam:
	        for src1 in sam:
	            source1.append(src1.strip())
	    with open(f"{year}/{month}_{year}/{lang_dict[lang].capitalize()}/align_{lang}_en/000_en_sen_{month}_{year}_aligned_am_tgt.txt", encoding="utf-16") as tam:
	        for tgt1 in tam:
	            target1.append(tgt1.strip())

	head2=lang_dict[lang].capitalize()+' Sentences'
	match = pd.DataFrame({'English Sentences': target0, head2: source0}) 
	almost_match = pd.DataFrame({'English Sentences': target1, head2: source1})
	len_e = match.duplicated(subset=['English Sentences']).sum()
	len_b = match.duplicated(subset=[head2]).sum()
	len_eb = match.duplicated(subset=['English Sentences']).sum()
	len_ae = almost_match.duplicated(subset=['English Sentences']).sum()
	len_ab = almost_match.duplicated(subset=[head2]).sum()
	len_aeb = almost_match.duplicated(subset=['English Sentences']).sum()
	out_dir =f"Consolidated_Files/{year}"
	print("total no of pairs with duplication\tm-"+str(len(match))+"\tam-"+str(len(almost_match)))

	if not os.path.exists(out_dir):
	    os.makedirs(out_dir)
	match.drop_duplicates(subset=['English Sentences'], inplace=True)
	almost_match.drop_duplicates(subset=['English Sentences'], inplace=True)
	print("total no of pairs after removing duplication\tm-"+str(len(match))+"\tam-"+str(len(almost_match)))
	match.to_csv(
	    os.path.join(out_dir, f"Total_TOI_{lang}-En_{year}_Aligner_Match.csv"),
	    encoding=config.CSV_FILE_ENCODING,
	    index=False,
	)
	match.to_csv(
	    os.path.join(out_dir, f"Total_TOI_{lang}-En_{year}_Aligner_Match.tsv"),
	    encoding=config.CSV_FILE_ENCODING,
	    index=False,
	    sep = '\t'
	)
	almost_match.to_csv(
	    os.path.join(out_dir, f"Total_TOI_{lang}-En_{year}_Aligner_Almost_Match.csv"),
	    encoding=config.CSV_FILE_ENCODING,
	    index=False,
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