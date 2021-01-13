# DATA VALIDATION PIPELINE

## Overview


<p align="center"> 
<img src="https://i.imgur.com/IYeXwV6.jpg">
</p>


In an NLP based project such as Anuvaad the quality of Data which is provided to train the model is of utmost importance.The Data validation pipeline is designed to ensure the quality of dataset which is fed to the NMT model which acts as the core of translation.The pipeline is in a development stage and as of now it has three modules (individual modules available under utils folder)

* Primary dataset cleaner
* Spell checker 
* Sanity checker

Each modules could be used intividually or all together as per the need, by specifying parameters accordingly.

#### 1. Primary dataset Cleanser

The primary dataset cleaner module cleans up the whole singular/parallel dataset to ensure basic sentence correction.

It mainly does things like :

*  Avoid whitespaces
*  Removes wrong-language sentences from a dataset
*  Removes un-necessarily placed special characters
*  Removes un-necessary HTML Tags in between sentence
*  Removes bullets, numbering and similar unwanted characters from the beginning of a sentence.
*  In case of parallel datasets, it drops of the corresponding row in case if a particular field is found wrong.

Third party library used:

    Langdetect: https://pypi.org/project/langdetect
    
Usage:

    import pandas as pd
    from parallelcleaner import parallelcleanerfn
    from singularcleaner import singularcleanerfn

    df1= pd.read_csv("./en_hi_dataset.csv", header=None)
    df = pd.DataFrame()
    df = singularcleanerfn(df1, "hi")

    df2= pd.read_csv("./hi_dataset.txt", header=None, sep='\t')
    df = pd.DataFrame()
    df = parallelcleanerfn(df2, "hi")

#### 2. Spell Checker

#### Spell checker currently supports only English in SINGULAR files

Spell Checker/Corrector is still under development and for now implemented using:

    Hunspell : http://hunspell.github.io/

A python binding of the above named cyhunspell is used. The exposed API is:

    Method name         :   spell_corrector
    Input Parameters    :   Pandas Dataframe consisting of one sentence per row in column L1, language1, language2
    Output              :   Pandas Dataframe consisting of corrected sentence per row in column L1

#### 3. Sanity Checker
#### 3.1. Number Sequence Fix

Third party library:
    
    https://github.com/luozhouyang/python-string-similarity
    
Description/Purpose:

* Fix wrongly translated number.
* Extract number(English Number System) sequence from parallel sentences and match/sort them based on longest common subsequence (LCS) with additional penalty for difference in sequence length.
* Number-sequences in one of the parallel sentence will be considered as ground truth and number sequences in other sentence will be replaced by number sequences from first one

Usage:

    from number_sequence_corrector import number_sequence_corr
    dataframe_number_sequence_corrected = number_sequence_corr(dataframe_number_sequence_incorrect,lang1,lang2)

Note:
1. In dataframe_number_sequence_incorrect first columns must be sentence which has correct number sequence in english number system and 2nd column must be sentence with incorrect number sequence in english number system.
2. Currently 2nd and 3rd argument in fuction(number_sequence_corr) call is not required and has default value of 'english and 'local' respectively.



## Pipeline Usage

To install necessary packages for the script, run:

    pip install -r requirements.txt

This is designed as a flask API. To start the flask server run :

    python3 app.py

API Endpoint : 

    http://0.0.0.0:5001/data_pipeline/dataset_validation

Input parameters :

    "dataset_type"    : Specifies the type of dataset provided as input.

                        accepted formats:

                        "SINGULAR" - For txt files or single column csv/tsv files
                        "PARALLEL" - For two-column CSV files out of which first one is English and next is of a regional language

    "operation"       : Specify which module of the pipeline must be executed.

                        accepted inputs:

                        "PRIMARY-CLEANER"
                        "SPELL_CHECKER"
                        "SANITY_CHECKER"
                        
                        "ALL" - > Performs all the three above said operations in order.

    "inputfile"       : Specifies the location of the input dataset

    "encoding"        : Specifies encoding format of the input dataset

    "language1"       : Specifies language of the first column of the dataset

    "language2"[optional] : specifies language of second column of dataset

Output:

    "drop"          :   Number of rows dropped wrt input dataset

    "inputfile"     :   input file path

    "inputrows"     :   Number of rows in the input dataset

    "operation"     :   Specify module/ALL

    "outputfile"    :   path of generated outputfile

    "outputrows"    :   Number of rows in outputfile
    
    "timetaken"     :   Total time taken to perform the operation

At the end, the generated output files could be found under the 'Output' folder 

#### Usage Example:

API Endpoint : 

    http://0.0.0.0:5001/data_pipeline/dataset_validation

INPUT(body) :

    {
        "operation"      :  "PRIMARY_CLEANER",
        "dataset_type"   :   "SINGULAR",
        "inputfile"      :  "/home/user2/Desktop/rest_api_demo/abc.txt",
        "encoding"       :  "utf-8",
        "language1"      :  "en",
        "language2"      :  "en"
    }

OUTPUT(body) :

    {
        "timetaken"     :   "0:00:00.600161",
        "drop"          :   1,
        "inputfile"     :   "/home/user2/Desktop/rest_api_demo/abc.txt",
        "inputrows"     :   6,
        "operation"     :   "PRIMARY_CLEANER",
        "outputfile"    :   "Output/validated_2021_01_10-01_40_44_AM_SINGULAR_PRIMARY_CLEANER.csv",
        "outputrows"    :   5
    }


