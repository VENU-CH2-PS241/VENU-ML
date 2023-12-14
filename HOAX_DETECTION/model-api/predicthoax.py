import numpy as np
import tensorflow as tf

from transformers import BertTokenizer

class Predict:
    def __init__(self, text, model_path):
        self.text = text
        self.model_path = model_path

    def load_model(self):
        model = tf.saved_model.load(self.model_path)
        return model
    
    def preprocess_text(self):
        tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-lite-base-p1')
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
        return tokenized_text

    def predict(self):
        model = self.load_model()
        tokenized_text = self.preprocess_text()
        predictions = model(tokenized_text)
        predicted_class = np.argmax(predictions)  
        probability = predictions[0][predicted_class]
        result = {
            'predicted_class': float(predicted_class),
            'probability': float(probability)
        }
        return result