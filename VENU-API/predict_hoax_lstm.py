import pickle
import re
import string
import joblib
import os
import tensorflow as tf

from tensorflow.keras.preprocessing.sequence import pad_sequences
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class Predict_lstm:
    def __init__(self, text, model_path):
        self.text = text
        self.model_path = model_path

    def load_model(self):
        model = tf.keras.models.load_model(os.path.join(self.model_path, 'model_lstm.h5'))
        return model
    
    def preprocess_text(self):
        stop_factory = StopWordRemoverFactory()
        stopword = stop_factory.create_stop_word_remover()
        Fact = StemmerFactory()
        stemmer = Fact.create_stemmer()
        if type(self.text) == str:
            text = self.text
            text = re.sub(r'http\S+', '', text.lower())
            text = re.sub(r'\d+', '', text)
            text = text.translate(str.maketrans("","",string.punctuation))
            text = stemmer.stem(text)
            text = stopword.remove(text)
            text = [text]
        else:
            text = self.text['berita']
            text = text.apply(lambda x : re.sub(r'http\S+', '', x.lower()))
            text = text.apply(lambda x : re.sub(r'\d+', '', x))
            text = text.apply(lambda x : x.translate(str.maketrans("","",string.punctuation)))
            text = text.apply(lambda x : stemmer.stem(x))
            text = text.apply(lambda x : stopword.remove(x))
        return text
    
    def tokenizer(self):
        with open(os.path.join(self.model_path, 'tokenizer/tokenizer.pickle'), 'rb') as handle:
            tokenizer = pickle.load(handle)
        text = self.preprocess_text()
        tokenized_text = tokenizer.texts_to_sequences(text)
        maxlen=500
        tokenized_text = pad_sequences(tokenized_text, maxlen=maxlen)
        return tokenized_text

    def predict(self):
        model = self.load_model()
        tokenizing = self.tokenizer()
        tokenized_text = tokenizing
        probability = model.predict(tokenized_text)
        result = {
            'probability': probability.astype('float'),
        }
        return result