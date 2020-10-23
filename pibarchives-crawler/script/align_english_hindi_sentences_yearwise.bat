:: Run aligner for hindi-english yearwise
@echo off 
for %%a in (january,february,march,april,may,june,july,august,september,october,november,december) do ( 
python ./../align_english_hindi_sentences.py --output-dir %1 --month %%a --year %2)

