import os
import time
import requests
from fastapi import FastAPI

app = FastAPI()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
CACHE = {}
CACHE_TIME = 300  # 5 minutes

@app.get("/")
def home():
    return {"status": "India Stock Predictor API running"}

@app.get("/predict")
def predict(symbol: str):
    symbol = symbol.upper()

    if not symbol.endswith(".BSE"):
        return {"error": "Use BSE symbols only (example: RELIANCE.BSE)"}

    now = time.time()

    # ✅ CACHE CHECK
    if symbol in CACHE:
        cached_data, cached_time = CACHE[symbol]
        if now - cached_time < CACHE_TIME:
            return cached_data

    base_symbol = symbol.replace(".BSE", "")
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": base_symbol + ".BSE",
        "apikey": API_KEY
    }

    r = requests.get(url, params=params)
    data = r.json()

    if "Global Quote" not in data or not data["Global Quote"]:
        return {"error": "API limit reached or invalid symbol"}

    quote = data["Global Quote"]
    price = float(quote["05. price"])
    prev_close = float(quote["08. previous close"])

    if price > prev_close:
        signal = "BUY"
    elif price < prev_close:
        signal = "SELL"
    else:
        signal = "HOLD"

    result = {
        "symbol": symbol,
        "price": price,
        "previous_close": prev_close,
        "signal": signal
    }

    CACHE[symbol] = (result, now)
    return result
