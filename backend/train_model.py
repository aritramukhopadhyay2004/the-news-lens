import pandas as pd
import joblib
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
nltk.download('stopwords', quiet=True)

# Load dataset
df = pd.read_csv('../dataset/news.csv')

X = df['text']
y = df['label']

# TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_vec = vectorizer.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Model
model = PassiveAggressiveClassifier(max_iter=100)
model.fit(X_train, y_train)

# Score
y_pred = model.predict(X_test)
print('Accuracy:', round(accuracy_score(y_test, y_pred), 3))

# Save
joblib.dump(model, './model/fake_news_model.pkl')
joblib.dump(vectorizer, './model/vectorizer.pkl')
print('✅ Models saved!')
