import tensorflow as tf
import time
import pickle
import re
import string
import joblib

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class Predict_lstm:
    def __init__(self, text, model_path):
        self.text = text
        self.model_path = model_path

    def load_model(self):
        model = joblib.load(self.model_path)
        return model
    
    def preprocess_text(self):
        stop_factory = StopWordRemoverFactory()
        stopword = stop_factory.create_stop_word_remover()
        Fact = StemmerFactory()
        stemmer = Fact.create_stemmer()
        text = self.text
        text = re.sub(r'http\S+', '', text.lower())
        text = re.sub(r'\d+', '', text)
        text = text.translate(str.maketrans("","",string.punctuation))
        text = stemmer.stem(text)
        text = stopword.remove(text)
        return text
    
    def tokenizer(self):
        start_time = time.time()
        with open('model/tokenizer/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        text = self.preprocess_text()
        tokenized_text = tokenizer.texts_to_sequences([text])
        maxlen=500
        tokenized_text = pad_sequences(tokenized_text, maxlen=maxlen)
        end_time = time.time()
        execution_time = end_time - start_time
        return [tokenized_text, execution_time]

    def predict(self):
        start_time = time.time()
        model = self.load_model()
        tokenizing = self.tokenizer()
        tokenized_text = tokenizing[0]
        exec_time_preprocess = tokenizing[1]
        probability = model.predict(tokenized_text)
        # probability = predictions._numpy()[0][0]
        end_time = time.time()
        execution_time_model = end_time - start_time
        result = {
            'probability': float(probability[0][0]),
            'exec_time_model' : execution_time_model,
            'exec_time_preprocess' : exec_time_preprocess
        }
        return result