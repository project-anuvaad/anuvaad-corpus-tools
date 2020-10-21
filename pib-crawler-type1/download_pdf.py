from selenium import webdriver
import pandas as pd
import os 
from pathlib import Path
import shutil


def download(driver, target_path):
    def execute(script, args):
        driver.execute('executePhantomScript',
                       {'script': script, 'args': args})
    driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
    page_format = 'this.paperSize = {format: "A4", orientation: "portrait" };'
    driver.execute('executePhantomScript',{'script':page_format,'args':[]})
    render = '''this.render("{}")'''.format(target_path)
    driver.execute('executePhantomScript',{'script':render,'args':[]})


def download_util(prid,file_name):
    print(file_name)
    name = os.path.basename(file_name)
    driver.get('https://www.pib.gov.in/PressReleasePage.aspx?PRID='+prid)
    driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
    page_format = 'this.paperSize = {format: "A4", orientation: "portrait" };'
    driver.execute('executePhantomScript',{'script':page_format,'args':[]})
    render = '''this.render("{}")'''.format(name)
    driver.execute('executePhantomScript',{'script':render,'args':[]})
    shutil.move(name,file_name)


if __name__ == '__main__':
    month = 'January'
    year = '2019'
    driver = webdriver.PhantomJS('C:\\Program Files\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    base_path = 'C:\\Users\\Dhanvi\\PIB_Scraping-3'
    parallel_file = os.path.join(base_path,year,month,'Parallel-Hindi.csv')
    pdf_path = os.path.join(base_path,year,month,'PDF')
    Path(pdf_path).mkdir(parents=True,exist_ok=True)
    df = pd.read_csv(parallel_file)
    for i in range(len(df)):
        en_file_name = df['English_Filename'][i]
        hi_file_name = df['Hindi_Filename'][i]
        rid = en_file_name.split('\\')[-1].split('-')[0]
        hrid = hi_file_name.split('\\')[-1].split('-')[0]
        download_util(rid,os.path.join(pdf_path,en_file_name.split('\\')[-1].split('.')[0]+".pdf"))
        download_util(hrid,os.path.join(pdf_path,hi_file_name.split('\\')[-1].split('.')[0]+".pdf"))
