from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.get("/predict")
def predict(symbol: str = Query(..., example="RELIANCE.NS")):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5d&interval=1d"
    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        return {"error": "Failed to fetch data"}

    data = r.json()

    try:
        prices = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        last_price = prices[-1]
        prev_price = prices[-2]

        direction = "UP" if last_price > prev_price else "DOWN"

        return {
            "symbol": symbol,
            "last_price": last_price,
            "prediction": direction
        }
    except Exception as e:
        return {"error": "Invalid symbol or data issue"}
