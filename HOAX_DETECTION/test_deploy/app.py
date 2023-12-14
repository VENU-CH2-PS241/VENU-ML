# from crypt import methods
# import imp
# from pyexpat import features

import os
import numpy as np
import tensorflow as tf
import pandas as pd

from flask import Flask, request, jsonify, render_template
from transformers import TFAlbertModel, AutoTokenizer
# import pickle

app = Flask(__name__)
# model = pickle.load(open("model_joblib.pkl", "rb"))
model = tf.saved_model.load('model/model_2023-11-29')
test_twt = {
    'berita' : ["lewat di tl aku, dan aku kaget. Aku kira RS ini dibangunnya sama pemerintah kita ternyata pembangunannya dari uang donasi masyarakat kita toh aku nangis banget pas liat videonya juga", "Jog dalam kota kecepatan 80km/jam dan nerobos lampu merah. Dimf bawah ini juga ada cctv kalau ojol berhenti dipinggir anda tabrak, giliran diminta ganti rugi merasa diperas. Playing victim sekali ya wkwkwk", "Peta hubungan diplomatik Israel dengan negara-negara dunia. Hanya ada satu negara dengan perekonomian raksasa ber-GDP di atas $1 triliun yang belum pernah menjalin relasi sama Israel. Yep, Indonesia.", "Pernah penasaran ga sih kenapa Nabi & Rasul itu diutusnya di Arab, Jordan, & Mesir padahal dunia ini luas? Gambar ini sedikit banyak menjelaskan", "Ada perbedaan pada momen kelahiran anak kedua pasangan Atta Halilintar dan Aurel Hermansyah. Pasalnya, semua orangtua atau nenek dari Ameena dan putri keduanya turut hadir. Tentunya hal ini memberikan kebahagiaan bagi Atta dan Aurel. Apalagi mengingat saat momen Ameena lahir, tak seramai kelahiran anak keduanya ini. Saat ditemui di RSIA Bunda, Jakarta Pusat, Senin (13/11) Atta Halilintar merasa momen kelahiran adik Ameena seperti mimpi yang menjadi kenyataan baginya. “Ini udah kayak mimpi jadi nyata buat saya sama Aurel karena semua orangtua bisa hadir. Kemarin (anak pertama) lahiran kan pas Covid ya jadi nggak semua bisa hadir,” ungkap Atta Halilintar. 1. Didampingi Orang-Orang Tersayang Diketahui Dalam foto yang dibagikan di akun media sosial Atta Halilintar, ayah dan ibunya tampak hadir di rumah sakit. Begitu juga dengan orangtua Aurel, Anang Hermansyah dan Ashanty serta Krisdayanti yang tak ingin ketinggalan momen tersebut. Atta pun mengatakan, orangtua dan mertuanya hadir di rumah sakit menanti detik-detik kelahiran anak keduanya. Bahkan mereka juga rela berangkat dini hari ke rumah sakit. 2. Berkumpul Sejak Subuh “Semua mendoakan, semua lengkap semuanya udah ada dari pagi ngumpul di RSIA Bunda mengantar ke rumah sakit dari jam 03.00 WIB terus salat subuh bareng juga,” ujarnya. Ia menilai doa dari orangtuanya dan mertuanya menjadi kekuatan bagi Aurel Hermansyah. “Jadi menurutku doa dari semua jadi menguatkan juga ya. Semua sudah nggak sabar menyambut cucu keduanya,” tukasnya."] 
}

df = pd.DataFrame(test_twt)

max_len = 70
model_name = 'indobenchmark/indobert-base-p1'
tokenizer = AutoTokenizer.from_pretrained(model_name)



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict", methods=['GET', "POST"])
def predict():
    X_test = tokenizer(
        text=df['berita'].tolist(),
        add_special_tokens=True,
        max_length=max_len,
        truncation=True,
        padding=True,
        return_tensors='tf',
        return_token_type_ids=False,
        return_attention_mask=True,
        verbose=True
    )
    predicted = model.predict({'input_ids': X_test['input_ids'], 'attention_mask': X_test['attention_mask']})
    return "{}".format(predicted)

if __name__ == "__main__":
    app.run(debug=True)