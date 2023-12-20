import json
import requests
import pandas as pd
import numpy as np
import os

from predict_hoax_lstm import Predict_lstm

# Ton to be sent
def get_response_scrap():
    url = "http://127.0.0.1:5000/api/scrap"

    r = requests.get(url)
    print(r)
    print(str(r.content, 'utf-8'))

def get_response_hoax():
    datas = {'text' : 'var1'}

    url = "https://venu-project-408000.as.r.appspot.com/api/v1/predict/hoax"

    r = requests.post(url, json=datas)
    print(r)
    print(json.dumps(datas))
    print(str(r.content, 'utf-8'))

def get_response_syscom():
    datas = {
        'text' : 'dsada asd'
    }

    url = "https://venu-project-408000.as.r.appspot.com/api/v1/predict/syscom"

    r = requests.post(url, json=datas)
    print(r)
    print(json.dumps(datas))
    print(str(r.content, 'utf-8'))

def test_inference():
    datas = pd.DataFrame({'berita' : ['var1', 'safw asdkfwe', 'https://adsfwei sadkfwe', '23 asldfj s']})
    data_processed = pd.read_json(os.path.join('datasets', 'content_2023-12-17.json'), orient='records', lines=True)

    predictor = Predict_lstm(data_processed, 'model')
    prediction_result = predictor.predict()

    print(np.squeeze(prediction_result['probability']))

get_response_scrap()
# test_inference()
