import numpy as np
import tensorflow as tf

from transformers import BertTokenizer

model_path = 'model/1'

model = tf.saved_model.load(model_path)

text = 'test dulu'

tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-lite-base-p1')
tokenized_text = tokenizer(
    text=text,
    add_special_tokens=True,
    max_length=70,
    truncation=True,
    padding='max_length',
    return_tensors='tf',
    return_token_type_ids=False,
    return_attention_mask=True,
)

predict = model([tf.TensorSpec.from_tensor( X_test['input_ids'][:3], name = 'input_ids'), tf.TensorSpec.from_tensor( X_test['attention_mask'][:3], name = 'attention_mask')])