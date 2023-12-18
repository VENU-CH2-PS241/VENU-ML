import json
import requests

# Ton to be sent
def get_response_scrap():
    url = "http://127.0.0.1:5000/api/scrap"

    r = requests.get(url)
    print(r)
    print(str(r.content, 'utf-8'))

def get_response_hoax():
    datas = {'text' : 'var1'}

    url = "http://127.0.0.1:5000/api/v1/predict/hoax"

    r = requests.post(url, json=datas)
    print(r)
    print(json.dumps(datas))
    print(str(r.content, 'utf-8'))

def get_response_syscom():
    datas = {'text' : 'var1'}

    url = "http://127.0.0.1:5000/api/v1/predict/syscom"

    r = requests.post(url, json=datas)
    print(r)
    print(json.dumps(datas))
    print(str(r.content, 'utf-8'))

get_response_syscom()