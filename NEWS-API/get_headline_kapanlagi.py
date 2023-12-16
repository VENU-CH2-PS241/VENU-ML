import pandas as pd
from datetime import date

from bs4 import BeautifulSoup
from requests import get

def get_headline_kapanlagi():
    url = 'https://www.kapanlagi.com/'

    today = date.today()
    datas = get(url)
    soup = BeautifulSoup(datas.text, 'html.parser')
    parent_tag = soup.find('ul', class_ = 'list-berita-kl clearfix')
    tag = parent_tag.find_all("li")
    # print(tag, len(tag))
    source = 'kapanlagi'
    data = {
        'title' : [],
        'link' : [],
        'image' : [],
        'source' : [],
    }

    for i in tag:
        i = i.find('div')
        try:
            link = i.find('a')['href'].strip()
            image = i.find('a').find('img')['src'].strip()
            title = i.find("div", class_ = 'deskrip-berita').find('p').find('a').text.strip()
            # tipe = i.find('span', attrs={'class':'kanal'}).text
            # waktu = i.find('span', attrs={'class':'date'}).text
            data['title'].append(title)
            data['link'].append(link)
            data['image'].append(image)
            data['source'].append(source)
        except:
            pass

    data = pd.DataFrame(data)
    # print(data.head(), len(data))
    # print(data.link[0])
    # data.to_csv('headline\{}_headline_{}.csv'.format(source, str(today)))
    return data
