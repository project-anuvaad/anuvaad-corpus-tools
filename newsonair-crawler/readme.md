# Newsonair Website sentence Scraper

## Overview

The code in this repo could be utilized to scrape data from Newsonair , which has a large collection of En-Hi parallel documents in news domain.

By observing various articles in [Newsonair](http://newsonair.com/) website, we can understand that historic data are available in these URL's

    English : http://newsonair.com/Text-Archive-Search.aspx
    Hindi   : http://newsonair.com/hindi/Hindi-Text-Archive-Search.aspx

## Scraping Logic

* By doing an empty string based search in a pre-defined date range, all set of english and hindi URL's are collected
* Using collected URL's basic scraping is done
* A CSV file is created with the following fields:
    *    Timestamp
    *    Date
    *    Title
    *    Link
    *    Paragraphs

* Data grouping is done based on desired Date range
* Grouped English and Hindi content in same date range is processed to obtain tokenized sentences.
* These sentences are aligned using 'Labse' model in order to create a parallel dataset.

To initiate the process:

    python3 ./newsonair_scraper.py
    python3 ./run_textscraper.py


## Outcome

The Above Script was continuously run from 01-01-2021 to 10-01-2021, and a total of **3349(HI) + 4180(EN)** sentences have been scraped and aligned to obtain a parallel dataset of **1736** perfect matching pairs

Sample output can be seen inside the *sample_outputs* Folder

## Status

    WIP [ Tested successfully on jan (1-10) 2021]
    Values are hard-coded
    All exceptions are not handled