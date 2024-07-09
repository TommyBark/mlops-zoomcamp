import requests

url = "http://127.0.0.1:9696/predict"

ride = {
    "PULocationID": "10",
    "DOLocationID": "50",
    "trip_distance": 50
}


response = requests.post(url, json=ride)

print(response.json())