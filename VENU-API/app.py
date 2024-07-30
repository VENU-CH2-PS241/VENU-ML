import pandas as pd
import json
import os
import numpy as np

from flask import Flask, request, jsonify, render_template
from datetime import date

from news_api.get_content_detik import scrap_detik
from news_api.get_headline_detik import get_headline_detik
from news_api.get_content_cnn import scrap_cnn
from news_api.get_headline_cnn import get_headline_cnn
from news_api.get_content_kapanlagi import scrap_kapanlagi
from news_api.get_headline_kapanlagi import get_headline_kapanlagi
from news_api.get_content_liputan6 import scrap_liputan6
from news_api.get_headline_liputan import get_headline_liputan6

from predict_syscom import system_predict

from predict_hoax_lstm import Predict_lstm

app = Flask(__name__)

current_dir = os.path.abspath(__file__)  
parent_dir = os.path.dirname(os.path.dirname(current_dir))  
target_dir = os.path.join(parent_dir, 'VENU-API', 'model')


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api/scrap", methods=['GET'])
def scrap():
    headline_cnn = get_headline_cnn()
    # headline_detik = get_headline_detik()
    headline_kapanlagi = get_headline_kapanlagi()
    headline_liputan6 = get_headline_liputan6()

    content_cnn = scrap_cnn(headline_cnn)
    # content_detik = scrap_detik(headline_detik)
    content_kapanlagi = scrap_kapanlagi(headline_kapanlagi)
    content_liputan6 = scrap_liputan6(headline_liputan6)

    df = pd.concat([content_cnn, content_kapanlagi, content_liputan6])

    # predictor = Predict_lstm(df, model_path=target_dir)
    # prediction_result = predictor.predict()

    # print(np.squeeze(prediction_result['probability']))
    # df['prediction'] = np.squeeze(prediction_result['probability'])

    # df.to_json('datasets/content_{}.json'.format(str(date.today())), orient='records', lines=True)

    return json.dumps(json.loads(df.to_json(orient="records")))

@app.route("/api/v1/predict/hoax", methods=['POST'])
def predict_text():
    if request.method == 'POST':        
        file = request.get_json()
        text = file['text']
        
        predictor = Predict_lstm(text, model_path=target_dir)
        prediction_result = predictor.predict()

        response = {
            'message': 'File successfully received and processed',
            'probability': prediction_result['probability'],
        }
        return jsonify(**response), 200
    
@app.route("/api/v1/predict/syscom", methods=['POST'])
def predict_syscomt():
    if request.method == 'POST':        
        file = request.get_json()
        text = file['text']
        
        predictor = system_predict(text)
        prediction_result = predictor.predict()

        response = {
            'message': 'File successfully received and processed',
            'indices': prediction_result['indices'],
        }
        return jsonify(**response), 200

def allowed_file(filename):
    return type(filename) == str
    

if __name__ == '__main__':
    app.run()