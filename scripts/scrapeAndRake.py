# WARNING, PLEASE READ
# This file is scraping an EXTERNAL website, ALWAYS check robots.txt
from time import sleep
import bz2
import os
import mechanicalsoup
import pandas as pd


    
def scrape(base_url, sub_url, identifierr, user_agent):
    browser = mechanicalsoup.StatefulBrowser(
        user_agent=user_agent,
        raise_on_404=True,
    )
    base = base_url
    browser.open(base)
    for link in browser.page.find_all("a", identifier):
        sub = link.get('href')
        ch = sub_url
        sub = ''.join(sub.split(ch,1))
        browser.download_link(link=link, file=sub)
        print(f'Downloading, {link}')
        sleep(1)

def rake():
    for x in os.listdir():
        if x.endswith(".bz2"):
            # Prints only text file present in My Folder
            zipfile = bz2.BZ2File(x) # open the file
            data = zipfile.read() # get the decompressed data
            newfilepath = x[:-4] # assuming the filepath ends with .bz2
            open(newfilepath, 'wb').write(data) # write a uncompressed file
    file_list = [f for f in os.listdir() if f.endswith('.csv')]
    append_list = []
    for file in sorted(file_list):
        append_list.append(pd.read_csv(file).assign(File_Name = os.path.basename(file)))
    csv_merged = pd.concat(append_list, ignore_index=True)
    csv_merged.to_csv('merged-data.csv')
    file_list = [f for f in os.listdir() if f.endswith('.csv') or f.endswith('.bz2')]
    for file in file_list:
        if file != 'merged-data.csv':
            os.remove(file)

if __name__ == '__main__':
    scrape("https://data.everef.net/market-history/2022/",
           '/market-history/2022/',
           "data-file-url",
           'EMP/0.4: https://github.com/Joe-TheBro/EVE-Market-Predictor')
    rake()