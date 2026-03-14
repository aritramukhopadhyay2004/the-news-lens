import json
import os
from newspaper import Article
import math
import re
import joblib
import os
from newspaper import Article

# Load models
model_path = os.path.join(os.path.dirname(__file__), 'model', 'fake_news_model.pkl')
vectorizer_path = os.path.join(os.path.dirname(__file__), 'model', 'vectorizer.pkl')
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def _sigmoid(x: float) -> float:
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

def predict_fake_news(text: str):
    text = re.sub(r'\W', ' ', str(text))
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = text.lower()
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    raw_score = model.decision_function(vec)[0]
    confidence = _sigmoid(raw_score)
    return prediction, confidence

def main(request):
    if request.method != 'POST':
        return {'statusCode': 405, 'body': 'Method not allowed'}

    try:
        body = json.loads(request.body)
        url = body.get('url')
        if not url:
            return {'statusCode': 400, 'body': json.dumps({'error': 'Missing "url" field'})}

        # Extract article
        article = Article(url)
        article.download()
        article.parse()
        text = article.title + " " + article.text
        if not text.strip():
            return {'statusCode': 400, 'body': json.dumps({'error': 'Could not extract article text'})}

        # Predict
        prediction, confidence = predict_fake_news(text)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'prediction': prediction,
                'confidence': round(float(confidence) * 100, 2)
            })
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

