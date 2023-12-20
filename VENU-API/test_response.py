import json
import requests

from predict_hoax_lstm import Predict_lstm

# Ton to be sent
def get_response_scrap():
    url = "https://venu-project-408000.as.r.appspot.com/api/scrap"

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
    datas = {'text' : 'dsada asd'}

    url = "https://venu-project-408000.as.r.appspot.com/api/v1/predict/syscom"

    r = requests.post(url, json=datas)
    print(r)
    print(json.dumps(datas))
    print(str(r.content, 'utf-8'))

def test_infer():
    predictor = Predict_lstm('afsa', model_path='model')
    prediction_result = predictor.predict()

    print(prediction_result)

get_response_hoax()