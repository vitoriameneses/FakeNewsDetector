import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from flask import Flask, request, jsonify
import nltk
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)

# Carregar o dataset
data = pd.read_csv('news.csv')
stop_words = set(stopwords.words('english'))
# Pré-processamento dos dados
#remoção de stopwords, pontuações e conversão para minúsculas

def preprocess_text(text):
    #Converter para minúsculas
    text = text.lower()
    # Remover pontuações
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenização
    tokens = word_tokenize(text)
    # Remover stopwords
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Reconstruir o texto após a remoção das stopwords
    text = ' '.join(filtered_tokens)
    return text
data['Texto'] = data['Texto'].str.lower()

# Features (X) e labels (y)
X = data['Texto']
y = data['Rótulo']

# Vetorização do texto usando TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_vectorized = vectorizer.fit_transform(X)

# Construção do modelo de árvore de decisão
model = DecisionTreeClassifier()
model.fit(X_vectorized, y)

@app.route('/detect', methods=['POST'])
def detect_fake_news():
    data = request.json
    text = data['text']
    # Pré-processar o texto de entrada
    text_preprocessed = preprocess_text(text)
    # Vetorizar o texto pré-processado
    text_vectorized = vectorizer.transform([text_preprocessed])
    # Fazer a previsão utilizando o modelo treinado
    prediction_prob = model.predict_proba(text_vectorized)
    # Extrair a probabilidade de ser fake news
    probability = prediction_prob[0][list(model.classes_).index('fake')]
    return jsonify({'probability': probability})
if __name__ == '__main__':
    app.run(debug=True)
