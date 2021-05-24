from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


headings_list = []
dates_list = []
link_list = []
count = 2
'''def refresh():
        try:
            element = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@title=f"{count}"]')))
            element.click()
            time.sleep(1)
        except Exception as e:
            print(f"Not clickable...refreshing page {count}")
            driver.refresh()
            refresh()'''
driver = webdriver.Chrome('chromedriver')

while (count<=7978):
    driver.get(f"https://www.kolkata24x7.com/category/national-news/page/{count}")
    #refresh()     
    headings = driver.find_elements_by_xpath('//div[@class="td-block-span6"]/div[@class="td_module_1 td_module_wrap td-animation-stack"]/h3[@class="entry-title td-module-title"]/a[@href]')
    for p in range(len(headings)):
        headings_list.append(headings[p].text)
        
    date = driver.find_elements_by_xpath('//div[@class="td-block-span6"]/div[@class="td_module_1 td_module_wrap td-animation-stack"]/div[@class="td-module-meta-info"]/span[@class="td-post-date"]/time[@class="entry-date updated td-module-date"]')
    for p in range(len(date)):
        dates_list.append(date[p].text)
    
    elements = driver.find_elements_by_css_selector("div.td-block-span6 > div.td_module_1.td_module_wrap.td-animation-stack > h3.entry-title.td-module-title > a")
    for element in elements:
        link_list.append(element.get_attribute("href"))
    count=count+1
    
df = pd.DataFrame({'Headings': headings_list, 'Date': dates_list, 'Link': link_list}) 
time.sleep(1)
print ("Complete")
driver.quit()
df.to_csv('Bengali_articles_list_ie_india.csv',
            mode='w',
            encoding='utf-16',
            index=False,
        )