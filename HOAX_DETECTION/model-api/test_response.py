import json
import requests

# Ton to be sent
datas = {'text' : 'var1'}

url = "http://127.0.0.1:5000/api/v1/predict/hoax"

r = requests.post(url, json=datas)
print(r)
print(json.dumps(datas))
print(str(r.content, 'utf-8'))