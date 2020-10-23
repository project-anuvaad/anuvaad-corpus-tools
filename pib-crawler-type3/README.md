# PIB Website Content Scraper

## Overview

The code in this repo could be utilized to scrape data from PIB website, which has a large collection of content in regional Indian languages.

By observing various articles in [PIB](http://pib.gov.in) website, we can understand that the URL is being changed in a particular pattern wherein only the document ID keeps on changing and gets circulated in a particular range.

Hence, this code scraps and download all PIB documents within the given range.

The  steps involved can be generalized in the following manner:

#### 1. Iterating & Saving content as TXT file + creating an index dataset

![Image](https://i.imgur.com/QDARBg8.jpg "PIB document general structure")



All the articles on the website have a general structure.

* The ID, which keeps on changing in order.
* URL, with ID appended at the end
* A heading inside the H2 tag
* A timestamp with article-posted date/time/region.

To initiate the process:

    python3 ./run_textscraper.py

Provide upper and lower document id manually. Sample values are provided within code.
It iterates through the given ID range and saves content in TXT format.

Alongside, an index dataset is created which holds the following data:

* 1st column : Document ID
* 2nd column : Document URL
* 3rd column : Number of characters
* 4th column : Document Timestamp
* 5th column : Document Heading

These index dataset could be further utilized accordingly to group files based on region/language/date/time and process the downloaded files.

#### 2. Download documents in PDF format for the articles which are  already processed

In some situations, if we need contents other than textual data, like images or representations in the proper format, merely TXT files won't do.
Files should be downloaded in PDF format without losing the structure.

To initiate the process:

    python3 ./run_pdf_downloader.py

The code checks for text files, which do not have a pdf equivalent and then downloads it.

## Outcome

The Above Script was continuously run with the default range provided, and a total of **1,74,557** files has been collected in both TXT and PDF format individually.

Further processing could be done utilizing the index dataset created.

Sample output can be seen inside the *sample_outputs* Folder
