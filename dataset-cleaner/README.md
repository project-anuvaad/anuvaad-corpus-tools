# Dataset-cleaner

## Overview

The code in this repo could be utilized to cleanse dataset prepared for Project Anuvvad by scraping from various sources. 
It mainly does remove bullets, numbering, unnecessary spacing, unwanted characters and misplaced lingual entries from each parallel/singular dataset.

The 4 files starting with name "exec_" could be executed independently from the terminal by specifying necessary arguments.

The remaining 2 files could be imported in python directly, and dataframes could be passed to obtain the cleaned output.

To install necessary packages for the script, run:

    pip install -r requirements.txt

To view script usage help from terminal, run:

    python3 exec_[scriptname].py -h

IMPORATNT : Update the BEARER_TOKEN in constants.py before using network related scripts.

### exec_alignfiles.py

The script accepts 2 TXT files as input and initiates the Aligner service.

To initiate the process:

    python3 exec_alignfiles.py -sc "./mal.txt" -l "ml" -tg "./eng.txt"

NOTE : The Target file must necessarily be in English, logs of initiated jobs will be saved in aligner_log.txt for future reference.


### exec_jobid_datasetmaker.py

The script creates cleansed dataset directly by specifying the Workflow Job-ID as input ( Aligner is developed to obtain matching Bi-Lingual sentence pairs, as two text files. Refer other Repos of the same project for details on the same).

This script could be executed independently from the command line. It accepts arguments such as:

* -j : Workflow Job ID
* -o : Output directory to save resultant CSV files ( optional)

To initiate the process:

    python3 exec_jobid_datasetmaker.py -j "WF-JOB-ID"  -o "/home/downloads/output/"

Once executed, 3 output files will be generated.

* Exactly matching cleaned parallel dataset
* Almost Matching cleaned parallel dataset
* No Match sentences text file

### exec_parallel_datasetcleaner.py

The script accepts a 2 column dataset as input and provides the cleaned parallel dataset as output.

This script could be executed independently from the command line. It accepts arguments such as:

* -i : input dataset filename
* -o : Output filename
* -s : second column language
* -e : encoding type of input dataset

NOTE: The input dataset must only have 2 columns and the first column must necessarily be in English.

To initiate the process:

    python3 exec_parallel_datasetcleaner.py -i "./en_hi_dataset.csv" -s "hi" -e "utf-16"  -o "./en_hi_cleaned.csv" 

### exec_singular_datasetcleaner.py

The script accepts a Text file or 1 column dataset as input and provides the cleaned file as output.

This script could be executed independently from the command line. It accepts arguments such as:

* -i : input dataset filename
* -o : Output filename
* -l : language code
* -e : encoding type of input dataset

To initiate the process:

    python3 exec_singular_datasetcleaner.py -i "./hi_sentences.txt" -l "hi" -e "utf-16"  -o "./hi_cleaned.txt"

 ### Cleaning datasets directly from code

 The files "parallelcleaner.py" and "singularcleaner.py" are standalone functions and could be imported and used directly from python as any other modules are used.

Exemplary cleaner usage in python:

    import pandas as pd
    from parallelcleaner import parallelcleanerfn
    from singularcleaner import singularcleanerfn

    df1= pd.read_csv("./en_hi_dataset.csv", header=None)
    df = pd.DataFrame()
    df = parallelcleanerfn(df1, "hi")

    

    df2= pd.read_csv("./hi_dataset.txt", header=None, sep='\n')
    df = pd.DataFrame()
    df = singularcleanerfn(df2, "hi")

    # to call the same function parallely as chunks in case of large datasets

    chunksize = 10000
    cleaneddf = pd.DataFrame()
    for i in range(int(df.shape[0]/chunksize)+1):

        tempdf = parallelcleanerfn(df.loc[i*chunksize:(i+1)*chunksize-1,:],"hi")
        cleaneddf = cleaneddf.append(tempdf)
        print(f'{i} iteration done')

NOTE : Regular expressions could be added/removed in the file regxlist.py
