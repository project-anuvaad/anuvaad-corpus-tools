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
from bs4 import BeautifulSoup
from polyglot.detect import Detector 
import regxlist
# from langdetect import detect ,detect_langs ,DetectorFactory
# DetectorFactory.seed = 0

def parallelcleanerfn(df,secondlanguage):


        # df=pd.DataFrame()
        # df['L1']=dfx[dfx.columns[0]]
        # df['L2']=dfx[dfx.columns[1]]

        print("Progressing paralell cleanup script, No of rows:", len(df))

        df = df.replace('\n','', regex=True)
        #drop duplicate pairs
        df=df.drop_duplicates(subset=['L2','L1'], keep="first")
        df_copy = df.copy()
        #create list of original content for dumping later
        dumpL1list=df_copy['L1'].to_list()
        dumpL2list=df_copy['L2'].to_list()

        #fixes html tags displayed in encoded format
        df = df.applymap(lambda text: BeautifulSoup(text, features = "lxml").string)

        #replaces all non ascii characters from english column
        df["L1"] =  df['L1'].str.replace('[^\x00-\x7F]','')
        #replaces semi colon with full stop
        df["L1"] =  df['L1'].str.replace(';','.')
        df["L2"] =  df['L2'].str.replace(';','.')

        #calls list of items for replacement from file
        common_regList = regxlist.common_regList
        regList = regxlist.regList

        #replaces all cases with space
        for reg in common_regList:
            df['L2']=df['L2'].str.replace(reg,' ')
            df['L1']=df['L1'].str.replace(reg,' ')

        df['L2']=df['L2'].str.strip()
        df['L1']=df['L1'].str.strip()

        for reg in regList:
            df['L2']=df['L2'].str.replace(reg,' ')
            df['L1']=df['L1'].str.replace(reg,' ')

        df['L2']=df['L2'].str.strip()
        df['L1']=df['L1'].str.strip()
        L1list=df['L1'].to_list()
        L2list=df['L2'].to_list()

     

        newlanglist1 = []
        newlanglist2 = []
        dumplstc1 = []
        dumplstc2 = []

        #function identifies and drops non english content
        #erroneous sentences are dumped to a seperate csv file
        for i in range(0,len(L1list)):

            try:

                title1= L1list[i]
                title2=L2list[i]
                dumptitle1= dumpL1list[i]
                dumptitle2 =dumpL2list[i]

                if(len(title1)<5 or len(re.findall(r'\w+', title1))<2 or len(title2)< 5 ):
                    dumplstc1.append(dumptitle1)
                    dumplstc2.append(dumptitle2)


                else:
                    
                    #using langdetect library. slower, more efficient. preferred for small datasets
                    # detlan1=str(detect(title1))
                    # detlan2=str(detect(title2))

                    #using polygot library , faster , preferred for larger datasets.
                    detlan1 = Detector(title1).language.code
                    detlan2 = Detector(title2).language.code
            
                    if(detlan1!='en' or detlan2!=secondlanguage):

                        dumplstc1.append(dumptitle1)
                        dumplstc2.append(dumptitle2)

                    elif(detlan1=='en' and detlan2==secondlanguage):

                        newlanglist1.append(title1)   
                        newlanglist2.append(title2)

                    else:
                        dumplstc1.append(dumptitle1)
                        dumplstc2.append(dumptitle2)


            except:
             
                dumplstc1.append(dumptitle1)   
                dumplstc2.append(dumptitle2)   
  
      
        cleaneddf = pd.DataFrame(list(zip(newlanglist1, newlanglist2)), columns =['L1', 'L2']) 
        cleaneddf = cleaneddf.replace('\n','', regex=True)

        #saves the dropped content to a dump CSV file
        dumpname = "Dumps/dump_"+str(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))+".csv"
        dumpdf = pd.DataFrame(list(zip(dumplstc1, dumplstc2)), columns =['L1', 'L2']) 

        if not os.path.exists(os.path.dirname(dumpname)):
            try:
                os.makedirs(os.path.dirname(dumpname))
            except:
                print("Create a folder named  'Dumps' in script directory")  

        dumpdf = dumpdf.replace('\n','', regex=True)
        dumpdf.to_csv(dumpname ,index=False)

        print("cleanup done, number of rows processed : ", len(cleaneddf))
        return(cleaneddf)

