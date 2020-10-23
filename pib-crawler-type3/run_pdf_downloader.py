###############################################################################
# AUTHOR  : Aswin Pradeep
# AIM     : Code to download contents of PIB website in PDF format,
#           whose textual content is previously available in same directory
# USAGE   : python3 ./run_pdf_downloader.py
###############################################################################

import glob
import pdfkit

# Code Block below could be ignored if code is executed in a machine with GUI
from pyvirtualdisplay import Display
display = Display()
display.start()


# check for existing text files
txtfiles = [f for f in glob.glob("*.txt")]


pdffiles = []
for txtfilename in txtfiles:
    pdffiles.append(txtfilename.replace(".txt", ".pdf"))

downpdffiles = [f for f in glob.glob("*.pdf")]

# identify and download PDF while for the Documents which are available in TXT format alone
for filename in pdffiles:
    if filename not in downpdffiles:
        try:
            url="https://www.pib.gov.in/PressReleasePage.aspx?PRID="+str(filename).replace(".pdf", "")
            pdfkit.from_url(url, filename)
            print(filename, " : downloaded successfully as PDF")

        # In case of failure in between processing, those ID's will be saved to another file for re-looking   
        except Exception as e:
            print(e)
            print(filename, " : failed ")
            file2 = open("PDF_Failedfiles_log.txt", "a")
            file2.write("\n")
            file2.write(str(filename).replace(".pdf", "")) 
            file2.close()  