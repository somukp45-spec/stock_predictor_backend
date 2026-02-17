import requests
from fastapi import FastAPI, Query

app = FastAPI()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json"
}

@app.get("/")
def root():
    return {"status": "India Stock API running"}

@app.get("/predict")
def predict(symbol: str = Query(...)):
    try:
        url = "https://query1.finance.yahoo.com/v7/finance/quote"
        params = {"symbols": symbol}

        r = requests.get(url, params=params, headers=HEADERS, timeout=10)

        # 🔐 Yahoo protection check
        if r.status_code != 200 or not r.text.strip():
            return {
                "error": "Yahoo blocked request",
                "status_code": r.status_code
            }

        data = r.json()

        result = data.get("quoteResponse", {}).get("result", [])

        if not result:
            return {"error": "Invalid Indian stock symbol"}

        stock = result[0]

        return {
            "symbol": symbol,
            "price": stock.get("regularMarketPrice"),
            "change": stock.get("regularMarketChange"),
            "change_percent": stock.get("regularMarketChangePercent"),
            "exchange": stock.get("fullExchangeName")
        }

    except Exception as e:
        return {"error": str(e)}
