import pandas as pd
import os   
import re

from datetime import date
from bs4 import BeautifulSoup
from requests import get

source = 'liputan6'

def scrap_liputan6(headline_data):
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
            # url = 'https://www.liputan6.com/bisnis/read/5481172/pns-tak-netral-di-pemilu-2024-terancam-dipecat-hingga-pidana'
            datas = get(url)
            soup = BeautifulSoup(datas.text, 'html.parser')
            parent_tag = soup.find('div', class_ = 'article-content-body__item-content')

            tag = parent_tag.find_all("p")
            paragraphs = [re.sub('\xa0', ' ', i.get_text().strip()) for i in tag]
            paragraphs = re.sub('Liputan6.com, ', ' ', ' '.join(paragraphs)).strip()
            jenis = url.split('/')[3]
            tanggal = soup.find('time').get_text()
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
# scrap_liputan6()

