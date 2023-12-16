import pandas as pd
import os
import joblib
import time

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing_dataset import preprocess_text

def load_dataset(folder_url):
    try:
        data_processed = pd.read_excel(os.path.join(folder_url, 'cleaned_dataset.xlsx'))
    except:
        data_url = os.listdir(folder_url)
        all_data = [pd.read_excel(os.path.join(folder_url, url))[['cleaned']] for url in data_url]
        dataset = all_data[0]
        for i in all_data[1:-1]:
            pd.concat([dataset, i])
        dataset = dataset.rename(columns = {'cleaned' : 'berita'})
        data_processed = dataset['berita'].apply(lambda x : preprocess_text(x))
        data_processed.to_excel(os.path.join(folder_url, 'cleaned_dataset.xlsx'), index=False)
    return data_processed

# pwd in System Recommendation Folder
# Membaca dataset
DATASET_URL = 'datasets'
MODEL_URL = 'models'

data = load_dataset(DATASET_URL)

# Menghapus nilai NaN dan duplicates
data = data.dropna()
data = data.drop_duplicates()

# # Membagi dataset menjadi set pelatihan dan set uji (80-20 split)
X_train, X_test = train_test_split(data['berita'], test_size=0.05, random_state=42)

# # Melatih model TF-IDF pada set pelatihan
try:
    tfidf_vectorizer = joblib.load(os.path.join(MODEL_URL, 'vectorizer', 'tfidf_vectorizer.joblib'))
    tfidf_matrix_train = tfidf_vectorizer.transform(X_train)
except:
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(X_train)
    joblib.dump(tfidf_vectorizer, os.path.join(MODEL_URL, 'vectorizer', 'tfidf_vectorizer.joblib'))
    

# # Fungsi untuk merekomendasikan artikel
def recommend_articles(article_text, tfidf_vectorizer, tfidf_matrix_train, top_n=5):
    tfidf_matrix_test = tfidf_vectorizer.transform([article_text])
    cosine_similarities = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train).flatten()
    similar_articles_indices = cosine_similarities.argsort()[-top_n:][::-1]
    return similar_articles_indices, cosine_similarities[similar_articles_indices]

# # Menggunakan model pada beberapa sampel dari set uji untuk evaluasi
for article in X_test.sample(5).values:
    start_time = time.time()
    indices, scores = recommend_articles(article, tfidf_vectorizer, tfidf_matrix_train, top_n=5)
    end_time = time.time()
    execution_time_model = end_time - start_time
    print(f"Artikel Uji: {article[:100]}...")  # Menampilkan 100 karakter pertama
    print("Rekomendasi:")
    for idx, score in zip(indices, scores):
        print(f" - {X_train.iloc[idx][:100]}... Skor: {score:.4f}")
    print('Waktu eksekusi : {}'.format(execution_time_model))
    print("\n")

