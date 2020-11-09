#######################################################################################################
# AUTHOR  : aswin.pradeep@tarento.com
# AIM     : Script to clean single columnar dataset or TXT file
# USAGE   : python3 exec_jobid_datasetmaker.py -j "ALIGN-JOB-ID" -s "hi" -o "/home/downloads/output/"
#######################################################################################################

import sys
import argparse
import pandas as pd
import urllib.request, json 
from singularcleaner import singularcleanerfn
from datetime import datetime

#python3 singular_datasetcleaner.py -i "file1.txt" -o "file2.txt" -e "utf-16" -l "ml"
msg = "Adding description"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input txt or Single column csv/tsv file")
parser.add_argument("-o", "--output", help = "Output txt file")
parser.add_argument("-l", "--locale", help = "language locale")
parser.add_argument("-e", "--encoding", help = "encoding type (utf8 or utf-16)")
args = parser.parse_args()

if args.input is None:
    sys.exit("ERROR : input variable missing!")

if args.output is None:
    sys.exit("ERROR : output variable missing!")

if args.locale is None:
    sys.exit("ERROR : language locale missing!")

if args.encoding is None:
    sys.exit("ERROR : encoding type missing!")

if args.output[-4:][0] is not ".":
    sys.exit("ERROR : check output extension")

print("Passed inputs : ")
print("----------------")
print("Input File  : " + args.input)
print("Output File : " + args.output)
print("Lang Locale : " + args.locale)
print("Enc Type    : " + args.encoding)


input_path  = args.input
output_path = args.output
lang = args.locale
enctype = args.encoding

if(input_path[-3:]=="csv"):
    df1=pd.read_csv(input_path,encoding=enctype,header=None,error_bad_lines=False,warn_bad_lines=True)
else:
    df1=pd.read_csv(input_path,encoding=enctype, sep='\t',header=None,error_bad_lines=False,warn_bad_lines=True)

df=pd.DataFrame()
df['L1']=df1[0]
df = df[1:]
df=singularcleanerfn(df,lang)
df.to_csv(output_path,index=False,header=False, sep='\n',encoding="utf-16" ) 
print("Cleanup Done . . .")
