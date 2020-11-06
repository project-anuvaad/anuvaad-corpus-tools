:: Run scraping for a given year
@echo off 
for %%a in (january,february,march,april,may,june,july,august,september,october,november,december) do ( 
python ./../scrape_main_pib_website_en-hi.py --output-dir %1 --month %%a --year %2)