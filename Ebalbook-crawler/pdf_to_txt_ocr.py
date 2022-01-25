import os
import sys
import json
import codecs
import config
import logging
import requests
from time import sleep

logging.basicConfig(level=logging.INFO, filename=config.LOGS, format='%(asctime)s-%(levelname)s-%(message)s')


class TokenizePdf:
    
    def __init__(self,input):
        self.path = input[0]
        self.header = {'auth-token' :input[1] }
        self.upload()
        self.get_language()
        #self.get_language2()
        self.ocr_and_tokenize()
        self.download_file()
        self.write_to_txt()


    def upload(self):
        logging.info('Processing file {}'.format(self.path))
        self.file_name = self.path.split('/')[-1].split('.')[0]
        files = [('file',(open(self.path,'rb')))]
        try : 
            response = requests.post(config.UPLOAD, headers=self.header, files=files)
            self.file_id = response.json()['data']
            logging.info('{} upload response : {}'.format(self.file_name,response.json()))
        except Exception as e :
            logging.error('Error in processin {} due to {}  \n {}'.format(self.file_name ,e,response.json()),exc_info=True)
            self.file_id = None

    def get_language(self):
        if self.file_id is not None :
            self.lang = self.file_name.split('_')[-1]
            logging.info('Language detected {}'.format(self.lang))
            if len(self.lang) is not 2 :
                logging.error('Invalid laguage code {} for file {}'.format(self.lang, self.file_name))
                self.lang = None
        else:
            self.lang = None

    # def get_language2(self):
    #     if self.file_id is not None :
    #         self.lang = self.file_name.split('/')[-1].split('.')[0]
    #         logging.info('Language detected {}'.format(self.lang))
    #         if len(self.lang) is not 2 :
    #             logging.error('Invalid laguage code {} for file {}'.format(self.lang, self.file_name))
    #             self.lang = None
    #     else:
    #         self.lang = None


    def ocr_and_tokenize(self):
        if self.lang is not None:
            self.init_request()
            self.tok_json = self.bulk_serach()
        else:
            self.tok_json = None




    def init_request(self):
        try :
            file = {
                    "workflowCode":config.WF_CODE,
                    "files": [{ "path":str(self.file_id),
                                "type":"pdf",
                                "locale":self.lang,
                                 "config":{"OCR": {"option": "HIGH_ACCURACY","language": self.lang, "top_correction": "False", "craft_word": config.craft_word, "craft_line": config.craft_line, "line_layout": config.line_layout,"mask_image":"False"}
                            }}]
                    }

            logging.info('OCR and Toeknization statred  for {}'.format(self.file_name))
            res  = requests.post(config.WF_INIT,json=file,headers=self.header)
            self.job_id = res.json()['jobID']
        except Exception as e:
            logging.error('Error in initiating WF request for {} due to {} '.format(self.file_name ,e),exc_info=True)
            self.job_id = None


    def bulk_serach(self):
        if self.job_id is not None :
            bs_request = {
        "jobIDs": [self.job_id],
        "taskDetails":"false"
        }
        logging.info('process started for file  {} with job id {}'.format(self.file_name,self.job_id))        
        res = requests.post(config.SEARCH,json=bs_request,headers=self.header, timeout = 70000)
        #print(res.json()['jobs'][0]['status'])
        retry=0
        while(1):
            
            try :
                r_j = res.json()
                progress = r_j['jobs'][0]['status']
                #print(progress)
                
            except Exception as e :
                logging.error('Error in bulk serach for {} due to {} '.format(self.file_name ,e),exc_info=True)
                progress='p'
                retry +=1
            res = requests.post(config.SEARCH,json=bs_request,headers=self.header, timeout = 70000)   
             
            if retry > 100:
                return None
             
            
            if progress in ['COMPLETED','FAILED','SUCCESS']:
                if progress is 'FAILED':
                    logging.error('Process faild for file  {} with job id {} '.format(self.file_name,self.job_id ))
                    return None
                else :
                    print(progress)
                    print(r_j)
                    outputfile = r_j['jobs'][0]['output'][0]['outputFile']
                    print(outputfile)
                    return outputfile
            sleep(10)
            
            


    def download_file(self):
        if self.tok_json is not None:
            try:
                download_url = config.DOWNLOAD + str(self.tok_json)
                res = requests.get(download_url,headers=self.header)
                # print(res)
                # shuck = res.json()
               # print(shuck)
                # with open(json_path, "w", encoding='utf-16') as write_file:
                #         json.dump(shuck , write_file,ensure_ascii=False )
                self.o_tk_json = res.json()
                save_folder_name = self.path.split('/')[-2]
                self.save_dir = os.path.join(config.OUTPUT_DIR , save_folder_name)
                os.system('mkdir -p {}'.format(self.save_dir))
                if config.SAVE_JSON:
                    json_path = os.path.join(self.save_dir,'{}.json'.format(self.file_name))
                    with open(json_path, "w", encoding='utf-8') as write_file:
                        json.dump(self.o_tk_json , write_file,ensure_ascii=False )
            except Exception as e:
                logging.error('Error in downloading file  {} \n {}  '.format(self.tok_json,e ),exc_info=True)
                self.o_tk_json =None
        else:
            self.o_tk_json = None


    def write_to_txt(self):
        if self.o_tk_json is not None:
            try:
                file_path = os.path.join(self.save_dir,'{}.txt'.format(self.file_name))
                os.system('rm {}'.format(file_path))
                for page in self.o_tk_json['outputs'][0]['pages']  :
                    for region in page['regions']:
                        if 'tokenized_sentences' in region.keys():
                            for sentence in region['tokenized_sentences'] :
                                with open(file_path, "a", encoding ='utf-16') as txtfile:
                                    txtfile.write("{}\n".format(sentence['src']))
                            # f = codecs.open(file_path, encoding='utf-16', errors='strict')     #to check utf16
                res = []                                                                       #print less than 3 words in the file
                with open(file_path, 'r', encoding = 'utf-16') as tosplit:
                    read = tosplit.readlines()
                for seg in read:                                            
                    temp = seg.split()
                    # print(temp)
                    if(len(temp)>3):
                        res.append(seg)
                        # print(res)
                        with open(file_path, 'w', encoding = 'utf-16') as splittedfile:
                            for x in res:
                                splittedfile.write(x)
                            splittedfile.close()

                logging.info('file {} successfully processed '.format(self.file_name))
            except Exception as e:
                 logging.error('Error occured during writing to txt for file {} \n {} '.format(self.file_name ,e),exc_info=True)
            except UnicodeError:                                                               #to write to
                print('conversion')
                with open(file_path, 'rb') as source_file:
                    with open(file_path, 'w+b') as dest_file:
                        contents = source_file.read()
                        dest_file.write(contents.decode('utf-8').encode('utf-16'))




            
            

