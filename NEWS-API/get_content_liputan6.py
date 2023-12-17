import pandas as pd
import os   
import re

from datetime import date
from bs4 import BeautifulSoup
from requests import get

def scrap_liputan6(headline_data):
    df = headline_data

    dataset = {
        'link' : [],
        'berita' : [],
        'title' : [],
        'source' : [],
        'tanggal' : [], 
        'jenis' : [],
        'image' : []
    }

    length = len(df)
    tmp = 1
    for i in range(length):
        data = df.iloc[i]
        try:
            url = data.link 
            # url = 'https://www.liputan6.com/bisnis/read/5481172/pns-tak-netral-di-pemilu-2024-terancam-dipecat-hingga-pidana'
            datas = get(url)
            soup = BeautifulSoup(datas.text, 'html.parser')
            parent_tag = soup.find('div', class_ = 'article-content-body__item-content')

            tag = parent_tag.find_all("p")
            paragraphs = [re.sub('\xa0', ' ', i.get_text().strip()) for i in tag]
            paragraphs = re.sub('Liputan6.com, ', ' ', ' '.join(paragraphs)).strip()
            jenis = url.split('/')[3]
            tanggal = soup.find('time').get_text()
            tmp += 1

            dataset['berita'].append(paragraphs)
            dataset['tanggal'].append(tanggal)
            dataset['jenis'].append(jenis)
            dataset['link'].append(data.link)
            dataset['title'].append(data.title)
            dataset['source'].append(data.source)
            dataset['image'].append(data.image)
        except:
            continue

        
        if tmp == 10:
            break
    # print(dataset)
    df_content = pd.DataFrame(dataset)
    # df_content.to_csv('content/{}_content_{}.csv'.format(data.source, str(date.today())), index = False)
    return df_content


# print(dataset)
# scrap_liputan6()

