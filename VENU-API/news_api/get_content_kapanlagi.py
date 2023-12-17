import pandas as pd
import os   
import re

from datetime import date
from bs4 import BeautifulSoup
from requests import get

def scrap_kapanlagi(headline_data):
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
            datas = get(url)
            soup = BeautifulSoup(datas.text, 'html.parser')
            parent_tag = soup.find('div', class_ = 'body-paragraph clearfix mainpart trial-html')

            tag = parent_tag.find_all("p")
            paragraphs = [re.sub('\xa0', ' ', i.get_text().strip()) for i in tag]
            paragraphs = re.sub('Kapanlagi.com - ', ' ', ' '.join(paragraphs)).strip()
            if paragraphs.find('Baca Ini Juga Yuk KLovers!') or paragraphs.find('Baca Artikel Lainnya'):
                try:
                    paragraphs = paragraphs.split('Baca Ini Juga Yuk KLovers!')[0]
                except:
                    paragraphs = paragraphs.split('Baca Artikel Lainnya')[0]

            jenis = url.split('/')[4]
            tanggal = soup.find('div', class_='klTop-post').find('p').find('time').get_text().split('\n')[2]
            tmp += 1

            dataset['berita'].append(paragraphs)
            dataset['tanggal'].append(tanggal)
            dataset['jenis'].append(jenis)
            dataset['title'].append(data.title)
            dataset['source'].append(data.source)
            dataset['link'].append(data.link)
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
# scrap_kapanlagi()

