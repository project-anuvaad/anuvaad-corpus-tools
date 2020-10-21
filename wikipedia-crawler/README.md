# Wikipedia Crawler

## Overview
This repository houses the crawler code for building the Anuvaad parallel corpus.
The ultimate goal is to build quality parallel datasets across various domains
(General, Judicial, Educational, Financial, Press, etc) & various Indian languages.

The current set of crawlers are built to scrape, tokenizer and align
multilingual reports/documents available at various sources.

##### Source : Wikipedia ([https://www.wikipedia.org](https://www.wikipedia.org))

## Processing Steps
The broader steps involved in all the tools can be generalized to the following :
##### 1. Scraping
Hit the required web page & download the contents in respective languages and move on to other wiki articles from the web page.Starting point for the wiki articles is in the initialization of next_links = ["/wiki/Supreme_Court"]. Creates a directory "Scraped_Files" in the current directory and saves the scraped text in "utf-16" format. An ID is assigned to each article and the files are stored as ID-lang_c.txt where lang_c is the ISO-639-1 code of the language scraped.

To run scraping:
	python3 run_scrape_pipeline.py
	
##### 2. Tokenizing
The process of spliting the scraped document into individual sentences using the Tokenizer. Tokenizes the files present in the directory "Scraped_Files" and stores them in the directory "Tokenized_Files" with the same filename.

To run tokenization:
	python3 tokenize_files.py

##### 3. Sentence Aligning
The process of pairing the sentences across different languages which has the same meaning. Aligns the tokenized files and stores the match files in directory "Aligned_Files".

To run aligner:
	python3 submit_to_aligner.py

## Parallel Corpus
The parallel corpus of the above datasets are available under :
[anuvaad-parallel-corpus](https://github.com/project-anuvaad/anuvaad-parallel-corpus)
