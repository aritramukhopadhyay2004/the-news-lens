import requests

news = "Aliens secretly control the government"

response = requests.post(
    "http://127.0.0.1:5000/predict",
json={"text": news}
)

print(response.json())