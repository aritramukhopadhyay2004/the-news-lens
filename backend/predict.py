import joblib
import math
import re

model = joblib.load('./model/fake_news_model.pkl')
vectorizer = joblib.load('./model/vectorizer.pkl')


def _sigmoid(x: float) -> float:
    """Convert a raw classifier score into a probability-like value."""
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0


def predict_fake_news(text):
    # Clean text
    text = re.sub(r'\W', ' ', str(text))
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = text.lower()

    # Predict
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]

    # PassiveAggressiveClassifier doesn't support predict_proba.
    # Use the decision function and a sigmoid to create a confidence score.
    try:
        raw_score = model.decision_function(vec)[0]
        confidence = _sigmoid(raw_score)
    except Exception:
        confidence = 0.5

    return prediction, confidence

if __name__ == '__main__':
    text = input('Enter news text: ')
    pred, conf = predict_fake_news(text)
    print(f'Prediction: {pred} (confidence: {conf:.2f})')
