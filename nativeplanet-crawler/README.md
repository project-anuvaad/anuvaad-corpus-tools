# nativeplanet scraper 

this is help to scrap the data from nativeplanet website , by  place / state  wise . nativeplanet is a tourism website  and data  available in 6 languages those are english , telugu , hindi,malayalam,tamil,kannada .



To execute this file you should have install selenium and beautifulsoup in your system . 


## inputs :

the inputs of this file are  : 1 ) link 2) lan 3) outputfile name

1) link : we should provide the link of the website where data is presentd in native planet 

          eg : if i want the total data of delhi place in hindi language then we should  follow the below steps 
          
          * go to https://telugu.nativeplanet.com/   -- > select the language  'hindi'  --> select places  option  --> click on delhi --> click on attractions  
           
           then get that link url and give url to the  link variable in this script  .
           
           final link is like this : https://hindi.nativeplanet.com/delhi/attractions/#gurudwara-sis-ganj
           
 2) lan : this specifies the language of the data , means which language data  that above link contains . eg:'hi'

3) outputfile name :  we should give name of the output text file to store that whole scraped data 

## output :

the output of this crawler is text file which contains sentences  related to perticular place/ state .
