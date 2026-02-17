from fastapi import FastAPI, Query
import requests

app = FastAPI()

API_KEY = "3PPXJ0AQE10FJX74"

@app.get("/")
def root():
    return {"status": "India Stock API running"}

@app.get("/predict")
def predict(symbol: str = Query(...)):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }

    r = requests.get(url, params=params)

    if r.status_code != 200 or not r.text:
        return {"error": "Alpha Vantage request failed"}

    data = r.json()

    if "Time Series (Daily)" not in data:
        return {"error": "Invalid symbol or API limit reached"}

    series = data["Time Series (Daily)"]
    dates = list(series.keys())

    latest = series[dates[0]]
    prev = series[dates[1]]

    close_today = float(latest["4. close"])
    close_prev = float(prev["4. close"])

    trend = "UP" if close_today > close_prev else "DOWN"

    return {
        "symbol": symbol,
        "trend": trend,
        "source": "Alpha Vantage"
    }
