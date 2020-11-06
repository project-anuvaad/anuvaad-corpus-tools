:: Run tokenize scrape file yearwise
@echo off 
for %%a in (january,february,march,april,may,june,july,august,september,october,november,december) do ( 
python ./../tokenizer_scrape_file.py --output-dir %1 --month %%a --year %2)

