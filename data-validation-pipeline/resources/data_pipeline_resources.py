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
            content = request.json
            if("dataset_type" in content):

                dataset_type = content['dataset_type']

            if("operation" in content):

                operation = content['operation']

            if("inputfile" in content):

                inputfile  = content['inputfile']

            if("encoding" in content):

                enctype  = content['encoding']

            if("language1" in content):

                language1 = content['language1']

            if("language2" in content):

                language2 = content['language2']

            startTime = datetime.now()

            if(inputfile[-3:] == "txt"):
                df= pd.read_csv(inputfile, header=None, sep='\n', encoding=enctype)
            if(inputfile[-3:] == "csv"):
                df= pd.read_csv(inputfile, header=None, encoding=enctype)

            def savedf(dfx):

                dfname = "Output/validated_"+str(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))+"_"+dataset_type+"_"+operation+".csv"

                if not os.path.exists(os.path.dirname(dfname)):

                    try:
                        os.makedirs(os.path.dirname(dfname))

                    except:
                        print("Create a folder named  'Output' ")  

                dfx.to_csv(dfname , index=False)

                outputjson ={
                    "operation":operation,
                    "inputfile":inputfile,
                    "inputrows":len(df),
                    "outputfile":dfname,
                    "outputrows":len(dfx),
                    "drop": len(df)-len(dfx),
                    "Time_Taken" : str(datetime.now() - startTime)
                }

                print(outputjson)
                return jsonify(outputjson)


            if(dataset_type == 'SINGULAR'):

                df.columns =['L1']
                if(operation=="PRIMARY_CLEANER"):

                    df1 = singularcleanerfn(df, language1)
                    return savedf(df1)

                if(operation=="SPELL_CHECKER"):
                    df2 = spell_corrector(df, language1,None)
                    return savedf(df2)
                    # pass

                if(operation=="SANITY_CHECKER"):

#                     df3 = number_sequence_corr(df, language1, language2)
                    return savedf(df)
                    pass

                if(operation=="ALL"):

                    df1 = singularcleanerfn(df, language1)
                    df2 = spell_corrector(df1, language1,None)
                    # df3 = sanitycheckerfn(df2, language1)
                    return savedf(df2)


            if(dataset_type == 'PARALLEL'):

                df.columns =['L1','L2']
                if(operation=="PRIMARY_CLEANER"):

                    df1 = parallelcleanerfn(df, language2)
                    return savedf(df1)

                if(operation=="SPELL_CHECKER"):
                    print(language2)
                    df2 = spell_corrector(df, language1, language2)
                    print(df2.head())
                    return savedf(df2)
                    pass

                if(operation=="SANITY_CHECKER"):

                    df3 = number_sequence_corr(df, language1, language2)
                    return savedf(df3)
                    pass

                if(operation=="ALL"):

                    df1 = parallelcleanerfn(df, language2)
                    df2 = spell_corrector(df1, language1, language2)
                    df3 = number_sequence_corr(df1, language1, language2)
                    return savedf(df3)
                
              
            return post_error("Parameter Error", "Given parameter mismatch with supported ones", None), 400

        except Exception as e:

            return post_error("Exception Occoured", str(e), None), 400


