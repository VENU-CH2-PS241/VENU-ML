import pandas as pd
from datetime import date

from bs4 import BeautifulSoup
from requests import get

def get_headline_liputan6():
    url = 'https://www.liputan6.com/'

    today = date.today()
    datas = get(url)
    soup = BeautifulSoup(datas.text, 'html.parser')
    # parent_tag = soup.find('ul', class_ = 'list-berita-kl clearfix')
    tag = soup.find_all("article")
    # print(tag, len(tag))
    source = 'liputan6'
    data = {
        'title' : [],
        'link' : [],
        'image' : [],
        'source' : [],
    }

    for i in tag[:15]:
        try:
            link = i.find('figure').find('a')['href'].strip()
            image = i.find('a').find('picture').find('img')['src'].strip()
            title = i.find("aside").find('header').find('h4').text.strip()
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
    data.to_csv('headline\{}_headline_{}.csv'.format(source, str(today)))
# get_headline_liputan6()
