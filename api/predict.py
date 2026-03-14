import json
import joblib
import math
import re
import os
from typing import Tuple

# Load models relative to api/
model_path = os.path.join(os.path.dirname(__file__), 'model', 'fake_news_model.pkl')
vectorizer_path = os.path.join(os.path.dirname(__file__), 'model', 'vectorizer.pkl')
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def _sigmoid(x: float) -> float:
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

def predict_fake_news(text: str) -> Tuple[str, float]:
    # Clean text
    text = re.sub(r'\W', ' ', str(text))
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = text.lower()

    # Vectorize & predict
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
        text = body.get('text')
        if not text:
            return {'statusCode': 400, 'body': json.dumps({'error': 'Missing "text" field'})}
        
        prediction, confidence = predict_fake_news(text)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'prediction': prediction,
                'confidence': float(confidence)
            })
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

