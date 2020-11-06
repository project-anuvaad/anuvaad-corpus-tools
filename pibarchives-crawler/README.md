# PIB Archives Crawler

## Overview
This repository houses the crawler code for building the Anuvaad parallel corpus.
The ultimate goal is to build quality parallel datasets across various domains
(General, Judicial, Educational, Financial, Press, etc) & various Indian languages.

The current set of crawlers are built to scrape, tokenizer and align
multilingual reports/documents available at various sources.

##### Source : Press Information Bureau Archives ([http://pibarchive.nic.in](http://pibarchive.nic.in))


## Processing Steps
The broader steps involved in all the tools can be generalized to the following :
##### 1. Scraping
Hit the required web page & download the contents in respective languages

	To run scraping for a particular month of a year:
		puthon3 pib_archieve_scrape.py --output-dir <output-directory> --month <month> --year <year>
		Example:
 		python3 pib_archive_scrape.py --output-dir ./PIB_archieve/2012 --month january --year 2012

	To scrape for a complete year execute the script:
		pib_archive_scrape_yearwise.bat <output-dir> <year>
		Example:
		pib_archive_scrape_yearwise.bat ./PIB_archieve/2012 2012

##### 2. Tokenizing
The process of spliting the scraped document into individual sentences using the Tokenizer.

	To tokenize we have to provide api link for language tokenizer in utilities.py
		ENGLISH_TOKENIZER_API = 
		HINDI_TOKENIZER_API   = 

	To tokenize scrape file for a particular month of a given year execute:
		python3 tokenizer_scrape_file.py  --output-dir <output-directory> --month <month> --year <year>
		Example:
		python3 tokenizer_scrape_file.py --output-dir ./PIB_archieve/2011 --month february --year 2011
  
	To tokenize scrape data for a complete year execute the script:
		tokenizer_scrape_file_yearwise.bat <output-dir> <year>
		Example:
		tokenizer_scrape_file_yearwise.bat ./PIB_archieve/2012 2012

##### 3. Sentence Aligning
The process of pairing the sentences across different languages which has the same meaning.

	To align hindi-english sentences various api link for hindi-english aligner in utilities.py
		DOCUMENT_UPLOAD_API   = 
		DOCUMENT_DOWNLOAD_API = 
		SUBMIT_ALIGNER_API    = 
		GET_ALIGNER_RESULT    = 
		
	Also provide bearer token in align_english_hindi_sentences.py
		BEARER_TOKEN =
		
	To run aligner for a particular month of a given year execute:
		python3 align_english_hindi_sentences.py  --output-dir <output-directory> --month <month> --year <year>
		Example:
		python3 align_english_hindi_sentences.py --output-dir ./PIB_archieve/2010 --month march --year 2010
		
	To align  complete year data execute the script:
		align_english_hindi_sentences_yearwise.bat <output-dir> <year>
		Example:
		align_english_hindi_sentences_yearwise.bat ./PIB_archieve/2010 2010

## Parallel Corpus
The parallel corpus of the above datasets are available under :
[anuvaad-parallel-corpus](https://github.com/project-anuvaad/anuvaad-parallel-corpus)
