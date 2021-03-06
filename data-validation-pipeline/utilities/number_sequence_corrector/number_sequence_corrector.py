import re
import pandas as pd
import numpy as np
from strsimpy.metric_lcs import MetricLCS

def number_sequence_corr(parallel_data:pd.DataFrame,language1:str ='english',language2:str ='local')->pd.DataFrame:
    data = parallel_data.copy()
    data[f'correted_{language2}'] = ['']*parallel_data.shape[0]
    for count in range(parallel_data.shape[0]):
        english_sample_text = data.iloc[count,0]
        if language2 == 'bn':
            local_lang_sample_text = re.sub(r'[১২৩৪৫৬৭৮৯০]{1}',ben_num_repl,data.iloc[count,1])
        else:
            local_lang_sample_text = data.iloc[count,1]
        data.iat[count,2]=get_corrected_sentence(english_sample_text,local_lang_sample_text)
    return data.loc[:,[True,False,True]].copy()

def ben_num_repl(matchobj):
    lookup_table = {'১':'1','২':'2','৩':'3','৪':'4','৫':'5','৬':'6','৭':'7','৮':'8','৯':'9','০':'0'}
    return lookup_table[matchobj.group(0)]

def get_corrected_sentence(english_sample_text,local_lang_sample_text):
    number_english_text = re.findall(r'\d+[.\\,:()\/\s\d]*\d+|\d{1}',english_sample_text)
    number_local_lang_text = list(re.finditer(r'\d+[.\\,:()\/\s\d]*\d+|\d{1}', local_lang_sample_text))
    score_dataframe = pd.DataFrame(columns=range(len(number_local_lang_text)),\
                                   index = range(len(number_english_text)),dtype=np.float)
    for column in score_dataframe.columns:
        for indx in score_dataframe.index:
            str_1 = number_local_lang_text[column].group(0)
            str_2 = number_english_text[indx]
            metric_lcs = MetricLCS()
            score_dataframe.at[indx,column] = metric_lcs.distance(str_1, str_2)\
                                                *(max(len(str_1),len(str_2))/min(len(str_1),len(str_2)))
    replace_dict = []
    while not (score_dataframe.shape[0] == 0 or score_dataframe.shape[1]==0):
        for column in score_dataframe.columns:
            if score_dataframe.shape[0] == 0 or score_dataframe.shape[1]==0:break
            k=score_dataframe.loc[:,column].idxmin()
            if column == score_dataframe.loc[k].idxmin():
#                 if score_dataframe.loc[k].min()<=0.8:
                if True:
                    score_dataframe.drop(columns=[column],inplace =True)
                    score_dataframe.drop(index=[k],inplace =True)
                    replace_dict.append((number_local_lang_text[column].group(0),\
                                         number_english_text[k],number_local_lang_text[column].span()[0]))
                else:
                    score_dataframe.drop(columns=[column],inplace =True)
    for column in score_dataframe.columns:
        replace_dict.append((number_local_lang_text[column].group(0),' ',number_local_lang_text[column].span()[0]))
    replace_dict = sorted(replace_dict,key=lambda x:x[2])
    edited_local_lang_sample_text = local_lang_sample_text
    look_from = 0
    for src,tgt,_ in replace_dict:
        iter_obj =re.finditer(r'\d+[.\\,:()\/\s\d]*\d+|\d{1}',edited_local_lang_sample_text)
        iter_local_lang__text = list(iter_obj)
        for idx,match_obj in enumerate(iter_local_lang__text):
            if src == match_obj.group(0) and match_obj.span()[0]>=look_from:
                open_brc_count_src = src.count('(')
                close_brc_count_src = src.count(')')
                open_brc_count_tgt = tgt.count('(')
                close_brc_count_tgt = tgt.count(')')
                look_from = len(edited_local_lang_sample_text[:match_obj.span()[0]]\
                            +' '\
                            + (max(0,open_brc_count_src-open_brc_count_tgt)\
                               +max(0,close_brc_count_tgt-close_brc_count_src))*'('\
                            +tgt\
                            + (max(0,close_brc_count_src-close_brc_count_tgt)\
                               +max(0,open_brc_count_tgt-open_brc_count_src))*')'\
                            +' ')
                edited_local_lang_sample_text=edited_local_lang_sample_text[:match_obj.span()[0]]\
                                            +' '\
                                            + (max(0,open_brc_count_src-open_brc_count_tgt)\
                                               +max(0,close_brc_count_tgt-close_brc_count_src))*'('\
                                            +tgt\
                                            + (max(0,close_brc_count_src-close_brc_count_tgt)\
                                               +max(0,open_brc_count_tgt-open_brc_count_src))*')'\
                                            +' '\
                                            + edited_local_lang_sample_text[match_obj.span()[1]:]
                break
    edited_local_lang_sample_text = edited_local_lang_sample_text.replace('( ','(').replace(' )',')')
    edited_local_lang_sample_text = ' '.join(edited_local_lang_sample_text.split())
    return edited_local_lang_sample_text