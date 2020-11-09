# Dataset-cleaner

## Overview

The code in this repo could be utilized to cleanse dataset prepared for Project Anuvvad by scraping from various sources. 
It mainly does remove bullets, numbering, unnecessary spacing, unwanted characters and misplaced lingual entries from each parallel/singular dataset.

The 3 files starting with name "exec_" could be executed independently from the terminal by specifying necessary arguments.

The remaining 2 files could be imported in python directly, and dataframes could be passed to obtain the cleaned output.

To install necessary packages for the script, run:

    pip install -r requirements.txt

To view script usage help from terminal, run:

    python3 exec_[scriptname].py -h


#### exec_jobid_datasetmaker.py

The script creates cleansed dataset directly by specifying the Alignment Job-ID as input ( Aligner API is made to obtain matching Bi-Lingual sentence pairs, in two text files. Refer other Repos of the same project for details on the same).

This script could be executed independently from the command line. It accepts arguments such as:

* -j : Aligner Job ID
* -s : Second language code, i.e language other than English
* -o : Output directory to save resultant CSV files ( optional)

To initiate the process:

    python3 exec_jobid_datasetmaker.py -j "ALIGN-JOB-ID" -s "hi" -o "/home/downloads/output/"

Once executed, 3 output files will be generated.

* Exactly matching cleaned parallel dataset
* Almost Matching cleaned parallel dataset
* No Match sentences text file

#### exec_parallel_datasetcleaner.py

The script accepts a 2 column dataset as input and provides the cleaned parallel dataset as output.

This script could be executed independently from the command line. It accepts arguments such as:

* -i : input dataset filename
* -o : Output filename
* -s : second column language
* -e : encoding type of input dataset

NOTE: The input dataset must only have 2 columns and the first column must necessarily be in English.

To initiate the process:

    python3 exec_parallel_datasetcleaner.py -i "./en_hi_dataset.csv" -s "hi" -e "utf-16"  -o "./en_hi_cleaned.csv" 

#### exec_singular_datasetcleaner.py

The script accepts a Text file or 1 column dataset as input and provides the cleaned file as output.

This script could be executed independently from the command line. It accepts arguments such as:

* -i : input dataset filename
* -o : Output filename
* -l : language code
* -e : encoding type of input dataset

To initiate the process:

    python3 exec_singular_datasetcleaner.py -i "./hi_sentences.txt" -l "hi" -e "utf-16"  -o "./hi_cleaned.txt"

 #### Cleaning datasets directly from code

 The files "parallelcleaner.py" and "singularcleaner.py" are standalone functions and could be imported and used directly from python as any other modules are used.

Exemplary cleaner usage in python:

    import pandas as pd
    from parallelcleaner import parallelcleanerfn
    from singularcleaner import singularcleanerfn

    df1= pd.read_csv("./en_hi_dataset.csv", header=None)
    df = pd.DataFrame()
    df = parallelcleanerfn(df1, "hi")

    

    df2= pd.read_csv("./hi_dataset.csv", header=None)
    df = pd.DataFrame()
    df = parallelcleanerfn(df2, "hi")


