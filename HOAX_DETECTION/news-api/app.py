from flask import Flask, request, jsonify, render_template
import numpy as np

import os

app = Flask(__name__)

current_dir = os.path.abspath(__file__)  
parent_dir = os.path.dirname(os.path.dirname(current_dir))  
target_dir = os.path.join(parent_dir, 'model-api', 'model')

# Model path
model_path_hoax = os.path.join(target_dir, "1") 

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api/v1/predict/hoax", methods=['POST'])
def predict_text():
    if request.method == 'POST':        
        file = request.form['file']
        text = str(file)
        
        predictor = Predict_lstm(text, model_path=model_path_hoax)
        prediction_result = predictor.predict()

        response = {
            'message': 'File successfully received and processed',
            'probability': prediction_result['probability'],
            'exec_time_model' : prediction_result['exec_time_model'],
            'exec_time_preprocess' : prediction_result['exec_time_preprocess']
        }
        return jsonify(**response), 200

def allowed_file(filename):
    return type(filename) == str

if __name__ == '__main__':
    app.run()