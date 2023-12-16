import pandas as pd
from datetime import date

from bs4 import BeautifulSoup
from requests import get

def get_headline_cnn():
    url = 'https://www.cnnindonesia.com'

    today = date.today()
    datas = get(url)
    soup = BeautifulSoup(datas.text, 'html.parser')
    parent_tag = soup.find('div', class_="nhl-list")
    tag = parent_tag.find_all("article")
    sumber = 'CNNIndonesia'
    data = {
        'title' : [],
        'link' : [],
        'image' : [],
        'source' : []
    }

    for i in tag:
        try:
            title = i.find("h2").text.strip()
            link = i.find('a')['href'].strip()
            image = i.find('img')['src'].strip()
            # tipe = i.find('span', attrs={'class':'kanal'}).text
            # waktu = i.find('span', attrs={'class':'date'}).text
            data['title'].append(title)
            data['link'].append(link)
            data['image'].append(image)
            data['source'].append(sumber)
        except:
            pass

    data = pd.DataFrame(data)
    print(data.head, len(data))
    # data.to_csv('headline\{}_headline_{}.csv'.format(sumber, str(today)))

get_headline_cnn()

