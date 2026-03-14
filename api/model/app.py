import os

from flask import Flask, request, jsonify, send_from_directory
from predict import predict_fake_news
from url_extractor import extract_article

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def frontend_static(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data['text']
    prediction, confidence = predict_fake_news(text)
    return jsonify({
        'prediction': prediction,
        'confidence': float(confidence)
    })

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/predict_url", methods=["POST"])
def predict_url():

    data = request.get_json()
    url = data["url"]

    article_text = extract_article(url)

    if not article_text:
        return jsonify({"error": "Could not extract article"})

    prediction, confidence = predict_news(article_text)

    return jsonify({
        "prediction": prediction,
        "confidence": round(confidence * 100, 2)
    })
