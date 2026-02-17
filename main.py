import requests
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def root():
    return {"status": "India Stock API running"}

@app.get("/predict")
def predict(symbol: str = Query(..., example="RELIANCE.NS")):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"

    r = requests.get(url, timeout=10)
    data = r.json()

    result = data.get("quoteResponse", {}).get("result", [])

    if not result:
        return {"error": "Invalid symbol"}

    stock = result[0]

    return {
        "symbol": symbol,
        "price": stock.get("regularMarketPrice"),
        "change": stock.get("regularMarketChange"),
        "change_percent": stock.get("regularMarketChangePercent")
    }
