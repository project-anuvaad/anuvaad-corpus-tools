import os
import ast
import pandas as pd
from flask import request,jsonify
from anuvaad_auditor.loghandler import log_info, log_exception
from anuvaad_auditor.errorhandler import post_error
from datetime import datetime
from utilities import singularcleanerfn,parallelcleanerfn,number_sequence_corr,spell_corrector
from flask_restful import fields, marshal_with, reqparse, Resource


class DataResources(Resource):

    def post(self):

        try:

            #read all content from input body
            content = request.json
            if("dataset_type" in content):

                dataset_type = content['dataset_type']

            if("module_name" in content):

                module_name = content['module_name']

            if("input_file" in content):

                input_file  = content['input_file']

            if("enc_type" in content):

                enc_type  = content['enc_type']

            if("src_lang" in content):

                src_lang = content['src_lang']

            if("dest_lang" in content):

                dest_lang = content['dest_lang']

            startTime = datetime.now()

            #reads input file into dataframe
            if(input_file[-3:] == "txt"):
                df= pd.read_csv(input_file, header=None, sep='\n', encoding = enc_type)
            if(input_file[-3:] == "csv"):
                df= pd.read_csv(input_file, header=None, encoding = enc_type)

            #function to save final output and return details in body
            def savedf(output_df):

                #output is saved to a folder in root directory named Output
                output_file = "Output/validated_"+str(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))+"_"+dataset_type+"_"+module_name+".csv"

                if not os.path.exists(os.path.dirname(output_file)):

                    try:
                        os.makedirs(os.path.dirname(output_file))

                    except:
                        print("Create a folder named  'Output' ")  

                output_df.to_csv(output_file , index=False)

                #output response body
                outputjson ={
                    "module_name":module_name,
                    "input_file":input_file,
                    "input_rows":len(df),
                    "output_file":output_file,
                    "output_rows":len(output_df),
                    "drop": len(df)-len(output_df),
                    "time_taken" : str(datetime.now() - startTime)
                }

                return jsonify(outputjson)

            #operations to handle single column dataset
            if(dataset_type == 'singular'):

                df.columns =['L1']
                
                if(module_name=="primary_cleaner"):

                    df1 = singularcleanerfn(df, src_lang)
                    return savedf(df1)

                if(module_name=="spell_checker"):
                    df2 = spell_corrector(df, src_lang,None)
                    return savedf(df2)

                if(module_name=="sanity_checker"):

                    return post_error("Parameter Error", "Sanity checker supports only parallel datasets for now", None), 400


                if(module_name=="all"):

                    #executes basic cleaner and spell checker in order, one after other
                    df1 = singularcleanerfn(df, src_lang)
                    #passes basic cleaner output dataframe to spell_checker
                    df2 = spell_corrector(df1, src_lang,None)
                    return savedf(df2)


            #operations to handle double column dataset [ column 1 is expected to be english ]
            if(dataset_type == 'parallel'):

                df.columns =['L1','L2']
                if(module_name=="primary_cleaner"):

                    df1 = parallelcleanerfn(df, dest_lang)
                    return savedf(df1)

                if(module_name=="spell_checker"):
                    df2 = spell_corrector(df, src_lang, dest_lang)
                    return savedf(df2)

                if(module_name=="sanity_checker"):

                    df3 = number_sequence_corr(df, src_lang, dest_lang)
                    return savedf(df3)


                if(module_name=="all"):
                    #executes basic cleaner, spell checker and sanity checker in order, one after other
                    df1 = parallelcleanerfn(df, dest_lang)
                    #passes basic_cleaner output to spellchecker
                    df2 = spell_corrector(df1, src_lang, dest_lang)
                    #passes spell_checker output to sanity_checker
                    df3 = number_sequence_corr(df2, src_lang, dest_lang)
                    return savedf(df3)
                
              
            return post_error("Parameter Error", "Given parameter mismatch with supported ones", None), 400

        except Exception as e:

            return post_error("Sorry, Exception occoured", str(e), None), 400


