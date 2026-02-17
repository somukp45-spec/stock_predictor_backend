import os
import requests
from fastapi import FastAPI, Query

app = FastAPI()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

@app.get("/")
def root():
    return {"status": "API running"}

@app.get("/predict")
def predict(symbol: str = Query(..., example="RELIANCE.BSE")):
    if not API_KEY:
        return {"error": "API key missing"}

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }

    r = requests.get(url, params=params, timeout=10)

    if r.status_code != 200:
        return {"error": "Alpha Vantage request failed"}

    data = r.json()

    if "Global Quote" not in data:
        return {"error": "Invalid symbol or API limit reached"}

    quote = data["Global Quote"]

    return {
        "symbol": symbol,
        "price": quote.get("05. price"),
        "change": quote.get("09. change"),
        "change_percent": quote.get("10. change percent")
    }
