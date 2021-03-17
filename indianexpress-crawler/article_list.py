
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
    argv[0] --> language,
    argv[1] --> sections or topic.  '''

lang = str(sys.argv[0])
section = str(sys.argv[1])

driver = webdriver.Chrome('chromedriver')

if (lang == 'tamil'):
    driver.get(f" 'https://tamil.indianexpress.com/section/{section}' ")
elif (lang == 'hindi'):
    driver.get(f" 'https://www.jansatta.com/section/{section}' ")
elif (lang == 'english'):
    driver.get(f" 'https://indianexpress.com/section/{section}' ")
elif (lang == 'malayalam'):
    driver.get(f" 'https://malayalam.indianexpress.com/section/{section}' ")
elif (lang == 'bengali'):
    driver.get(f" 'https://bengali.indianexpress.com/section/{section}' ")
elif (lang == 'marathi'):
    driver.get(f" 'https://www.loksatta.com/section/{section}' ")
else:
    print ("Please provide valid language") 
    
headings_list, dates_list, link_list = [],[],[] 
count = 0

def refresh():
        try:
            element = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="next page-numbers"]')))
            element.click()
            time.sleep(1)
        except Exception as e:
            print(f"Not clickable...refreshing page {count}")
            driver.back()
            refresh()

while True:
    refresh()    
    headings = driver.find_elements_by_xpath('//h2[@class="head"]')
    for p in range(len(headings)):
        headings_list.append(headings[p].text)
        
    date = driver.find_elements_by_xpath('//span[@class="byline"]')
    for p in range(len(date)):
        dates_list.append(date[p].text)
    
    elements = driver.find_elements_by_css_selector("h2.head a")
    for element in elements:
        link_list.append(element.get_attribute("href"))  
    count=count+1

df = pd.DataFrame({'Headings': headings_list, 'Date': dates_list, 'Link': link_list}) 
time.sleep(1)
print ("Complete")
driver.quit()
df.to_csv(f" '{lang}_articles_list_{section}_2021.csv' ",
    mode='w',
    encoding='utf-16',
    index=False,
)

