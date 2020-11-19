#######################################################################################################
# AUTHOR  : aswin.pradeep@tarento.com
# AIM     : Script to create cleaned parallel dataset from Anuvaad_Aligner_Job_ID
# USAGE   : python3 exec_jobid_datasetmaker.py -j "WF-JOB-ID" -o "/home/downloads/output/"
#######################################################################################################

import sys
import csv
import argparse
import pandas as pd
import urllib.request, json 
import requests
import constants
from parallelcleaner import parallelcleanerfn

msg = "Adding description"

# Initialize parser & add arguments
parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-j", "--job"       , help = "WF Job ID eg : A_A-UFZxF-1604944590772")
parser.add_argument("-o", "--outputdir" , help = "Output directory ending with slash [give directory,not filename] eg: /home/user/downloads/", default="./" )
args = parser.parse_args()

if args.job is None:
    sys.exit("ERROR : Job ID missing!")

if args.outputdir[-1:] is not "/":
    sys.exit("ERROR : Invalid Directory!")



print("Passed inputs : ")
print("----------------")
print("Input File          : " + args.job)
print("Output Directory    : " + args.outputdir)




align_job_id = args.job
outputdir = args.outputdir
outputfile = align_job_id
search_url = constants.SEARCH_URL
download_url = constants.DOWNLOAD_URL
head  = constants.HEADERS

try:
    

    body = {"jobIDs": [align_job_id],"taskDetails": "true" }
    data = requests.post(search_url, json=body, headers=head).json()

    print("Job Status : " + data['jobs'][0]['status'])

    secondlanguage = data['jobs'][0]['input']['files'][0]['locale']    
    nomatch=str(data['jobs'][0]['output']['noMatch']['source'])
    match_english=str(data['jobs'][0]["output"]['match']['target'])
    match_non_english=str(data['jobs'][0]["output"]['match']['source'])
    almostmatch_english=str(data['jobs'][0]['output']['almostMatch']['target'])
    almostatch_non_english=str(data['jobs'][0]['output']['almostMatch']['source'])


    df1=pd.read_csv(download_url+nomatch,encoding='utf-16', sep='\t',header=None, quoting=csv.QUOTE_NONE )
    df=pd.DataFrame()
    df['L1']=df1[0]
    df.to_csv(outputdir+outputfile+"_NO_MATCH_UNCLEANED.txt",index=False,header=False, sep='\t',encoding="utf-16")
    print("No Match Done . . .")


    df1=pd.read_csv(download_url+almostmatch_english,encoding='utf-16', sep='\t',header=None, quoting=csv.QUOTE_NONE)
    df2=pd.read_csv(download_url+almostatch_non_english,encoding='utf-16', sep='\t',header=None, quoting=csv.QUOTE_NONE)
    df=pd.DataFrame()
    df['L1']=df1[0]
    df['L2']=df2[0]
    df = df[1:]
    # df.to_csv(outputdir+outputfile+"_ALMOST_UNCLEANED.csv",index=False)
    # print("Almost Match Uncleaned Done . . .")

    df=parallelcleanerfn(df,secondlanguage)
    df.to_csv(outputdir+outputfile+"_ALMOST_CLEANED_en_"+secondlanguage+".csv",index=False,encoding='utf-16') 
    print("Almost Match Cleanup Done . . .")



    df1=pd.read_csv(download_url+match_english,encoding='utf-16', sep='\t',header=None, quoting=csv.QUOTE_NONE)
    df2=pd.read_csv(download_url+match_non_english,encoding='utf-16', sep='\t',header=None, quoting=csv.QUOTE_NONE)
    df=pd.DataFrame()
    df['L1']=df1[0]
    df['L2']=df2[0]
    df = df[1:]
    # df.to_csv(outputdir+outputfile+"_MATCH_UNCLEANED.csv",index=False)
    # print("Match uncleaned done . . .")


    df=parallelcleanerfn(df,secondlanguage)
    df.to_csv(outputdir+outputfile+"_MATCH_CLEANED_en_"+secondlanguage+".csv",index=False,encoding='utf-16') 
    print("Match Cleanup Done . . .")


except Exception as e:
    print(e)
    print("Please see the above exception")
