import tensorflow as tf
import time

from transformers import BertTokenizer

class Predict:
    def __init__(self, text, model_path):
        self.text = text
        self.model_path = model_path

    def load_model(self):
        model = tf.saved_model.load(self.model_path)
        return model
    
    def preprocess_text(self):
        start_time = time.time()
        tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-lite-base-p1', use_fast=True)
        tokenized_text = tokenizer(
            text=self.text,
            add_special_tokens=True,
            max_length=70,
            truncation=True,
            padding='max_length',
            return_tensors='tf',
            return_token_type_ids=False,
            return_attention_mask=True,
        )
        end_time = time.time()
        execution_time = end_time - start_time
        return [tokenized_text, execution_time]

    def predict(self):
        start_time = time.time()
        model = self.load_model()
        preprocessed_text = self.preprocess_text()
        tokenized_text = preprocessed_text[0]
        exec_time_preprocess = preprocessed_text[1]
        predictions = model([tokenized_text['input_ids'], tokenized_text['attention_mask']])
        probability = predictions._numpy()[0][0]
        end_time = time.time()
        execution_time_model = end_time - start_time
        result = {
            'probability': float(probability),
            'exec_time_model' : execution_time_model,
            'exec_time_preprocess' : exec_time_preprocess
        }
        return result