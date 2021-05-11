import requests
import time
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from requests.exceptions import MissingSchema

'''
    argv[1] --> output folder,
    argv[2] --> language (ex: Tamil),
    argv[3] --> section or topic (ex: sports/entertainment)
    '''
def main():
    out_folder = str(sys.argv[1])
    language = str(sys.argv[2])
    section = str(sys.argv[3])
    try:
        articles_data = pd.read_csv(f"{out_folder}/{language}_lokmat_{section}_updated.csv", encoding='utf-16')
    except:
        articles_data = pd.read_csv(f"{out_folder}/{language}_lokmat_{section}.csv", encoding='utf-16')
    filenames = articles_data['Headings']
    bad_chars = [';', ':', '!', '?', '|', '/', '"', '+', '<', '>', '.', "*"]
    #dates_list = []
    count = 0

    start_time = time.time()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

    for count, link in tqdm(enumerate(articles_data['Link']), total = articles_data.shape[0]):
        try:
            markup_string = requests.get(link, headers=headers, stream=True, allow_redirects=False).content
            soup = BeautifulSoup(markup_string, "html.parser")
            content = soup.findAll(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figcaption'])
        except MissingSchema:
            print("Missing shema for link :",link)
            sys.stdout.flush()
            content = []
        except AttributeError:
            print("NoneType object has no attribute text")
            sys.stdout.flush()
            content = []
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
    
        #date = soup.find('p', attrs={'class': 'storyby'})
        #dates_list.append(date.text.split('|')[-1])
        filename = ''.join(i for i in str(filenames[count]) if not i in bad_chars)
        out_dir = f"{out_folder}/{language}_articles_{section}"

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(os.path.join(out_dir, f"{count} {filename[:10]}.txt"), mode="w", encoding="utf-16") as file_w:
            for text in range(len(content)):
                file_w.write(content[text].text.strip() + "\r\n")
                
    #dates = pd.DataFrame({'Date': dates_list})        
    #dates.to_csv(f"{out_folder}/{language}_lokmat_{section}_date.csv", index=False)

    # print(' %s seconds ' % (time.time() - start_time))
if __name__ == "__main__":
    main()
