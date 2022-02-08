# importing libraries
import os
import io
import time
import selenium
import requests
import urllib.request
from PIL import Image
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException


#Install Selenium Driver 
driver_sam = webdriver.Chrome(ChromeDriverManager().install())
search_url='https://samagra.kite.kerala.gov.in/#/textbook/page'
driver_sam.get(search_url)

#Select the available languages
medium=[]
lang = driver_sam.find_element_by_xpath('/html/body/app-root/app-textbook/div[2]/div[1]/div/form/div/div[1]/div/select')
med=lang.find_elements_by_tag_name('option')
for m in med:
    medium.append(m.text)

#Select the available standards
grade=[]
standard=driver_sam.find_element_by_xpath('/html/body/app-root/app-textbook/div[2]/div[1]/div/form/div/div[2]/div/select')
std = standard.find_elements_by_tag_name('option')
for s in std:
    grade.append(s.text)

#Select the available subjects
sub=[]
subject_name=driver_sam.find_element_by_xpath('/html/body/app-root/app-textbook/div[2]/div[1]/div/form/div/div[3]/div/select')
subu = subject_name.find_elements_by_tag_name('option')
value=subject_name.find_elements_by_name('value')
for i in value:
    sub.append(i.text)

# download the file url
def download_file(download_url,my_file, path):

    response = urllib.request.urlopen(download_url)    
    file = open(os.path.join(path,my_file), 'wb')
    file.write(response.read())
    file.close()

# Vids = WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'entry-thumbnails-link')))


# automate the page to page view and download the file
my_link=[]
path = '/home/test/Project_Anuvaad/samagra/'
driver_sam.implicitly_wait(10) # seconds

for i in tqdm(range(3, len(medium))):
    x = driver_sam.find_element_by_xpath('/html/body/app-root/app-textbook/div[2]/div[1]/div/form/div/div[1]/div/select')
    drop = Select(x)
    drop.select_by_index(i)
    m_path=path+medium[i]+'/'
    
    print(medium[i])
    for j in range(11,len(grade)):
        
        x = driver_sam.find_element_by_xpath('/html/body/app-root/app-textbook/div[2]/div[1]/div/form/div/div[2]/div/select')
        drop = Select(x)
        drop.select_by_index(j)
        g_path = m_path+str(j+1)
        
        subjects = []
        x = driver_sam.find_element_by_xpath('/html/body/app-root/app-textbook/div[2]/div[1]/div/form/div/div[3]/div/select')
        subject = x.find_elements_by_tag_name('option')
        print(grade[j])
        
        for sub in range(0,len(subject)):
#             print(len(subject[sub]))
            print(subject[sub].text)
            subjects.append(subject[sub].text)
            sub_path = driver_sam.find_element_by_xpath('/html/body/app-root/app-textbook/div[2]/div[1]/div/form/div/div[3]/div/select')
            drop = Select(sub_path)
            drop.select_by_index(sub)
            
            os.mkdir(os.path.join(g_path, subjects[sub]))
            sub_path = os.path.join(g_path,subjects[sub])+'/'
      
        

            contain=driver_sam.find_element_by_xpath('/html/body/app-root/app-textbook/div[2]/div[2]/div/div/div')
            get_link= contain.find_elements_by_tag_name('a')
            for z in get_link:
                hre=z.get_attribute('href')
                filename = hre.split('/')[-1:]

                download_file(hre,filename[0],sub_path)

            time.sleep(10)


