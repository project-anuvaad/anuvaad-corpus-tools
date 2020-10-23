from pathlib import Path
import os
from sentence_tokenizer import tokenize_file
from sentence_pair_aligner import start_aligner
from pib_scraper import populate_data,get_driver
import sys

months = ['January','February','March','April','May','June','July','August','September','October','November','December']

year = sys.argv[1]

scrape = int(sys.argv[2])

tokenize = int(sys.argv[3])

align = int(sys.argv[4])

print(year)

if(scrape == 1):
    driver = get_driver()
    dri = get_driver()
    
for month in months[::-1]:

    path_scrap = os.path.join(os.getcwd(),year,month,"All")
    
    path_tokenize = os.path.join(os.getcwd(),year,month,"Tokenize")
    
    path_align = os.path.join(os.getcwd(),year,month,"Aligned")
    
    path_parallel_csv = os.path.join(os.getcwd(),year)
    
    path_total_lines = os.path.join(year,month)
    
    base_path = os.getcwd()
    
    if(scrape == 1):
        Path(path_scrap).mkdir(parents=True,exist_ok=True)
        populate_data(driver,dri,'All',month,year,path_parallel_csv)
        
    if(tokenize == 1):
        Path(path_tokenize).mkdir(parents=True,exist_ok=True)
        tokenize_file(month,year,base_path,path_parallel_csv,path_tokenize,path_total_lines)
        
    if(align == 1):
        Path(path_align).mkdir(parents=True,exist_ok=True)
        start_aligner(month,year,path_parallel_csv,path_tokenize,path_align,path_total_lines)
