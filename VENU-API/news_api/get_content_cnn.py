import pandas as pd
import os   
import re

from datetime import date
from bs4 import BeautifulSoup
from requests import get

def scrap_cnn(headline_data):
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
        try:
            data = df.iloc[i]
            url = data.link 
            datas = get(url)
            soup = BeautifulSoup(datas.text, 'html.parser')

            tag = soup.find_all("p")
            paragraphs = [re.sub('\xa0', ' ', i.get_text().strip()) for i in tag]
            paragraphs = re.sub('ADVERTISEMENT SCROLL TO CONTINUE WITH CONTENT', ' ', ' '.join(paragraphs)).strip()

            tanggal = soup.find('div', class_='text-cnn_grey text-sm mb-4').get_text()
            jenis = data.link.split('/')[3]
            tmp += 1

            dataset['berita'].append(paragraphs)
            dataset['jenis'].append(jenis)
            dataset['tanggal'].append(tanggal)
            dataset['link'].append(data.link)
            dataset['title'].append(data.title)
            dataset['source'].append(data.source)
            dataset['image'].append(data.image)

        except:
            continue

        if tmp == 10:
            break

    df_content = pd.DataFrame(dataset)
    # df_content.to_csv('content/{}_content_{}.csv'.format(data.source, str(date.today())), index = False)
    return df_content


# print(dataset)

