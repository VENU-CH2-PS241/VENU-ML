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
    source = 'detikNews'
    data = {
        'title' : [],
        'link' : [],
        'image' : [],
        'source' : []
    }
    for no in range(len(tag)):
        try:
            media = tag[no].find('div', class_ = re.compile('media .*'))
            media_text = media.find('div', class_ = re.compile('media__text.*'))
            media_image = media.find('div', class_ = re.compile('media__image.*'))
            title = media_text.find(['h2', 'h3']).get_text().strip()
            link = media_text.find(['h2', 'h3']).find('a')['href']
            image = media_image.find('a').find('span').find('img')['src'].strip()

            data['title'].append(title)
            data['link'].append(link)
            data['image'].append(image)
            data['source'].append(source)
        except:
            pass

    data = pd.DataFrame(data)
    # print(data, len(data['link']))
    return data

get_headline_detik()
