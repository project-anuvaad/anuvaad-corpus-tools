# PIB_Scraping

#### Creates all the directories and files in the current directory
#### Tokenizer in this for now discards sentences that have 4 or less than 4 words. This is not feasible. For now aligning works fine 

To run : 

	python wrapper.py 'year' 'whetherScrape?' 'whetherTokenize?' 'whetherAlign?'

Pipeline : 

	SCRAPE ---> TOKENIZE ---> ALIGN

(Arguments : 1 is True, 0 is False. Arguments are added in to make it possible to work on any one of the stage in the pipeline)

First Run : 
	
	python wrapper.py 2020 1 1 1

wrapper.py takes in 4 command line arguments:

*	1) The first one being the year to scrape, it scrapes all the months in reverse order and writes those files in All directory in the respective month. The file is stored as PRID-Language.txt. It also generates a file containing all the PRID of the websites scraped, which makes it easy to debug and access.

*	2) The second argument is for whether to scrape the specified year. This is added in to make it possible to tokenize or align files that are already scraped.

*	3) The third argument is for whether to tokenize the specified year. If true this tokenizes the files present in the default directory
	
*	4) The fourth argument is for whether to align the files that are tokenized in the previous stage. 

Scrape PIB website of all documents on given date , month and year. The required date,month and year is updated in the init function in scrap3_3.py 

sentence_extraction.py has the code for tokenization of scraped data. Tokenization in this file is carried out using a regular expression and not by calling the API endpoint for it. Only those sentences that have more than 4 words are considred and written in the file, i.e. all those sentences with either 4 or less than 4 words are discarded. It also creates a csv file of all the tokenized sentences from the given file.

aligning.py is used for aligning the two parallel files. This is to be run after tokenization. It also creates a csv file of all the matched and almost matched sentences. 

The code only scraps Hindi and English parallel documents. The code scraps and generates a parallel lookup csv file in the current directory.


# To run only aligner

To run : 

	python aligning.py

#### Change the base_path in the code to the root folder of the downloaded tokenized files from Google Drive. The program searches for files in the same folder structure as followed in Drive. The program assumes that all Tokenized files are present in {root_folder}/year/month/Tokenized-Mine-No-Constraints. The program writes the csv file and the aligned files in the folder structure {root_folder}/year/month/Total-Match|Almost-Match.csv and {root_folder}/year/month/Aligned respectively. Any changes in the structure should be updated in the code also.

Specify the base_path (root folder) of the downloaded scraped and tokenized files. Program then aligns the two parallel files and writes the most and almost_matched sentences in their respective files . These are the sentences that have more then 4 words. By testing, it was noticed that it is more feasible to discard sentences only after aligning. There will be sentences that have more than 4 words in English but its Hindi counterpart might not be so and hence we miss a sentence that can be perfectly matched. The code also generates csv files of Total-Match and Total-Almost-Match. These files also consist of only those sentences that have more than 4 words in either English or in Hindi.

# To download PDF

Specify the root folder and month and year of which should be downloaded, the program creates a PDF folder in the destination and downloads all the PDF from the website that are actually parallel to each other.