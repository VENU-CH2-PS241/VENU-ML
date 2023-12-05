# from crypt import methods
# import imp
# from pyexpat import features

import os
import numpy as np
import tensorflow as tf

from flask import Flask, request, jsonify, render_template
from transformers import TFAlbertModel
# import pickle

app = Flask(__name__)
# model = pickle.load(open("model_joblib.pkl", "rb"))
model = tf.keras.models.load_model('models/model_2023-11-29', custom_objects={"TFAlbertModel": TFAlbertModel})

@app.route("/")
def home():
    return render_template('index.html')

# @app.route("/predict", methods=["POST"])
# def predict():
#     float_features = [float(x) for x in request.form.values()]
#     features = [np.array(float_features)]
#     prediction = model.predict(features)
#     return render_template("index.html", prediction_text = "{}".format(prediction))

if __name__ == "__main__":
    app.run(debug=True)