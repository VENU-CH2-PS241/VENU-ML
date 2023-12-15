from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
from predicthoax import Predict
from predict_hoax_lstm import Predict_lstm

import os


app = Flask(__name__)

current_dir = os.path.abspath(__file__)  
parent_dir = os.path.dirname(os.path.dirname(current_dir))  
# target_dir = os.path.join(parent_dir, "Chotracker-CC-ModelAPI/model")
target_dir = os.path.join(parent_dir, 'model-api', 'model')

# Model path
model_path_hoax = os.path.join(target_dir, "1") 
# model_path_cnn = os.path.join(target_dir, "model_weights.h5")  # Size model Besar, Download model di trello

# @app.route("/api/v1/predict/chobot", methods=['POST'])
# def predict_chatbot():
#     if request.method == 'POST':
#         if 'text' not in request.json:
#             return jsonify({'message': 'Text input not provided'}), 400
#         text = request.json['text']
#         response = predict_intent(text)
#         return jsonify({'message': response}), 200

# @app.route("/api/v1/predict/regression", methods=['POST'])
# def predict_regression_image():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return jsonify({'message': 'There is no file sended'}), 400

#         file = request.files['file']

#         if not allowed_file(file.filename):
#             return jsonify({'message': 'File is not image'}), 400

#         image = Image.open(file.stream)

#         predictor = RegressionPredictor(model_path_regression)
#         prediction_result = predictor.predict(image)
#         rounded_value = "{:.2f}".format(prediction_result)
#         response = {
#             'message': 'File successfully received and processed',
#             'prediction': rounded_value
#         }
#         return jsonify(response), 200

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api/v1/predict/hoax", methods=['POST'])
def predict_text():
    if request.method == 'POST':
        # if 'file' not in request.files:
        #     # return jsonify({'message': 'There is no file sended'}), 400
        #     return request
        
        file = request.form['file']

        # if not allowed_file(file.filename):
        #     return jsonify({'message': 'File is not image'}), 400

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
        # return render_template('test_hoax.html', result=prediction_result)

def allowed_file(filename):
    return type(filename) == str

if __name__ == '__main__':
    app.run()