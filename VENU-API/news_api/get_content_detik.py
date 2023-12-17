import pandas as pd
import os   
import re

from datetime import date
from bs4 import BeautifulSoup
from requests import get

def scrap_detik(headline_data):
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
            url = 'https://health.detik.com/true-story/d-7093479/viral-kabar-pakai-masker-wajib-lagi-saat-kasus-covid-naik-ini-klarifikasi-kemenkes'
            datas = get(url)
            soup = BeautifulSoup(datas.text, 'html.parser')
            tag = soup.find('article')
            text = tag.find_all('p')

            paragraphs = [i.get_text().strip() for i in text]
            paragraphs = re.sub('ADVERTISEMENT SCROLL TO CONTINUE WITH CONTENT', ' ', ' '.join(paragraphs)).strip()
            tanggal = tag.find('div', class_ = 'detail__date').get_text()
            tmp += 1
            jenis = data.link.split('/')[3]

            dataset['berita'].append(paragraphs)
            dataset['tanggal'].append(tanggal)
            dataset['jenis'].append(jenis)
            dataset['link'].append(data.link)
            dataset['image'].append(data.image)
            dataset['title'].append(data.title)
            dataset['source'].append(data.source)

        except Exception as e:
            print(e)
            continue

        if tmp == 10:
            break

    df_content = pd.DataFrame(dataset)
    # print(df_content)
    # df_content.to_csv('content/detik_content_{}.csv'.format(str(date.today())), index = False)
    return df_content
