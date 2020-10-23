###############################################################################
# AUTHOR  : Aswin Pradeep
# AIM     : Code to iterate through Documents in PIB website,
#           save content to TEXT file and prepare an Index of downloaded content
# USAGE   : python3 ./run_textscraper.py
###############################################################################
import urllib.request
from inscriptis import get_text
import re
import requests
from bs4 import BeautifulSoup
import pdfkit
import csv


# Scraping happens in decending order, hence starting_file_id > stopping_file_id
# Sample values
# 1653267 - starting_file_id for 2020 september
# 1479900 - stopping_file_id for 2017 january
starting_file_id = input("Enter Starting ID : ")
stopping_file_id = input("Enter Stopping ID : ")


for i in range(starting_file_id, stopping_file_id, -1):
    try:
        print(" Processing file with ID = ", i)

        # URL formation from ID
        url = "https://www.pib.gov.in/PressReleasePage.aspx?PRID="+str(i)

        # Opens URL and saves whole content to text file
        html = urllib.request.urlopen(url).read().decode('utf-8')
        text = get_text(html)
        if(len(text) > 250):
            fnametxt = str(i)+".txt"
            file1 = open(fnametxt, "w")
            file1.write(text)
            file1.close()
            # Using bs4 scraping is done on URL for index dataset creation
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'lxml')
            h2text = ''
            tstamp = ''

            # For PIB documents, generally file heading is in <h2> tag 
            # so contents of h2 are saved
            for heading in soup.find_all(["h2"]):
                h2text = h2text+heading.text.strip()

            # For all documents TIMESTAMP is saved ,
            # which could be used to classify documents 
            # on the basis of Time/Locatiom/Language
            mydivs = soup.findAll(
                "div", {"class": "ReleaseDateSubHeaddateTime text-center pt20"})
            for div in mydivs:
                div1 = str(div)
                start = ':'
                end = '<'
                s = div1
                tstamp = s[s.find(start)+len(start):s.rfind(end)]

            # Finally a row will be appended to CSV file for each document 
            # with infos like : documentID, URL, no:of:characters in document, TIMESTAMP and Heading
            row_contents = [i, url, len(text), tstamp.strip(), h2text.strip()]
            with open(r'Pib_index_dataset.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(row_contents)

    # In case of failure in between processing,
    # those ID's will be saved to another file for re-looking
    except:
        print(i, " Failed")
        file2 = open("TXT_Failedfiles_log.txt", "a")
        file2.write("\n")
        file2.write(str(i))
        file2.close()
