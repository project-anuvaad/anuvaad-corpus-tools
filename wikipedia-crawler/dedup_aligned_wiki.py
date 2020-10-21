import pandas as pd
import os
from pathlib import Path


lang = 'hi'
b_path = os.path.join(r'C:\Users\Dhanvi\Wikipedia_Scraping','Aligned_Files')
output_path = os.path.join(r'C:\Users\Dhanvi\Wikipedia_Scraping','Deduped_Aligned_Files')
Path(output_path).mkdir(parents=True,exist_ok=True)

df = pd.read_csv(os.path.join(b_path,'en-'+lang+'-m.csv'),encoding='utf-16')
df = df.drop_duplicates()
df.to_csv(os.path.join(output_path,'en-'+lang+'-m-Deduped.csv'),index=False,encoding='utf-16')

df = pd.read_csv(os.path.join(b_path,'en-'+lang+'-am.csv'),encoding='utf-16')
df = df.drop_duplicates()
df.to_csv(os.path.join(output_path,'en-'+lang+'-am-Deduped.csv'),index=False,encoding='utf-16')
