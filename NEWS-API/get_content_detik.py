import pandas as pd
import os   
import re

from datetime import date
from bs4 import BeautifulSoup
from requests import get

# headline_data = os.listdir('headline-detik')

def scrap_detik(headline_data):
    df = pd.concat([pd.read_csv(os.path.join('headline', data)).drop(columns=['Unnamed: 0']) for data in headline_data], ignore_index = True)
    df = df[df.link.isna().apply(lambda x : not x)].reset_index()

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
        try:
            data = df.iloc[i]
            url = data.link 
            datas = get(url)
            soup = BeautifulSoup(datas.text, 'html.parser')
            tag = soup.find_all("p")
            paragraphs = [i.get_text().strip() for i in tag]
            paragraphs = re.sub('ADVERTISEMENT SCROLL TO CONTINUE WITH CONTENT', ' ', ' '.join(paragraphs)).strip()
            image = soup.find('div', class_ = 'detail__media').find('img')['src']
            header = soup.find('article').find('div' , class_ = 'detail__header')
            tanggal = header.find('div', class_ = 'detail__date').get_text()
            tmp += 1
        except Exception as e:
            continue

        title = data.title
        source = 'detiknews'
        jenis = data.link.split('/')[3]

        dataset['berita'].append(paragraphs)
        dataset['image'].append(image)
        dataset['title'].append(title)
        dataset['tanggal'].append(tanggal)
        dataset['source'].append(source)
        dataset['jenis'].append(jenis)

        if tmp == 10:
            break

    # print(dataset)

    df_content = pd.DataFrame(dataset)
    df_content.to_csv('content/detik_content_{}.csv'.format(str(date.today())), index = False)
