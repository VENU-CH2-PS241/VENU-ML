import pandas as pd
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing_dataset import preprocess_text

DATASET_URL = 'datasets'
MODEL_URL = 'model'

class system_predict:
    def __init__(self, article):
        self.article = article

    def load_dataset(self, folder_url):
        try:
            data_processed = pd.read_json(folder_url, orient='records', lines=True)
            data_processed['berita'] = data_processed['berita'].apply(lambda x : preprocess_text(x))
        except Exception as e:
            return e
        return data_processed

    # pwd in System Recommendation Folder
    # Membaca dataset

    def train_model(self):
        data = self.load_dataset(os.path.join(DATASET_URL, 'content_2023-12-17.json'))

        # Menghapus nilai NaN dan duplicates
        data = data.dropna()
        data = data.drop_duplicates()

        # # Membagi dataset menjadi set pelatihan dan set uji (80-20 split)
        X_train = data['berita']

        # # Melatih model TF-IDF pada set pelatihan
        try:
            tfidf_vectorizer = joblib.load(os.path.join(MODEL_URL, 'vectorizer', 'tfidf_vectorizer.joblib'))
            tfidf_matrix_train = tfidf_vectorizer.transform(X_train)
        except:
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix_train = tfidf_vectorizer.fit_transform(X_train)
            joblib.dump(tfidf_vectorizer, os.path.join(MODEL_URL, 'vectorizer', 'tfidf_vectorizer.joblib'))
        
        return tfidf_vectorizer, tfidf_matrix_train
        

    # # Fungsi untuk merekomendasikan artikel
    def recommend_articles(self, tfidf_vectorizer, tfidf_matrix_train, top_n=5):
        tfidf_matrix_test = tfidf_vectorizer.transform([self.article])
        cosine_similarities = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train).flatten()
        similar_articles_indices = cosine_similarities.argsort()[-top_n:][::-1]
        return similar_articles_indices, cosine_similarities[similar_articles_indices]

    # # Menggunakan model pada beberapa sampel dari set uji untuk evaluasi
    def predict(self):
        tfidf_vectorizer, tfidf_matrix_train = self.train_model()
            
        indices, scores = self.recommend_articles(tfidf_vectorizer, tfidf_matrix_train, top_n=5)
        indices = indices.astype('int32')
        result = {
            'indices' : indices.tolist()
        }
        return result


