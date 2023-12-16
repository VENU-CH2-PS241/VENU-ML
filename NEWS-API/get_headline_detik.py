import pandas as pd
import re

from datetime import date
from bs4 import BeautifulSoup
from requests import get

def get_headline_detik():
    url = 'https://www.detik.com/'
    datas = get(url)
    soup = BeautifulSoup(datas.text, 'html.parser')
    tag = soup.find_all("article")
    sumber = 'detikNews'
    # print(tag)
    data = {
        'title' : [],
        'link' : [],
        # 'image' : [],
        # 'source' : []
    }
    for no in range(len(tag)):
        try:
            data['title'].append(tag[no].find('div', class_ = re.compile('media .*')).find('div', class_ = re.compile('media__text.*')).find(['h2', 'h3']).get_text().strip())
            data['link'].append(tag[no].find('div', class_ = re.compile('media .*')).find('div', class_ = re.compile('media__text.*')).find(['h2', 'h3']).find('a')['href'])
        except:
            pass

    # data = pd.DataFrame(data)
    print(data, len(data))
    # return data

get_headline_detik()
