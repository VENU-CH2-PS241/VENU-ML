import pandas as pd
import os   
import re

from datetime import date
from bs4 import BeautifulSoup
from requests import get

# headline_data = os.listdir('headline')
SOURCE = 'CNNIndonesia'

def scrap_cnn(headline_data):
    # print(headline_data)
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
        try:
            data = df.iloc[i]
            url = data.link 
            datas = get(url)
            soup = BeautifulSoup(datas.text, 'html.parser')

            tag = soup.find_all("p")
            paragraphs = [re.sub('\xa0', ' ', i.get_text().strip()) for i in tag]
            paragraphs = re.sub('ADVERTISEMENT SCROLL TO CONTINUE WITH CONTENT', ' ', ' '.join(paragraphs)).strip()

            tanggal = soup.find('div', class_='text-cnn_grey text-sm mb-4').get_text()
            title = data.title
            source = SOURCE
            jenis = data.link.split('/')[3]
            tmp += 1
        except:
            continue

        dataset['berita'].append(paragraphs)
        dataset['title'].append(title)
        dataset['source'].append(source)
        dataset['tanggal'].append(tanggal)
        dataset['jenis'].append(jenis)
        dataset['image'].append(data.image)

        if tmp == 10:
            break

    df_content = pd.DataFrame(dataset)
    df_content.to_csv('content/{}_content_{}.csv'.format(source, str(date.today())), index = False)

# print(dataset)

