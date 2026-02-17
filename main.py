import requests
from fastapi import FastAPI

app = FastAPI()

API_KEY = "PASTE_YOUR_ALPHA_VANTAGE_KEY_HERE"

@app.get("/")
def root():
    return {"status": "India Stock API running"}

@app.get("/predict")
def predict(symbol: str):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "Time Series (Daily)" not in data:
        return {"error": "API limit reached or invalid symbol"}

    latest_day = list(data["Time Series (Daily)"].keys())[0]
    latest = data["Time Series (Daily)"][latest_day]

    open_price = float(latest["1. open"])
    close_price = float(latest["4. close"])

    return {
        "symbol": symbol,
        "date": latest_day,
        "open": open_price,
        "close": close_price,
        "prediction": "UP" if close_price > open_price else "DOWN"
    }
