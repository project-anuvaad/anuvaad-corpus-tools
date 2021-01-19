#File contains code to scrape & create En-Hi CSV from newsonair

import re
import time
import pandas as pd
from ast import literal_eval
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from indicnlp.tokenize import sentence_tokenize
from nltk.tokenize import sent_tokenize 


ENG_URL = "http://newsonair.com/Text-Archive-Search.aspx"
HIN_URL = "http://newsonair.com/hindi/Hindi-Text-Archive-Search.aspx"
FROM_DATE = "arguments[0].setAttribute('value', '09/01/2020 12:00 AM')"
TO_DATE = "arguments[0].setAttribute('value','09/2/2020  12:00 PM')"

#temporary output file paths
ENG_CSV = "/home/eng_csv.csv"
HIN_CSV = "/home/hin_csv.csv"


#function to scrap URL's
#status WIP. It works but might hang in between without switching page
def get_href(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    a=driver.find_element_by_id('ctl00_ContentPlaceHolder1_from_Date_txt')
    driver.execute_script(FROM_DATE,a)
    b=driver.find_element_by_id('ctl00_ContentPlaceHolder1_to_Date_txt')
    driver.execute_script(TO_DATE, b)
    driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Button1"]').click()
    j=100
    href_links=[]
    

    t_end = time.time() + 60
    while time.time() < t_end:
        try:
            driver.implicitly_wait(5)
            parent=driver.find_element_by_id('ctl00_ContentPlaceHolder1_pnlHelloWorld')
            driver.implicitly_wait(5)
            links1=parent.find_elements_by_tag_name("a")
            for el in links1:
                    if el.get_attribute('href') == None or not re.search('^http', el.get_attribute('href')):
                        break
                    else:
                        # print(el.get_attribute("href"))
                        if el.get_attribute("href") not in href_links:
                            href_links.append(el.get_attribute("href"))
              
            driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lbNext"]').click()    
                    
            
        except Exception as e:
            print(e)
            pass
    print(len(href_links))
    return(href_links)



def get_df(link1):

        date = []
        timex = []
        title = []
        data = []
        links = []

        href_links = get_href(link1)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        for link2 in href_links:
            
            try :
                print(link2)
                driver.get(link2)
                user_data=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_FormView1"]/tbody/tr/td')            
                # get the whole body text 
                text_data=user_data.text  
                list2=text_data.split('\n')
                #get date      
                date.append(list2[0])
                # get time  
                timex.append(list2[2])         
                #get title   
                title.append(list2[3])         
                # get all the data 
                sentences=[sen.strip() for sen in list2[5:] if len(sen)>1]
                data.append(sentences)
                #get links 
                links.append(link2)
                
            except Exception as e:
                print('check the id',link2)
                print(e)
                
        df=pd.DataFrame()
        df['time']=timex
        df['date']=date
        df['title']=title
        df['link']=links
        df['data']=data
        print(df)
        return(df)

hi_df = get_df(HIN_URL)
hi_df.to_csv(HIN_CSV)

en_df = get_df(ENG_URL)
en_df.to_csv(ENG_CSV)
