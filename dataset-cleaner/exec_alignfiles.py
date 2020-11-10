#######################################################################################################
# AUTHOR  : aswin.pradeep@tarento.com
# AIM     : Script to initiate alignment for two text files
# USAGE   : python3 exec_alignfiles.py -sc "./mal.txt" -l "ml" -tg "./eng.txt"
#######################################################################################################

import sys
import argparse
import requests
import constants
from datetime import datetime

msg = "Adding description"

# Initialize parser & add arguments
parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-sc", "--source", help = "source file path to align")
parser.add_argument("-l", "--locale" , help = "language locale code of source file" )
parser.add_argument("-tg", "--target", help = "target file path to align")
args = parser.parse_args()

if args.source is None:
    sys.exit("ERROR : Source file missing!")

if args.locale is None:
    sys.exit("ERROR : Source language code missing")

if args.target is None:
    sys.exit("ERROR : Target file missing")



print("Passed inputs : ")
print("----------------")
print("Source  File     : " + args.source)
print("Source Locale    : " + args.locale)
print("Taregt File      : " + args.target)

try: 
    upload_url = constants.UPLOAD_URL
    aligner_url = constants.ALIGNER_URL

    file1_path = args.source
    file2_path = args.target
    source_locale = args.locale

    payload = {}
    file1_body = [
    ('file', open(file1_path,'rb'))
    ]
    headers = constants.HEADERS

    upload_response1 = requests.request("POST", upload_url, headers=headers, data = payload, files = file1_body)

    file1_response  = upload_response1.json()["data"]
    print(file1_path , " Uploaded successfully as ", file1_response)

    file2_body = [
    ('file', open(file2_path,'rb'))
    ]

    upload_response2 = requests.request("POST", upload_url, headers=headers, data = payload, files = file2_body)

    file2_response  = upload_response2.json()["data"]
    print(file2_path , " Uploaded successfully as ", file2_response)

    aligner_body = {
    "workflowCode":"WF_A_AL",
    "files": [
                {
                    "locale": source_locale,
                    "path": file1_response,
                    "type": "txt"
                },
                {
                    "locale": "en",
                    "path": file2_response,
                    "type": "txt"
                }
    ]
    }
    aligner_response = requests.request("POST", aligner_url, json=aligner_body, headers=headers).json()
    print("Job submitted to aligner successfully, save job ID given below : ")
    print(aligner_response['jobID'])

    logfile = open("aligner_log.txt","a")
    logfile.write("\n\n"+str(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))) 
    logfile.write("\n"+"Source path : " + file1_path)
    logfile.write("\n"+"Source language : " + source_locale)
    logfile.write("\n"+"target path : " + file2_path)
    logfile.write("\n"+"target language : " + 'en')
    logfile.write("\n"+"Job ID : " +  aligner_response['jobID'])
    logfile.write("\n"+"Response JSON : " + str(aligner_response))
    logfile.close()

except Exception as e:
    print(e)
    print("Please see the above exception")