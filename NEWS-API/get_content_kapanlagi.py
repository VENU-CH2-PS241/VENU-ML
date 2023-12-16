import pandas as pd
import os   
import re

from datetime import date
from bs4 import BeautifulSoup
from requests import get

source = 'kapanlagi'

def scrap_kapanlagi(headline_data):
    df = pd.concat([pd.read_csv(os.path.join('headline', data)).drop(columns=['Unnamed: 0']) for data in headline_data], ignore_index = True)

    dataset = {
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
            # url = 'https://www.kapanlagi.com/showbiz/selebriti/penyanyi-danilla-riyadi-ungkap-pernah-menjadi-korban-pelecehan-di-rumahnya-sendiri-berat-banget-f3a8ec.html?page=3'
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
            # print(paragraphs)

            jenis = url.split('/')[4]
            tanggal = soup.find('div', class_='klTop-post').find('p').find('time').get_text().split('\n')[2]
            title = data.title
            image = data.image
            tmp += 1
        except:
            continue

        dataset['berita'].append(paragraphs)
        dataset['title'].append(title)
        dataset['source'].append(source)
        dataset['tanggal'].append(tanggal)
        dataset['jenis'].append(jenis)
        dataset['image'].append(image)

        if tmp == 10:
            break
    # print(dataset)
    df_content = pd.DataFrame(dataset)
    df_content.to_csv('content/{}_content_{}.csv'.format(source, str(date.today())), index = False)

# print(dataset)
# scrap_kapanlagi()

