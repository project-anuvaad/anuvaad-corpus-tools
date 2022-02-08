# Kerala textbook website crawler
       this consists of four languages
         1. Tamil 
         2. English 
         3.Malayalam
         4.Kannada


# Summary 
 	It is an education website where number of pdfs from standards one to 12 presides.Will be scraping the links of pdfs and run the tokenization for the breakdown of sentences to save them in the text files. Further proceeds with data preprocessing and aligning for parallel corpus.
         
     
# Topics for the entire scraping procedure

1.importing libraries:

2.Install Selenium Driver:

3.Select the available languages:

4.Select the available standards:

5.Select the available subjects:

6.download the file url:

7.automate the page to page view and download the file:
       
# Procedure
1. Specify the required libraries.
2. Can install each time to run the browser or can assign the path of the driver after installation.
3. Get the list of languages used.
4. Get the list of the standards used.
5. Get the list of subjects used.
6. By defining the file location, path and the url inside a function.
7. This website parse through medium->grades->subjects.
   Getting the file through a nested like process, where we can access the subjects only if we have the drop down of the grade selected.
   drop.select - used to get the list from dropdown.
   By running the code we are automating the website to parse through each of the page to identify the file and download to the specified path.



