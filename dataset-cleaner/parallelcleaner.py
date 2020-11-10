#######################################################################################################
# AUTHOR  : aswin.pradeep@tarento.com
# AIM     : Standalone python function to clean parallel dataframe
# USAGE   : df = parallelcleanerfn(df, "hi")
#######################################################################################################

import pandas as pd
import urllib.request, json 
import numpy as np
import re
from datetime import datetime
import os
from langdetect import detect ,detect_langs ,DetectorFactory
DetectorFactory.seed = 0

def parallelcleanerfn(dfx,secondlanguage):


        df=pd.DataFrame()
        df['L1']=dfx[dfx.columns[0]]
        df['L2']=dfx[dfx.columns[1]]
    
        print("Progressing cleanup script . . .")

        df=df.drop_duplicates(subset=['L2','L1'], keep="first")

        df["L1"] =  df['L1'].str.replace('[^\x00-\x7F]','')
        df["L1"] =  df['L1'].str.replace(';','.')
        df["L2"] =  df['L2'].str.replace(';','.')

        common_regList=[]
        common_regList.append('▁')
        common_regList.append('"')
        common_regList.append("'")
        common_regList.append("&#")
        common_regList.append("\...")

        for reg in common_regList:
            df['L2']=df['L2'].str.replace(reg,' ')
            df['L1']=df['L1'].str.replace(reg,'')

        df['L2']=df['L2'].str.strip()
        df['L1']=df['L1'].str.strip()

        regList=[]
        regList.append('^[0-9]+\.')
        regList.append('^[0-9]\.')
        regList.append('^[0-9][0-9]\.')
        regList.append('^[(][0-9]+[)]')
        regList.append('^[0-9]+[)]')
        regList.append('^[(][a-zA-Z][)]')
        regList.append('^[a-zA-z]\.')
        regList.append('^[a-zA-z][)]')
        regList.append('^[IVXLCDM]+\.')
        regList.append('^[(][IVXLCDM]+[)]')
        regList.append('^[ivxlcdm]+\.')
        regList.append('^[(][ivxlcdm]+[)]')
        regList.append('^[ivxlcdm]+[)]')
        regList.append('^-')
        regList.append('^·')
        regList.append('^●')
        regList.append('^&')
        regList.append('^#')
        regList.append('^—')
        regList.append('^\...')
        regList.append('^Ø')
        regList.append('^•')
        regList.append('  +')
        regList.append('= =+')
        regList.append('==+')

        for reg in regList:
            df['L2']=df['L2'].str.replace(reg,'')
            df['L1']=df['L1'].str.replace(reg,'')

        df['L2']=df['L2'].str.strip()
        df['L1']=df['L1'].str.strip()
        L1list=df['L1'].to_list()
        L2list=df['L2'].to_list()

        newlanglist1 = []
        dumplst = []
        for title in L1list:
            try:
                if(len(title)<10 or len(re.findall(r'\w+', title))<4):
                    newlanglist1.append("NA")
                    dumplst.append(title)
                else:
                    detlan=detect(title)
                    if(detlan!='en'):
                        newlanglist1.append("NA")
                        dumplst.append(title)
                    elif(detlan=='en'):
                        newlanglist1.append(title)   
            except:
                newlanglist1.append("NA")
                dumplst.append(title)

        newlanglist2 = []
        for title in L2list:
            try:
                if(len(title)<5):
                    newlanglist2.append("NA")
                    dumplst.append(title)
                else:
                    detlan=detect(title)
                    if(detlan!=secondlanguage):
                        newlanglist2.append("NA")
                        dumplst.append(title)
                    elif(detlan==secondlanguage):
                        newlanglist2.append(title)
                
            except:
                newlanglist2.append("NA")
                dumplst.append(title)

        for i in range(len(newlanglist1)):
            if(newlanglist1[i]=="NA" or newlanglist2[i]=="NA"):
                newlanglist1[i]=""
                newlanglist2[i]=""

        df['COL1']=newlanglist1
        df['COL2']=newlanglist2

        df['COL1'].replace('', np.nan, inplace=True)
        df['COL2'].replace('', np.nan, inplace=True)

        df.dropna(subset=['COL1'], inplace=True)
        df.dropna(subset=['COL2'], inplace=True)

        del df['L1']
        del df['L2']

        dumpname = "Dumps/dump_"+str(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))+".txt"

        if not os.path.exists(os.path.dirname(dumpname)):
            try:
                os.makedirs(os.path.dirname(dumpname))
            except:
                print("Create a folder named  'Dumps' in script directory")  

        for item in dumplst:
            file2 = open(dumpname,"a")
            file2.write(str(item)) 
            file2.write("\n")
            file2.close()
            
        print(len(df), " rows processed successfully")
        return(df)


