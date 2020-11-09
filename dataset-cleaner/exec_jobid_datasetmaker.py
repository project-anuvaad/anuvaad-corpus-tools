#######################################################################################################
# AUTHOR  : aswin.pradeep@tarento.com
# AIM     : Script to create cleaned parallel dataset from Anuvaad_Aligner_Job_ID
# USAGE   : python3 exec_jobid_datasetmaker.py -j "ALIGN-JOB-ID" -s "hi" -o "/home/downloads/output/"
#######################################################################################################

import sys
import argparse
import pandas as pd
import urllib.request, json 
from parallelcleaner import parallelcleanerfn

msg = "Adding description"

# Initialize parser & add arguments
parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-j", "--job"       , help = "Aligner Job ID eg : ALIGN-1604300691304")
parser.add_argument("-o", "--outputdir" , help = "Output directory ending with slash [give directory,not filename] eg: /home/user/downloads/", default="./" )
parser.add_argument("-s", "--secondlang", help = "language in second column of dataset (assuming first is always english)")
args = parser.parse_args()

if args.job is None:
    sys.exit("ERROR : Aligner Job ID missing!")

if args.secondlang is None:
    sys.exit("ERROR : Second language locale missing!")

if args.outputdir[-1:] is not "/":
    sys.exit("ERROR : Invalid Directory!")



print("Passed inputs : ")
print("----------------")
print("Input File          : " + args.job)
print("Output Directory    : " + args.outputdir)
print("Second Language     : " + args.secondlang)




align_job_id = args.job
outputdir = args.outputdir
outputfile = align_job_id
secondlanguage = args.secondlang

search_url = "https://auth.anuvaad.org/anuvaad-etl/extractor/aligner/v1/alignment/jobs/get/"+align_job_id
download_url="https://auth.anuvaad.org/download/"


try:
    with urllib.request.urlopen(search_url) as url:
        data = json.loads(url.read().decode())

    nomatch=str(data[0]['output']['noMatch']['source'])
    match_english=str(data[0]['output']['match']['target'])
    match_non_english=str(data[0]['output']['match']['source'])
    almostmatch_english=str(data[0]['output']['almostMatch']['target'])
    almostatch_non_english=str(data[0]['output']['almostMatch']['source'])


    df1=pd.read_csv(download_url+nomatch,encoding='utf-16', sep='\t',header=None )
    df=pd.DataFrame()
    df['L1']=df1[0]
    df.to_csv(outputdir+outputfile+"_NO_MATCH_UNCLEANED.txt",index=False,header=False, sep='\t',encoding="utf-16")
    print("No Match Done . . .")


    df1=pd.read_csv(download_url+almostmatch_english,encoding='utf-16', sep='\t',header=None)
    df2=pd.read_csv(download_url+almostatch_non_english,encoding='utf-16', sep='\t',header=None)
    df=pd.DataFrame()
    df['L1']=df1[0]
    df['L2']=df2[0]
    df = df[1:]
    # df.to_csv(outputdir+outputfile+"_ALMOST_UNCLEANED.csv",index=False)
    # print("Almost Match Uncleaned Done . . .")

    df=parallelcleanerfn(df,secondlanguage)
    df.to_csv(outputdir+outputfile+"_ALMOST__CLEANED_en_"+secondlanguage+".csv",index=False,encoding='utf-16') 
    print("Almost Match Cleanup Done . . .")



    df1=pd.read_csv(download_url+match_english,encoding='utf-16', sep='\t',header=None)
    df2=pd.read_csv(download_url+match_non_english,encoding='utf-16', sep='\t',header=None)
    df=pd.DataFrame()
    df['L1']=df1[0]
    df['L2']=df2[0]
    df = df[1:]
    # df.to_csv(outputdir+outputfile+"_MATCH_UNCLEANED.csv",index=False)
    # print("Match uncleaned done . . .")


    df=parallelcleanerfn(df,secondlanguage)
    df.to_csv(outputdir+outputfile+"MATCH__CLEANED_en_"+secondlanguage+".csv",index=False,encoding='utf-16') 
    print("Match Cleanup Done . . .")


except Exception as e:
    # print(e)
    print("Please verify if Alignment Job Id is correct & Completed")