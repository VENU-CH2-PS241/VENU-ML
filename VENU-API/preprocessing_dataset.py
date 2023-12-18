import re
import string

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

def preprocess_text(text):
    stop_factory = StopWordRemoverFactory()
    stopword = stop_factory.create_stop_word_remover()
    text = re.sub(r'http\S+', '', text.lower())
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans("","",string.punctuation))
    text = stopword.remove(text)
    return text