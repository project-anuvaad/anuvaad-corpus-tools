

#file location
INPUT_DIR='/home/test/Project_Anuvaad/samagra/'  
OUTPUT_DIR='/home/test/Project_Anuvaad/samagra/'


BATCH_SIZE=4
LOGS='ocr_tok_new_dev_from_dec7.log'


SAVE_JSON=True
OVERWRITE=False


LOGIN='https://auth.anuvaad.org/anuvaad/user-mgmt/v1/users/login'
USER="navneet.kumar@tarento.com"
PASS="Srikara@1234"



#WF CONFIG DEV
WF_INIT= "https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/async/initiate"
WF_CODE  = "WF_A_FCWDLDBSOD15GVOTK_S"
SEARCH='https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/jobs/search/bulk'
DOWNLOAD="https://auth.anuvaad.org/download/"
UPLOAD='https://auth.anuvaad.org/anuvaad-api/file-uploader/v0/upload-file'



craft_word="False"
craft_line="False"
line_layout = "False"


