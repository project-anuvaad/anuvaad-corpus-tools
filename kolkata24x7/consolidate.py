#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd                

import os
import config
lang = "Malayalam"
lang_code = "ml"
year= 2021
source0, target0, source1, target1 = [], [], [], []
month_list = [
                "jan"
            ]
for month in month_list:
    with open(f"{year}/Output/{year}/{month}_{year}/{lang}/align_{lang_code}_en/000_{lang_code}_sen_{month}_{year}_aligned_m_src.txt", encoding="utf-16") as sm:
        for src0 in sm:
            source0.append(src0.strip())
    with open(f"{year}/Output/{year}/{month}_{year}/{lang}/align_{lang_code}_en/000_en_sen_{month}_{year}_aligned_m_tgt.txt", encoding="utf-16") as tm:
        for tgt0 in tm:
            target0.append(tgt0.strip())
    with open(f"{year}/Output/{year}/{month}_{year}/{lang}/align_{lang_code}_en/000_{lang_code}_sen_{month}_{year}_aligned_am_src.txt", encoding="utf-16") as sam:
        for src1 in sam:
            source1.append(src1.strip())
    with open(f"{year}/Output/{year}/{month}_{year}/{lang}/align_{lang_code}_en/000_en_sen_{month}_{year}_aligned_am_tgt.txt", encoding="utf-16") as tam:
        for tgt1 in tam:
            target1.append(tgt1.strip())

match = pd.DataFrame({'English Sentences': target0, f" '{lang} Sentences' ": source0}) 
almost_match = pd.DataFrame({'English Sentences': target1, f" '{lang} Sentences' ": source1})
len_e = match.duplicated(subset=['English Sentences']).sum()
len_b = match.duplicated(subset=[f" '{lang} Sentences' "]).sum()
len_eb = match.duplicated(subset=['English Sentences']).sum()
len_ae = almost_match.duplicated(subset=['English Sentences']).sum()
len_ab = almost_match.duplicated(subset=[f" '{lang} Sentences' "]).sum()
len_aeb = almost_match.duplicated(subset=['English Sentences']).sum()
out_dir =f"Consolidated_Files/{year}"
print(f"English {len_e}, {lang} {len_b}, En-{lang_code} Pair {len_eb}")
print(f"English {len_ae}, {lang} {len_ab}, En-{lang_code} Pair {len_aeb}")
print(len(match),len(almost_match))

if not os.path.exists(out_dir):
    os.makedirs(out_dir)
match.drop_duplicates(subset=['English Sentences'], inplace=True)
almost_match.drop_duplicates(subset=['English Sentences'], inplace=True)
print(len(match),len(almost_match))
match.to_csv(
    os.path.join(out_dir, f"Total_lokmat_{lang_code}-En_{year}_Aligner_Match.csv"),
    encoding=config.CSV_FILE_ENCODING,
    index=False,
)
match.to_csv(
    os.path.join(out_dir, f"Total_lokmat_{lang_code}-En_{year}_Aligner_Match.tsv"),
    encoding=config.CSV_FILE_ENCODING,
    index=False,
    sep = '\t'
)
almost_match.to_csv(
    os.path.join(out_dir, f"Total_lokmat_{lang_code}-En_{year}_Aligner_Almost_Match.csv"),
    encoding=config.CSV_FILE_ENCODING,
    index=False,
)

