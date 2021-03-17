#  Sakshi Website sentence scraper 

## overview 

sakshi website is having the news in three languages  which  are  Telugu,Hindi,English

By using these files we can get the data and urls of sakshi news for perticular month and year .



###  urls-crawler : 

using this urls-crawler we can get urls of perticular  month at one time  , every time we need to change the inputs of this file if we want different month and language urls ,and these inputs  are hard coded .



the inputs of this file are : 1) months_back  2) lan  3)output_file_name 

 1) months_back : this variable takes value that is how many months back data you want . for eg : if we specify the months_back=2 , and   assume present mar2021 then it scrap all the urls in the month of jan 2021 .
 
 2) lan  :  we have to provide the language  code  (hi/te/en) , if we specify the lan='en' then it scrap the english urls .  there are only three languages available we have to specify one of three 
 
 3) outputfile_name :  name of output csv  file and path , in which you want to store urls.
 
### data-crawler-and-tokenizer  :
 
 the output of this file is tokenized sentences 
 
 the inputs of this file are :  1)lan  2) url_file_name  3) output_file_name
 
 1) lan : which represents language of urls data 
 
 2)url_file_name :  csv file which is having the all urls , csv file that should contain all urls in first column , usually we take  the csv files from above urls_crawler output
 
 3)output of file  :we have to  specify the path and text filename to store all tokenized text , we get this text from all urls .
 
