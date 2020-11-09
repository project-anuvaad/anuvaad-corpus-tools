#######################################################################################################
# AUTHOR  : aswin.pradeep@tarento.com
# AIM     : Script to create cleaned parallel dataset from uncleaned parallel dataset.
#           The input dataset must have only two column and c1 must be in english,
#           c2 language code must be specified
# USAGE   : python3 exec_jobid_datasetmaker.py -j "ALIGN-JOB-ID" -s "hi" -o "/home/downloads/output/"
#######################################################################################################

import sys
import argparse
import pandas as pd
import urllib.request, json 
from parallelcleaner import parallelcleanerfn

msg = "Adding description"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input txt or Single column csv/tsv file")
parser.add_argument("-o", "--output", help = "Output txt file")
parser.add_argument("-s", "--secondlang", help = "second column language locale")
parser.add_argument("-e", "--encoding", help = "encoding type (utf8 or utf-16)")
args = parser.parse_args()

if args.input is None:
    sys.exit("ERROR : input variable missing!")

if args.output is None:
    sys.exit("ERROR : output variable missing!")

if args.secondlang is None:
    sys.exit("ERROR : language locale missing!")

if args.encoding is None:
    sys.exit("ERROR : encoding type missing!")

if args.output[-4:][0] is not ".":
    sys.exit("ERROR : check output extension")

print("Passed inputs : ")
print("----------------")
print("Input File  : " + args.input)
print("Output File : " + args.output)
print("Lang Locale : " + args.secondlang)
print("Enc Type    : " + args.encoding)


input_path  = args.input
output_path = args.output
secondlang = args.secondlang
enctype = args.encoding
if(args.input[-3:]=="csv"):
    seperator=','
else:
    seperator='\t'

df1=pd.read_csv(input_path,encoding=enctype, sep=seperator,header=None,error_bad_lines=False,warn_bad_lines=True)

df=pd.DataFrame()
df['L1']=df1[0]
df['L2']=df1[1]
df = df[1:]
df = parallelcleanerfn(df,secondlang)
df.to_csv(output_path,index=False, sep=seperator,encoding="utf-16" ) 
print("Cleanup Done . . .")
