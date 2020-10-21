from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException,WebDriverException,ElementClickInterceptedException,TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from pathlib import Path
import time
import pandas as pd
import os
import winsound


#Create chrome webdriver object 
#Input: -
#Output: webdriver object
def get_driver():
    try:
        executable_path = "Path\to\your\chromedriver.exe"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        webdriver1 = webdriver.Chrome(executable_path=executable_path,options=chrome_options)
        return webdriver1
    except WebDriverException as e:
        print(e)
        get_driver()

#Scrape PIB webpage using div with id PdfDiv
#Input: Source code of the webpage to scrape (page_source)
#Output: List of all the paragraphs or sentences in the given source
def write_text(page_source):
    return_text = []
    soup = BeautifulSoup(page_source,"html.parser")
    div = soup.find("div",attrs={"id":"PdfDiv"})
    table = div.find("table")
    td = table.find("td")
    divs = td.find_all("div")
    wrote_text = ""
    for i,div in enumerate(divs):
        if(len(div.find_all("div")) > 0 and i < 5 ):
            for s in str(div).split("</div>"):
                s=s.replace("<div style='font-weight: 200; text-align: center; font-size: 30px;'>","")
                s = s.replace("<div style='height:30px;width:100%;'>","")
                if(s.strip() != ""):
                    return_text.append(s.strip())
            continue
        if(div.get_text().strip() != "" and "Release ID:" not in div.get_text() and div.get_text().strip() not in wrote_text and "Posted On:" not in div.get_text()):
            text = " ".join(div.get_text().split('\r'))
            remove_text = ""
            if(len(div.find_all("table")) != 0):
                for t in div.find_all("table"):
                    remove_text += " ".join(t.get_text().strip().split())
                    text = text.replace(remove_text,"")
                    remove_text = ""
            return_text.append(text)
            wrote_text += div.get_text().strip().replace(remove_text,"")
    return return_text


def get_prid2(date,month,year,url,dri,list_rid,memo):
    lang = "Hindi"
    start = time.time()
    key_name = "Parallel-"+lang
    wait = WebDriverWait(dri,200)
    rid = url.split('=')[1]
    english_rid = rid
    path = os.path.join(os.getcwd(),year,month,date)
    filepath = os.path.join(year,month,date)
    Path(path).mkdir(parents=True,exist_ok=True)
    list_rid.append(rid)
    dri.get(url)
    wait.until(presence_of_element_located((By.CLASS_NAME,"container")))
    dri.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    dri.execute_script("for(var i = 0;i<document.getElementsByClassName('addthis-smartlayers').length;i++){document.getElementsByClassName('addthis-smartlayers')[i].style.display = 'none'}")
    page_source = dri.page_source
    if(len(dri.find_elements_by_class_name("ReleaseLang")) == 0):
        return list_rid,memo
    english_text = write_text(page_source)
    f1 = open(path+rid+"-English.txt",'w',encoding='utf-16')
    for t in english_text:
        f1.write(t+"\n")
    f1.close()
    try:
        release_lang = dri.find_elements_by_class_name("ReleaseLang")[0]
    except:
        return list_rid,memo
    a_tags = release_lang.find_elements_by_tag_name("a")
    for i,a in enumerate(a_tags):
        if(a.text == lang):
            url = a.get_attribute("href")
            r = requests.get(url)
            lang_text = write_text(r.text)
            lang_rid = url.split("=")[1]
            list_rid.append(lang_rid)
            with open(os.path.join(path,lang_rid+"-"+lang+".txt"),'w',encoding="utf-16") as f2:
                for t in lang_text:
                    f2.write(t+"\n")
            curr_list = [os.path.join(filepath,english_rid+"-English.txt"),os.path.join(filepath,lang_rid+"-"+text_name+".txt")]
            if(memo.get(key_name) is not None):
                memo[key_name].append(curr_list)
            else:
                memo[key_name] = []
                memo[key_name].append(curr_list)
            break
    return list_rid,memo
    start = time.time()
    english_rid = ''
    hindi_rid = ''
    text_name = None
    wait = WebDriverWait(dri,200)
    rid = url.split("=")[1]
    path = os.getcwd()+"\\"+year+"\\"+month+"\\"+date+"\\"
    filepath = year+"\\"+month+"\\"+date+"\\"
    Path(path).mkdir(parents=True,exist_ok=True)
    # print('Handling language English')
    # get_text(rid,'English',path)
    english_rid = rid
    list_rid.append(english_rid)
    r = requests.get(url,timeout=100)
    soup = BeautifulSoup(r.text,"html.parser")
    release_lang = soup.find("div",attrs={"class":"ReleaseLang"})
    if(release_lang is None):
        return list_rid,memo

def select_value(wait,select,value):
    select.select_by_visible_text(value)
    wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
    print("Finished selecting",value)


def populate_data(driver,dri,day,month,year,path_parallel_csv):
    start = time.time()
    query_url = "https://www.pib.gov.in/allRel.aspx"
    print("Finished initalize")
    memo = {}
    list_rid=[]
    wait = WebDriverWait(driver,200)
    driver.get(query_url)
    wait.until(presence_of_element_located((By.CLASS_NAME,"content-area")))
    print("Finished loading")
    select_day = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlday")[0])
    if(day != select_day.first_selected_option.text):
        select_value(wait,select_day,day)
    select_day = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlday")[0])
    if(select_day.first_selected_option.text != day):
        return 'Stop'
    select_year = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlYear")[0])
    if(year!= select_year.first_selected_option.text):
        select_value(wait,select_year,year)
    select_year = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlYear")[0])
    if(select_year.first_selected_option.text != year):
        return 'Stop'
    select_month = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlMonth")[0])
    if(month != select_month.first_selected_option.text):
        select_value(wait,select_month,month)
    select_month = Select(driver.find_elements_by_id("ContentPlaceHolder1_ddlMonth")[0])
    if(select_month.first_selected_option.text != month):
        return 'Stop'
    div = driver.find_elements_by_class_name("content-area")[0]
    div_search = driver.find_elements_by_class_name("search_box_result")[0].text
    print(div_search)
    num = div_search.split(' ')[1]
    num = int(num)
    print(num)
    for i in range(1,num+1):
        try:
            ul = div.find_elements_by_xpath('//*[@id="form1"]/section[2]/div/div[7]/div/div/ul['+str(i)+']')[0]
            li = ul.find_elements_by_tag_name("li")[0]
            ul_leftul = li.find_elements_by_tag_name("ul")[0]
            lis = ul_leftul.find_elements_by_tag_name("li")
            for li_one in lis:
                # li_one = driver.find_elements_by_xpath('//*[@id="form1"]/section[2]/div/div[7]/div/div/ul[3]/li/ul/li[3]')[0]
                a = li_one.find_elements_by_tag_name("a")[0]
                print(a.text)
                print(a.get_attribute("href"))
                list_rid,memo = get_prid2(day,month,year,a.get_attribute("href"),dri,list_rid,memo)
        except IndexError as e:
            print('Here inside populate_data')
            print(e)
            break
    print(len(list_rid))
    for key in memo:
        csv_list = memo[key]
        lang = key.split('-')[1]
        header = ['English_Filename',lang+'_Filename']
        df = pd.DataFrame(csv_list)
        filename = month+"-"+year+"-"+key+".csv"
        if(not os.path.exists(filename)):
            df.to_csv(path_parallel_csv+month+"-"+key+".csv",index=False,header=header,mode='a')
        else:
            df.to_csv(path_parallel_csv+month+"-"+key+".csv",index=False,header=False,mode='a')
    f1 = open(path_parallel_csv+month+'-Rid.txt','w')
    for r in list_rid:
        f1.write(r+"|")
    end = time.time()
    print("total time taken ",end-start)

if __name__ == "__main__":
    driver = get_driver()
    dri = get_driver()
    # populate_data(driver,dri,'All','February','2020')
    populate_data(driver,dri,'All','December','2019')
    winsound.Beep(2500,100)
    # populate_data(driver,dri,'All','February','2020')
