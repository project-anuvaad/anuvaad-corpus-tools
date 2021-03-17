#######################################################################################################
# AUTHOR  : aswin.pradeep@tarento.com
# AIM     : Standalone python function to clean single column dataframe
# USAGE   : df = singularcleanerfn(df, "hi")
#######################################################################################################

import pandas as pd
import urllib.request, json 
import numpy as np
import re
from datetime import datetime
import os
from polyglot.detect import Detector 
import regxlist
# from langdetect import detect ,detect_langs ,DetectorFactory
# DetectorFactory.seed = 0


def singularcleanerfn(df,lang):
    
        print("Progressing single column cleanup script , numer of rows : ", len(df))

        df=df.drop_duplicates()
        if(lang=='en'):
            df["L1"] =  df['L1'].str.replace('[^\x00-\x7F]','')

        df["L1"] =  df['L1'].str.replace(';','.')
        df["L1"] =  df['L1'].str.replace(':',' ')

        common_regList = regxlist.common_regList
        regList = regxlist.regList

        for reg in common_regList:
            df['L1']=df['L1'].str.replace(reg,' ')

        df['L1']=df['L1'].str.strip()

        for reg in regList:
            df['L1']=df['L1'].str.replace(reg,' ')

        df['L1']=df['L1'].str.strip()
        L1list=df['L1'].to_list()
        dumplst = []
        newlanglist1 = []
        for title in L1list:
            try:
                if(len(title)<5):
                # if(len(title)<10 or len(re.findall(r'\w+', title))<4):
                    newlanglist1.append("NA")
                    dumplst.append(title)
                else:
                    # detlan=detect(title) #using langdetect library
                    detlan = Detector(title).language.code #using polygot langdetect
                    if(detlan!=lang):
                        newlanglist1.append("NA")
                        dumplst.append(title)
                    elif(detlan==lang):
                        newlanglist1.append(title)   
            except:
                newlanglist1.append("NA")
                dumplst.append(title)

        for i in range(len(newlanglist1)):
            if(newlanglist1[i]=="NA"):
                newlanglist1[i]=""


        df['COL1']=newlanglist1

        df['COL1'].replace('', np.nan, inplace=True)

        df.dropna(subset=['COL1'], inplace=True)

        del df['L1']

        dumpname = "Dumps/dump_"+str(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))+".txt"

        if not os.path.exists(os.path.dirname(dumpname)):
            try:
                os.makedirs(os.path.dirname(dumpname))
            except:
                print("Create a folder named  'Dumps' in script directory")  

        for item in dumplst:
            file2 = open(dumpname,"a")
            file2.write(item) 
            file2.write("\n")
            file2.close()

        df = df.replace('\n','', regex=True)
        print(len(df), " rows processed successfully")    
        return(df)

