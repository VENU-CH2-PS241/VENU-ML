from transformers import BertTokenizer, BertModel
import torch
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

# Memuat tokenizer dan model BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def extract_features(text):
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze()

# Membaca dan memproses dataset
file_path = 'Copy of all_cleaned.xlsx'  # Ganti dengan path file Anda
data = pd.read_excel(file_path)
data = data.dropna()

# Membagi dataset
X_train, X_test = train_test_split(data['berita'], test_size=0.2, random_state=42)

# Ekstraksi fitur BERT untuk set pelatihan
bert_features_train = [extract_features(text) for text in X_train]

# Fungsi rekomendasi menggunakan BERT
def recommend_articles_bert(article_text, bert_features_train, top_n=5):
    article_feature = extract_features(article_text)
    cosine_similarities = cosine_similarity(article_feature.reshape(1, -1), bert_features_train).flatten()
    similar_articles_indices = cosine_similarities.argsort()[-top_n:][::-1]
    return similar_articles_indices, cosine_similarities[similar_articles_indices]

# Menggunakan model pada beberapa sampel dari set uji
for article in X_test.sample(5).values:
    indices, scores = recommend_articles_bert(article, bert_features_train, top_n=5)
    print(f"Artikel Uji: {article[:100]}...")
    print("Rekomendasi:")
    for idx, score in zip(indices, scores):
        print(f" - {X_train.iloc[idx][:100]}... Skor: {score:.4f}")
    print("\n")