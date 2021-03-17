import pandas as pd
import numpy as np
import re
import tqdm
from selenium.webdriver import ActionChains
from selenium import webdriver
import datetime
import time
import argparse
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



#inputs  required 

# here you need to specify how many months back data you want 
#eg : if i want 2 months back data urls , then i have to specify months_back=2 ,  so i get jan2021 urls (present mar2021 )
months_back=2

lan='te'       # please select the language , which urls you want  en/hi/te

oultput_filename='/home/telugu_urs.csv'  # plase mention the outputfile name to store urls


def get_english_urls(months_back):

    chrome_path='/home/test/Downloads/chromedriver'
    driver=webdriver.Chrome(chrome_path)
    link='https://english.sakshi.com/archive'
    driver.get(link)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="fromDate"]').click()
    for d in range(months_back):                                
        previous = driver.find_element_by_css_selector("body > div.datepicker-container.datepicker-dropdown.datepicker-top-left > div:nth-child(3) > ul:nth-child(1) > li:nth-child(1)")
        ActionChains(driver).click(previous).perform()
    html_list = driver.find_element_by_css_selector('body > div.datepicker-container.datepicker-dropdown.datepicker-top-left > div:nth-child(3) > ul:nth-child(3)')
    items = html_list.find_elements_by_tag_name("li")

    class_m=[]
    for item in items:
        class_m.append(item.get_attribute('class'))


    all_links1=[]
    for i in range(len(class_m)):


        if class_m[i]!='muted':
            driver.find_element_by_xpath('//*[@id="fromDate"]').click()
            lin="body > div.datepicker-container.datepicker-dropdown.datepicker-top-left > div:nth-child(3) > ul:nth-child(3) > li:nth-child("+str(i+1)+")"
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, lin))).click()
            driver.find_element_by_xpath('//*[@id="arch_button"]').click()
            time.sleep(5)
            parent=driver.find_element_by_xpath('//*[@id="node-1729"]/div/div/div/div')

            elems=parent.find_elements_by_tag_name("a")

            for elem in elems:

                all_links1.append(elem.get_attribute("href"))
    eng_links=[]
    for alll in all_links1:
        if  re.search('^https',str(alll)) :
            eng_links.append(alll) 
            
            
    return eng_links       
            

def get_telugu_urls(months_back):
    
    # you must have selenium install in your local system with specific path
    chrome_path='/home/test/Downloads/chromedriver'
    driver=webdriver.Chrome(chrome_path)
    link='https://www.sakshi.com/archive'
    driver.get(link)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="popupDatepicker"]').click()
    for d in range(months_back):                                    
        previous = driver.find_element_by_css_selector("body > div.datepicker-container.datepicker-dropdown.datepicker-top-left > div:nth-child(3) > ul:nth-child(1) > li:nth-child(1)")
        ActionChains(driver).click(previous).perform()
    html_list = driver.find_element_by_css_selector('body > div.datepicker-container.datepicker-dropdown.datepicker-top-left > div:nth-child(3) > ul:nth-child(3)')
    items = html_list.find_elements_by_tag_name("li")


    class_m=[]
    for item in items:
        class_m.append(item.get_attribute('class'))
    all_links=[]
    for i in range(len(class_m)):    
        if class_m[i]!='muted':
            driver.find_element_by_xpath('//*[@id="popupDatepicker"]').click()
            lin="body > div.datepicker-container.datepicker-dropdown.datepicker-top-left > div:nth-child(3) > ul:nth-child(3) > li:nth-child("+str(i+1)+")"
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, lin))).click()
            driver.find_element_by_xpath('//*[@id="arch_button"]').click()
            time.sleep(5)
            parent=driver.find_element_by_xpath('//*[@id="node-408940"]/div/div/div/div')

            elems=parent.find_elements_by_tag_name("a")


            for elem in elems:

                all_links.append(elem.get_attribute("href")) 
    tel_links=[]
    for alll in all_links:
        if  re.search('^https',str(alll)) :
            tel_links.append(alll)    
    
    
    return tel_links
    
def get_hindi_urls(months_back):
    
    chrome_path='/home/test/Downloads/chromedriver'
    driver=webdriver.Chrome(chrome_path)
    link='https://hindi.sakshi.com/archive'
    driver.get(link)


    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="fromDate"]').click()

    for d in range(months_back):                               
        previous = driver.find_element_by_css_selector("body > div.datepicker-container.datepicker-dropdown.datepicker-top-left > div:nth-child(3) > ul:nth-child(1) > li:nth-child(1)")
        ActionChains(driver).click(previous).perform()



    html_list = driver.find_element_by_css_selector('body > div.datepicker-container.datepicker-dropdown.datepicker-top-left > div:nth-child(3) > ul:nth-child(3)')
    items = html_list.find_elements_by_tag_name("li")
    class_m=[]
    for item in items:
        class_m.append(item.get_attribute('class'))


    all_links1=[]
    for i in range(len(class_m)):


        if class_m[i]!='muted':
            driver.find_element_by_xpath('//*[@id="fromDate"]').click()
            lin="body > div.datepicker-container.datepicker-dropdown.datepicker-top-left > div:nth-child(3) > ul:nth-child(3) > li:nth-child("+str(i+1)+")"
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, lin))).click()
            driver.find_element_by_xpath('//*[@id="arch_button"]').click()
            time.sleep(5)
            parent=driver.find_element_by_xpath('//*[@id="block-system-main"]')

            elems=parent.find_elements_by_tag_name("a")

            for elem in elems:

                all_links1.append(elem.get_attribute("href"))



    hindi_links=[]
    for alll in all_links1:
        if  re.search('^https',str(alll)) :
            hindi_links.append(alll)    


    return hindi_links



if lan=='en':
    all_urls=get_english_urls(months_back)
elif lan=='te':
    
    all_urls=get_telugu_urls(months_back)   
elif lan=='hi':
    all_urls=get_hindi_urls(months_back)
else:
    print('plase select the correct language code from  te/en/hi')
    
data=pd.DataFrame(all_urls)   
data.to_csv(oultput_filename,index=None)  
    
     
